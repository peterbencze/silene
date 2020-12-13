# Copyright 2020 Peter Bencze
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from typing import Optional, List

import pyppeteer
import syncer
from pyppeteer.browser import Browser
from pyppeteer.errors import PageError, ElementHandleError
from pyppeteer.network_manager import Request, Response
from pyppeteer.page import Page

from silene.browser_page import BrowserPage
from silene.crawl_frontier import CrawlFrontier
from silene.crawl_request import CrawlRequest
from silene.crawl_response import CrawlResponse
from silene.crawler_configuration import CrawlerConfiguration
from silene.element import Element
from silene.errors import NoSuchElementError, WaitTimeoutError, CrawlerNotRunningError, NoSuchPageError

logger = logging.getLogger(__name__)


class Crawler(ABC):
    def __init__(
            self,
            crawl_frontier: CrawlFrontier = None
    ) -> None:
        self._configuration: CrawlerConfiguration = self.configure()
        self._crawl_frontier: CrawlFrontier = crawl_frontier or CrawlFrontier(self._configuration)
        self._running: bool = False
        self._stop_initiated: bool = False
        self._browser: Optional[Browser] = None
        self._page: Optional[Page] = None
        self._page_index: Optional[int] = None
        self._next_request: Optional[CrawlRequest] = None
        self._send_head_request: bool = False
        self._aborted_request: bool = False
        self._last_request: Optional[Request] = None
        self._last_response: Optional[Response] = None

    @abstractmethod
    def configure(self) -> CrawlerConfiguration:
        pass

    def start(self) -> None:
        self._running = True
        self._browser = syncer.sync(pyppeteer.launch())
        self._page = syncer.sync(self._browser.pages())[0]  # about:blank page
        self._page_index = 0
        self._add_page_listeners(self._page)

        self.on_start()
        self._run()
        self.on_stop()

        syncer.sync(self._page.close())
        syncer.sync(self._browser.close())
        self._running = False
        self._stop_initiated = False

    def crawl(self, request: CrawlRequest) -> bool:
        return self._crawl_frontier.add_request(request)

    def click(self, selector: str, click_count=1) -> None:
        self._check_if_crawler_running()

        try:
            syncer.sync(self._page.click(selector, options={'clickCount': click_count}))
        except PageError:
            raise NoSuchElementError(selector)

    def click_and_wait(self, selector: str, click_count=1, timeout=30000) -> None:
        self._check_if_crawler_running()

        syncer.sync(asyncio.wait([
            self._page.click(selector, options={'clickCount': click_count}),
            self._page.waitForNavigation(options={'timeout': timeout})
        ]))

    def close_page(self, page: BrowserPage) -> None:
        self._check_if_crawler_running()

        pages = syncer.sync(self._browser.pages())
        if len(pages) == 1:
            raise ValueError('Cannot close the last page')

        syncer.sync(pages[page.index].close())

    def double_click(self, selector: str) -> None:
        self.click(selector, click_count=2)

    def evaluate(self, selector: str, function: str):
        try:
            return syncer.sync(self._page.querySelectorEval(selector, function))
        except ElementHandleError:
            raise NoSuchElementError(selector)

    def find_element(self, selector: str) -> Optional[Element]:
        self._check_if_crawler_running()

        element_handle = syncer.sync(self._page.querySelector(selector))
        return Element(element_handle) if element_handle else None

    def get_current_page(self) -> BrowserPage:
        return BrowserPage(self._page_index, self._page.url, syncer.sync(self._page.title()))

    def get_pages(self) -> List[BrowserPage]:
        self._check_if_crawler_running()

        return [
            BrowserPage(index, page.url, syncer.sync(page.title()))
            for index, page in enumerate(syncer.sync(self._browser.pages()))
        ]

    def get_title(self) -> str:
        self._check_if_crawler_running()

        return syncer.sync(self._page.title())

    def get_url(self) -> str:
        self._check_if_crawler_running()

        return self._page.url

    def select(self, selector: str, values: List[str]) -> List[str]:
        self._check_if_crawler_running()

        try:
            return syncer.sync(self._page.select(selector, *values))
        except ElementHandleError:
            raise NoSuchElementError(selector)

    def switch_to_page(self, page: BrowserPage) -> None:
        self._check_if_crawler_running()

        try:
            self._page = syncer.sync(self._browser.pages())[page.index]
        except IndexError:
            raise NoSuchPageError(page.index)

        self._page_index = page.index
        syncer.sync(self._page.bringToFront())
        self._add_page_listeners(self._page)

    def type(self, selector: str, value: str) -> None:
        self._check_if_crawler_running()

        try:
            syncer.sync(self._page.querySelectorEval(selector, f'element => element.value = {json.dumps(value)}'))
        except ElementHandleError:
            raise NoSuchElementError(selector)

    def wait_for_selector(
            self,
            selector: str,
            visible: bool = False,
            hidden: bool = False,
            timeout: int = 30000
    ) -> None:
        self._check_if_crawler_running()

        # WaitTask class is not compatible with syncer, this async method is a workaround
        async def wait_for_selector() -> None:
            await self._page.waitForSelector(selector, {'visible': visible, 'hidden': hidden, 'timeout': timeout})

        try:
            syncer.sync(wait_for_selector())
        except pyppeteer.errors.TimeoutError:
            raise WaitTimeoutError(timeout, selector)

    def wait_for_timeout(self, milliseconds: int) -> None:
        self._check_if_crawler_running()

        syncer.sync(self._page.waitFor(milliseconds))

    def stop(self) -> None:
        self._stop_initiated = True

    def on_start(self) -> None:
        logger.info('Crawler is starting')

    def on_request_redirect(self, response: CrawlResponse, redirected_request: CrawlRequest) -> None:
        logger.info('Request redirect: %s -> %s', response.request, redirected_request)

    def on_response_success(self, response: CrawlResponse) -> None:
        logger.info('Response success: %s', response)

    def on_response_error(self, response: CrawlResponse) -> None:
        logger.info('Response error: %s', response)

    def on_stop(self) -> None:
        logger.info('Crawler is stopping')

    def _check_if_crawler_running(self) -> None:
        if not self._running:
            raise CrawlerNotRunningError()

    def _run(self) -> None:
        while not self._stop_initiated and self._crawl_frontier.has_next_request():
            self._aborted_request = False
            self._next_request = self._crawl_frontier.get_next_request()

            # Send a HEAD request first
            self._send_head_request = True
            try:
                syncer.sync(self._page.goto(self._next_request.url))
            except PageError as error:
                # Ignore exceptions that are caused by aborted requests
                if self._aborted_request:
                    # Request was redirected, create a new crawl request for it
                    self._handle_redirect(self._next_request, self._last_request, self._last_response)
                    continue
                else:
                    raise error

            # Send a GET request
            self._send_head_request = False
            self._handle_response(self._next_request, syncer.sync(self._page.goto(self._next_request.url)))

    def _add_page_listeners(self, page: Page) -> None:
        syncer.sync(self._page.setRequestInterception(True))
        page.on('request', self._on_request)
        page.on('response', self._on_response)

    async def _on_request(self, request: Request) -> None:
        self._last_request = request

        if request.isNavigationRequest() and len(request.redirectChain) > 0:
            self._aborted_request = True
            await request.abort()
        else:
            overrides = {}

            if self._send_head_request:
                overrides['method'] = 'HEAD'

            if request.headers:
                headers = request.headers.copy()
                headers.update(self._next_request.headers)
                overrides['headers'] = headers

            await request.continue_(overrides)

    async def _on_response(self, response: Response) -> None:
        self._last_response = response

    def _handle_redirect(self, origin_crawl_request: CrawlRequest, origin_request: Request, response: Response):
        crawl_response = CrawlResponse(origin_crawl_request, response.status, response.headers, None)
        redirected_request = CrawlRequest(origin_request.url).merge(origin_crawl_request)

        self.crawl(redirected_request)
        origin_crawl_request.redirect_func(crawl_response, redirected_request) if origin_crawl_request.redirect_func \
            else self.on_request_redirect(crawl_response, redirected_request)

    def _handle_response(self, request: CrawlRequest, response: Response):
        crawl_response = CrawlResponse(request, response.status, response.headers, syncer.sync(response.text()))

        if 200 <= response.status < 300:
            request.success_func(crawl_response) if request.success_func else self.on_response_success(
                crawl_response)
        else:
            request.error_func(crawl_response) if request.error_func else self.on_response_error(crawl_response)
