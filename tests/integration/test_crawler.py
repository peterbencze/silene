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

import pytest
from pytest_httpserver import HTTPServer

from silene.browser_page import BrowserPage
from silene.cookie import Cookie
from silene.crawl_request import CrawlRequest
from silene.crawl_response import CrawlResponse
from silene.crawler import Crawler
from silene.crawler_configuration import CrawlerConfiguration
from silene.errors import NoSuchElementError, NoSuchPageError


def test_successful_request_handing(httpserver: HTTPServer) -> None:
    request_path = '/response-success'
    request_url = httpserver.url_for(request_path)
    response_data = 'Test'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert response.request.url == request_url
            assert response.status == 200
            assert len(response.headers) > 0
            assert response.text == response_data

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_request_redirect_handling(httpserver: HTTPServer) -> None:
    redirect_origin_path = '/redirect-origin'
    redirect_target_path = '/redirect-target'
    redirect_origin_url = httpserver.url_for(redirect_origin_path)
    redirect_target_url = httpserver.url_for(redirect_target_path)
    headers = {'Location': redirect_target_url}
    httpserver.expect_ordered_request(redirect_origin_path, method='HEAD').respond_with_data(status=301,
                                                                                             headers=headers)
    httpserver.expect_ordered_request(redirect_target_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(redirect_target_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(redirect_origin_url)])

        def on_request_redirect(self, response: CrawlResponse, redirected_request: CrawlRequest) -> None:
            assert response.request.url == redirect_origin_url
            assert redirected_request.url == redirect_target_url
            assert response.status == 301
            assert len(response.headers) > 0
            assert response.text is None

        def on_response_success(self, response: CrawlResponse) -> None:
            assert response.request.url == redirect_target_url
            assert response.status == 200
            assert len(response.headers) > 0
            assert response.text == ''

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_request_error_handling(httpserver: HTTPServer) -> None:
    request_path = '/response-error'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(status=500)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert False, f'Response success: {response}'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert response.request.url == request_url
            assert response.status == 500
            assert len(response.headers) > 0
            assert response.text == ''

    TestCrawler().start()

    httpserver.check_assertions()


def test_custom_request_header_handling(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD', headers={'foo': 'bar'}).respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET', headers={'foo': 'bar'}).respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url, headers={'foo': 'bar'})])

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_on_start_should_be_called_when_crawler_starts():
    called = False

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([])

        def on_start(self) -> None:
            nonlocal called
            called = True

    TestCrawler().start()

    assert called is True


def test_on_stop_should_be_called_when_crawler_stops():
    called = False

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([])

        def on_stop(self) -> None:
            nonlocal called
            called = True

    TestCrawler().start()

    assert called is True


