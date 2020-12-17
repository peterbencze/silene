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

import heapq
import re
from hashlib import sha256
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from silene.crawl_request import CrawlRequest
from silene.crawler_configuration import CrawlerConfiguration


class CrawlFrontier:
    """
    This class is used for managing URLs eligible for crawling and supporting such operations as adding requests and
    selecting for crawl.
    """

    def __init__(
            self,
            crawler_configuration: CrawlerConfiguration
    ) -> None:
        """
        Creates a new crawl frontier instance.

        :param crawler_configuration: the crawler configuration
        """

        self._crawler_configuration = crawler_configuration
        self._requests = []
        self._url_hashes = set()
        self._allowed_domain_pattern = re.compile(fr'^(?:.*\.)?({"|".join(crawler_configuration.allowed_domains)})$')

        for request in crawler_configuration.seed_requests:
            self.add_request(request)

    def add_request(self, request: CrawlRequest) -> bool:
        """
        Adds a crawl requests to the queue.

        :param request: the crawl request to add to the queue
        :return: True if the request was added to the queue, False otherwise (filtered out)
        """

        if self._crawler_configuration.filter_duplicate_requests:
            url_hash = self._generate_url_hash(request.url)
            if url_hash in self._url_hashes:
                return False
            else:
                self._url_hashes.add(url_hash)

        if self._crawler_configuration.filter_offsite_requests and not re.search(self._allowed_domain_pattern,
                                                                                 request.domain):
            return False

        heapq.heappush(self._requests, request)
        return True

    def has_next_request(self) -> bool:
        """
        Returns a value indicating whether the queue has any remaining crawl requests or not.

        :return: True if the queue is not empty, False otherwise
        """

        return len(self._requests) > 0

    def get_next_request(self) -> Optional[CrawlRequest]:
        """
        Returns the next crawl request.

        :return: the next crawl request if the queue is not empty, None otherwise
        """

        try:
            return heapq.heappop(self._requests)
        except IndexError:
            # If heap is empty
            return None

    @staticmethod
    def _generate_url_hash(url: str) -> str:
        url_parts = urlparse(url)
        sorted_query_params = sorted(parse_qsl(url_parts.query), key=lambda param: (param[0], param[1]))
        url_parts = url_parts._replace(query=urlencode(sorted_query_params), fragment='')
        normalized_url = urlunparse(url_parts)
        return sha256(str(normalized_url).encode('utf-8')).hexdigest()
