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

from silene.crawl_request import CrawlRequest
from silene.crawler_configuration import CrawlerConfiguration


def test_constructor_should_raise_value_error_when_invalid_domain_in_allowed_domains() -> None:
    with pytest.raises(ValueError) as exc_info:
        CrawlerConfiguration([], allowed_domains=['example.invalid'])

    assert str(exc_info.value) == 'Could not extract a valid domain from example.invalid'


def test_seed_requests_should_return_seed_requests() -> None:
    seed_requests = [CrawlRequest('https://example.com')]
    crawler_configuration = CrawlerConfiguration(seed_requests)

    assert crawler_configuration.seed_requests is seed_requests


def test_filter_duplicate_requests_should_return_default_value_when_not_specified() -> None:
    crawler_configuration = CrawlerConfiguration([])

    assert crawler_configuration.filter_duplicate_requests is True


def test_filter_duplicate_requests_should_return_specified_value_when_specified() -> None:
    crawler_configuration = CrawlerConfiguration([], filter_duplicate_requests=False)

    assert crawler_configuration.filter_duplicate_requests is False


def test_filter_offsite_requests_should_return_default_value_when_not_specified() -> None:
    crawler_configuration = CrawlerConfiguration([])

    assert crawler_configuration.filter_offsite_requests is False


def test_filter_offsite_requests_should_return_specified_value_when_specified() -> None:
    crawler_configuration = CrawlerConfiguration([], filter_offsite_requests=True)

    assert crawler_configuration.filter_offsite_requests is True


def test_allowed_domains_should_return_empty_list_when_no_allowed_domains_specified() -> None:
    crawler_configuration = CrawlerConfiguration([])

    assert crawler_configuration.allowed_domains == []


def test_allowed_domains_should_return_domains_only() -> None:
    crawler_configuration = CrawlerConfiguration([], allowed_domains=['https://www.example.com:80/'])

    assert crawler_configuration.allowed_domains == ['www.example.com']
