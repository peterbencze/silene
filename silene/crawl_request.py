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

from typing import Callable, TYPE_CHECKING, Dict, Optional
from urllib.parse import urlparse

if TYPE_CHECKING:
    from silene.crawl_response import CrawlResponse


class CrawlRequest:
    """Represents an HTTP request which will be executed by the crawler."""

    def __init__(
            self,
            url: str,
            headers: Dict[str, str] = None,
            priority: int = 0,
            redirect_func: Callable[['CrawlResponse', 'CrawlRequest'], None] = None,
            success_func: Callable[['CrawlResponse'], None] = None,
            error_func: Callable[['CrawlResponse'], None] = None
    ) -> None:
        """
        Creates a crawl request instance.

        :param url: the URL of the request
        :param headers: the headers of the request (optional)
        :param priority: the priority of the request, higher value means higher priority, defaults to 0 (optional)
        :param redirect_func: a function that will be called when the request is redirected (status code in range of
                              300 - 399) (optional)
        :param success_func: a function that will be called with successful responses (status code in range of 200 -
                             299) (optional)
        :param error_func: a function that will be called with unsuccessful responses (status code in range of 400 -
                           499 / 500 - 599) (optional)
        """

        self._url = url
        self._domain = urlparse(url).hostname
        self._headers = headers if headers is not None else {}
        self._priority = priority
        self._redirect_func = redirect_func
        self._success_func = success_func
        self._error_func = error_func

    def merge(self, other_request: 'CrawlRequest') -> 'CrawlRequest':
        """
        Combines this crawl request with another one.
        This method will only use the other request's attribute if this request does not specify it. The result will
        be a new object.

        :param other_request: the other crawl request
        :return: a new, combined crawl request
        """

        return CrawlRequest(
            self._url,
            self._headers or other_request._headers,
            self._priority or other_request._priority,
            self._redirect_func or other_request._redirect_func,
            self._success_func or other_request._success_func,
            self._error_func or other_request._error_func
        )

    @property
    def url(self) -> str:
        """
        Returns the request URL.

        :return: the request URL
        """

        return self._url

    @property
    def domain(self) -> str:
        """
        Returns the request domain.

        :return: the request domain
        """

        return self._domain

    @property
    def headers(self) -> Optional[Dict[str, str]]:
        """
        Returns the request headers.

        :return: the request headers if specified, None otherwise
        """

        return self._headers

    @property
    def priority(self) -> int:
        """
        Returns the request priority.

        :return: the request priority
        """

        return self._priority

    @property
    def redirect_func(self) -> Optional[Callable[['CrawlResponse', 'CrawlRequest'], None]]:
        """
        Returns the function that will be called when the request is redirected.

        :return: the function that will be called when the request is redirected if specified, None otherwise
        """

        return self._redirect_func

    @property
    def success_func(self) -> Optional[Callable[['CrawlResponse'], None]]:
        """
        Returns the function that will be called with successful responses.

        :return: the function that will be called with successful responses if specified, None otherwise
        """

        return self._success_func

    @property
    def error_func(self) -> Optional[Callable[['CrawlResponse'], None]]:
        """
        Returns the function that will be called with unsuccessful responses.

        :return: the function that will be called with unsuccessful responses if specified, None otherwise
        """

        return self._error_func

    def __lt__(self, other: 'CrawlRequest') -> bool:
        """
        Compares this crawl request to another one by priority.

        :param other: the other crawl request
        :return: True if this request's priority is larger, False otherwise
        """

        return self._priority > other._priority

    def __str__(self) -> str:
        """
        Returns the string representation of the crawl request.

        :return: the string representation of the crawl request
        """

        return f'CrawlRequest(url={self._url}, domain={self._domain}, headers={len(self._headers)} headers, ' \
               f'priority={self._priority})'