def test_crawl(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path, method='GET').respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(first_page_url, success_func=self.on_first_response)])

        def on_first_response(self, _: CrawlResponse) -> None:
            assert self.crawl(CrawlRequest(second_page_url)) is True

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_click_when_element_is_found(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    response_data = f'<a id="link" href="{second_page_url}">Click me</a>'
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path, method='GET').respond_with_data(content_type='text/html',
                                                                                       response_data=response_data)
    httpserver.expect_ordered_request(second_page_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(first_page_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            self.click('#link')

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_click_when_element_is_not_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            with pytest.raises(NoSuchElementError) as exc_info:
                self.click('#nonexistent')

            assert str(exc_info.value) == 'Unable to locate element using selector #nonexistent'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_close_page_when_there_is_only_one_page(httpserver: HTTPServer):
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            page = self.get_current_page()

            with pytest.raises(ValueError) as exc_info:
                self.close_page(page)

            assert str(exc_info.value) == 'Cannot close the last page'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_close_page_when_there_are_multiple_pages(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    first_page_response_data = f'''
        <title>First page</title>
        <a id="link" href="{second_page_url}" target="_blank">Go to second page</a>
    '''
    second_page_response_data = f'<title>Second page</title>'
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=first_page_response_data)
    httpserver.expect_ordered_request(second_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=second_page_response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(first_page_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            self.click_and_wait('#link', timeout=1000)
            pages = self.get_pages()
            self.close_page(pages[1])
            pages = self.get_pages()

            assert len(pages) == 1
            assert pages[0].index == 0
            assert pages[0].url == first_page_url
            assert pages[0].title == 'First page'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_delete_cookie(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    third_page_path = '/third-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    third_page_url = httpserver.url_for(third_page_path)
    cookie = Cookie('cookie_name', 'cookie_value')
    headers = {'Cookie': 'cookie_name=cookie_value'}
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path, method='GET').respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='HEAD', headers=headers).respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='GET', headers=headers).respond_with_data()
    httpserver.expect_ordered_request(third_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(third_page_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([
                CrawlRequest(first_page_url, success_func=self.on_first_page_response),
                CrawlRequest(second_page_url, success_func=self.on_second_page_response),
                CrawlRequest(third_page_url, success_func=self.on_third_page_response)
            ])

        def on_first_page_response(self, _: CrawlResponse) -> None:
            self.set_cookie(cookie)

        def on_second_page_response(self, _: CrawlResponse) -> None:
            assert len(self.get_cookies()) == 1

            self.delete_cookie(cookie)

        def on_third_page_response(self, _: CrawlResponse) -> None:
            assert len(self.get_cookies()) == 0

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_evaluate_when_element_is_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '<div id="test">Test</div>'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert self.evaluate('#test', 'element => element.textContent') == 'Test'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_evaluate_when_element_is_not_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            with pytest.raises(NoSuchElementError) as exc_info:
                self.evaluate('#nonexistent', 'element => element.textContent')

            assert str(exc_info.value) == 'Unable to locate element using selector #nonexistent'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_find_element_when_element_is_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '<div id="test">Test</div>'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            element = self.find_element('#test')

            assert element.get_attribute('id') == 'test'
            assert element.get_text() == 'Test'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_find_element_when_element_is_not_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert self.find_element('#nonexistent') is None

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_get_cookies(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    headers = {'Set-Cookie': 'cookie_name=cookie_value'}
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(headers=headers)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            cookies = self.get_cookies()

            assert len(cookies) == 1
            assert cookies[0].name == 'cookie_name'
            assert cookies[0].value == 'cookie_value'
            assert cookies[0].domain == 'localhost'
            assert cookies[0].path == '/'
            assert cookies[0].expires == -1
            assert cookies[0].http_only is False
            assert cookies[0].secure is False
            assert cookies[0].session is True
            assert cookies[0].same_site is None

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_get_current_page(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '<title>Test</title>'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            page = self.get_current_page()

            assert page.index == 0
            assert page.url == request_url
            assert page.title == 'Test'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_get_title(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '<title>Test title</title>'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert self.get_title() == 'Test title'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_get_url(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            assert self.get_url() == request_url

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_get_pages(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    first_page_response_data = f'''
        <title>First page</title>
        <a id="link" href="{second_page_url}" target="_blank">Go to second page</a>
    '''
    second_page_response_data = f'<title>Second page</title>'
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=first_page_response_data)
    httpserver.expect_ordered_request(second_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=second_page_response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(first_page_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            self.click_and_wait('#link', timeout=500)
            pages = self.get_pages()

            assert len(pages) == 2
            assert pages[0].index == 0
            assert pages[0].url == first_page_url
            assert pages[0].title == 'First page'
            assert pages[1].index == 1
            assert pages[1].url == second_page_url
            assert pages[1].title == 'Second page'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_select_when_element_is_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '''
                    <select id="test" multiple>
                        <option value="foo">foo</option>
                        <option value="bar">bar</option>
                        <option value="baz">baz</option>
                    </select>
    '''
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            values = ['foo', 'bar']
            assert self.select('#test', values) == values

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_select_when_element_is_not_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            with pytest.raises(NoSuchElementError) as exc_info:
                self.select('#nonexistent', ['foo', 'bar'])

            assert str(exc_info.value) == 'Unable to locate element using selector #nonexistent'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_set_cookie(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    headers = {'Cookie': 'cookie_name=cookie_value'}
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path, method='GET').respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='HEAD', headers=headers).respond_with_data()
    httpserver.expect_ordered_request(second_page_path, method='GET', headers=headers).respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([
                CrawlRequest(first_page_url, success_func=self.on_first_page_response),
                CrawlRequest(second_page_url)
            ])

        def on_first_page_response(self, _: CrawlResponse) -> None:
            self.set_cookie(Cookie('cookie_name', 'cookie_value'))

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_switch_to_page_when_page_exists(httpserver: HTTPServer) -> None:
    first_page_path = '/first-page'
    second_page_path = '/second-page'
    first_page_url = httpserver.url_for(first_page_path)
    second_page_url = httpserver.url_for(second_page_path)
    first_page_response_data = f'''
            <title>First page</title>
            <a id="link" href="{second_page_url}" target="_blank">Go to second page</a>
        '''
    second_page_response_data = f'<title>Second page</title>'
    httpserver.expect_ordered_request(first_page_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(first_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=first_page_response_data)
    httpserver.expect_ordered_request(second_page_path,
                                      method='GET').respond_with_data(content_type='text/html',
                                                                      response_data=second_page_response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(first_page_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            self.click_and_wait('#link', timeout=500)
            pages = self.get_pages()
            self.switch_to_page(pages[1])
            current_page = self.get_current_page()

            assert current_page.index == 1
            assert current_page.url == second_page_url
            assert current_page.title == 'Second page'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_switch_to_page_when_page_does_not_exist(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            with pytest.raises(NoSuchPageError) as exc_info:
                self.switch_to_page(BrowserPage(1, request_url, 'Nonexistent'))

            assert str(exc_info.value) == 'No page exists with index 1'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_type_when_element_is_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    response_data = '<input type="text" id="test">'
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data(content_type='text/html')
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data(content_type='text/html',
                                                                                    response_data=response_data)

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            value = 'Test'
            self.type('#test', value)

            assert self.evaluate('#test', 'element => element.value') == value

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()


def test_type_when_element_is_not_found(httpserver: HTTPServer) -> None:
    request_path = '/page'
    request_url = httpserver.url_for(request_path)
    httpserver.expect_ordered_request(request_path, method='HEAD').respond_with_data()
    httpserver.expect_ordered_request(request_path, method='GET').respond_with_data()

    class TestCrawler(Crawler):
        def configure(self) -> CrawlerConfiguration:
            return CrawlerConfiguration([CrawlRequest(request_url)])

        def on_response_success(self, response: CrawlResponse) -> None:
            with pytest.raises(NoSuchElementError) as exc_info:
                self.type('#nonexistent', 'Test')

            assert str(exc_info.value) == 'Unable to locate element using selector #nonexistent'

        def on_response_error(self, response: CrawlResponse) -> None:
            assert False, f'Response error: {response}'

    TestCrawler().start()

    httpserver.check_assertions()
