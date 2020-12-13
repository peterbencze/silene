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

from typing import Callable, TYPE_CHECKING
from urllib.parse import urlparse

if TYPE_CHECKING:
    from silene.crawl_response import CrawlResponse


class CrawlRequest:
    def __init__(
            self,
            url: str,
            priority: int = 0,
            redirect_func: Callable[['CrawlResponse', 'CrawlRequest'], None] = None,
            success_func: Callable[['CrawlResponse'], None] = None,
            error_func: Callable[['CrawlResponse'], None] = None
    ) -> None:
        self._url = url
        self._domain = urlparse(url).hostname
        self._priority = priority
        self._redirect_func = redirect_func
        self._success_func = success_func
        self._error_func = error_func

    def merge(self, other_request: 'CrawlRequest') -> 'CrawlRequest':
        return CrawlRequest(
            self._url,
            self._priority or other_request._priority,
            self._redirect_func or other_request._redirect_func,
            self._success_func or other_request._success_func,
            self._error_func or other_request._error_func
        )

    @property
    def url(self) -> str:
        return self._url

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def redirect_func(self) -> Callable[['CrawlResponse', 'CrawlRequest'], None]:
        return self._redirect_func

    @property
    def success_func(self) -> Callable[['CrawlResponse'], None]:
        return self._success_func

    @property
    def error_func(self) -> Callable[['CrawlResponse'], None]:
        return self._error_func

    def __lt__(self, other: 'CrawlRequest') -> bool:
        return self._priority > other._priority

    def __str__(self):
        return f'CrawlRequest(url={self._url}, domain={self._domain}, priority={self._priority})'
