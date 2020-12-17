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

from typing import Dict, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from silene.crawl_request import CrawlRequest


class CrawlResponse:
    """Represents an HTTP response."""

    def __init__(
            self,
            request: 'CrawlRequest',
            status: int,
            headers: Dict[str, str],
            text: str = None
    ) -> None:
        """
        Creates a new crawl response instance.

        :param request: the request that generated this response
        :param status: the response status
        :param headers: the response headers
        :param text: the response text (optional)
        """

        self._request = request
        self._status = status
        self._headers = headers
        self._text = text

    @property
    def request(self) -> 'CrawlRequest':
        """
        Returns the request that generated this response.

        :return: the request that generated this response
        """

        return self._request

    @property
    def status(self) -> int:
        """
        Returns the response status.

        :return: the response status
        """

        return self._status

    @property
    def headers(self) -> Dict[str, str]:
        """
        Returns the response headers.

        :return: the reponse headers
        """

        return self._headers

    @property
    def text(self) -> Optional[str]:
        """
        Returns the response text.

        :return: the response text if specified, None otherwise
        """

        return self._text

    def __str__(self) -> str:
        """
        Returns the string representation of the crawl response.

        :return: the string representation of the crawl response
        """

        return f'CrawlResponse(url={self._request.url}, status={self._status})'
