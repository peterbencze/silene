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
    def __init__(
            self,
            seed_requests: List[CrawlRequest],
            filter_duplicate_requests: bool = True,
            filter_offsite_requests: bool = False,
            allowed_domains: List[str] = None
    ) -> None:
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
        return self._seed_requests

    @property
    def filter_duplicate_requests(self) -> bool:
        return self._filter_duplicate_requests

    @property
    def filter_offsite_requests(self) -> bool:
        return self._filter_offsite_requests

    @property
    def allowed_domains(self) -> List[str]:
        return self._allowed_domains
