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

from typing import List

import tld
from tld.exceptions import TldDomainNotFound

from silene.crawl_request import CrawlRequest


class CrawlerConfiguration:
    """Specifies settings of the crawler."""

    def __init__(
            self,
            seed_requests: List[CrawlRequest],
            filter_duplicate_requests: bool = True,
            filter_offsite_requests: bool = False,
            allowed_domains: List[str] = None
    ) -> None:
        """
        Creates a new crawler configuration instance.

        :param seed_requests: the list of initial crawl requests to make
        :param filter_duplicate_requests: toggles duplicate request filtering, defaults to True (optional)
        :param filter_offsite_requests: toggles offsite request filtering, defaults to False (optional)
        :param allowed_domains: the list of allowed domains (optional)
        """

        self._seed_requests = seed_requests
        self._filter_duplicate_requests = filter_duplicate_requests
        self._filter_offsite_requests = filter_offsite_requests
        self._allowed_domains = []
        if allowed_domains:
            for domain in allowed_domains:
                try:
                    result = tld.get_tld(domain, as_object=True, fix_protocol=True)
                    self._allowed_domains.append(result.parsed_url.hostname)
                except TldDomainNotFound:
                    raise ValueError(f'Could not extract a valid domain from {domain}')

    @property
    def seed_requests(self) -> List[CrawlRequest]:
        """
        Returns the list of initial crawl requests to make.

        :return: the list of initial crawl requests to make
        """

        return self._seed_requests

    @property
    def filter_duplicate_requests(self) -> bool:
        """
        Returns a value indicating whether the duplicate request filter is enabled or not.

        :return: True if the duplicate request filter is enabled, False otherwise
        """

        return self._filter_duplicate_requests

    @property
    def filter_offsite_requests(self) -> bool:
        """
        Returns a value indicating whether the offsite request filter is enabled or not.

        :return: True if the offsite request filter is enabled, False otherwise
        """

        return self._filter_offsite_requests

    @property
    def allowed_domains(self) -> List[str]:
        """
        Returns the list of allowed domains.
        This setting has effect only when the offsite request filter is enabled.

        :return: the list of allowed domains
        """

        return self._allowed_domains

    def __str__(self):
        """
        Returns the string representation of the crawler configuration.

        :return: the string representation of the crawler configuration
        """

        return f'CrawlerConfiguration(seed_requests={len(self._seed_requests)} requests, ' \
               f'filter_duplicate_requests={self._filter_duplicate_requests}, ' \
               f'filter_offsite_requests={self._filter_offsite_requests}, ' \
               f'allowed_domains={len(self._allowed_domains)} domains)'
