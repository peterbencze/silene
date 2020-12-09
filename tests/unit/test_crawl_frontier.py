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

from silene.crawl_frontier import CrawlFrontier
from silene.crawl_request import CrawlRequest
from silene.crawler_configuration import CrawlerConfiguration

request = CrawlRequest(url='http://example.com')


def test_add_request_should_add_duplicate_request_to_queue_when_duplicate_request_filter_is_disabled() -> None:
    crawler_configuration = CrawlerConfiguration([request], filter_duplicate_requests=False)
    crawl_frontier = CrawlFrontier(crawler_configuration)
    crawl_frontier.get_next_request()

    result = crawl_frontier.add_request(request)

    assert result is True
    assert crawl_frontier.get_next_request() is request


def test_add_request_should_not_add_duplicate_request_to_queue_when_duplicate_request_filter_is_enabled() -> None:
    crawler_configuration = CrawlerConfiguration([CrawlRequest(url='http://example.com/test?abc=def&ghi=jkl#fragment')])
    crawl_frontier = CrawlFrontier(crawler_configuration)
    crawl_frontier.get_next_request()

    result = crawl_frontier.add_request(CrawlRequest(url='http://example.com/test?ghi=jkl&abc=def'))

    assert result is False
    assert crawl_frontier.get_next_request() is None


def test_add_request_should_add_request_to_queue_when_offsite_request_filter_is_disabled() -> None:
    crawler_configuration = CrawlerConfiguration([], filter_offsite_requests=False, allowed_domains=['notexample.com'])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    result = crawl_frontier.add_request(request)

    assert result is True
    assert crawl_frontier.get_next_request() is request


def test_add_request_should_not_add_offsite_request_to_queue_when_offsite_request_filter_is_enabled() -> None:
    crawler_configuration = CrawlerConfiguration([], filter_offsite_requests=True, allowed_domains=['notexample.com'])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    result = crawl_frontier.add_request(request)

    assert result is False
    assert crawl_frontier.get_next_request() is None


def test_add_request_should_add_allowed_request_to_queue_when_offsite_request_filter_is_enabled() -> None:
    crawler_configuration = CrawlerConfiguration([], filter_offsite_requests=True, allowed_domains=['example.com'])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    result = crawl_frontier.add_request(request)

    assert result is True
    assert crawl_frontier.get_next_request() is request


def test_has_next_request_should_return_false_when_queue_is_empty() -> None:
    crawler_configuration = CrawlerConfiguration([])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    assert crawl_frontier.has_next_request() is False


def test_has_next_request_should_return_true_when_queue_is_not_empty() -> None:
    crawler_configuration = CrawlerConfiguration([request])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    assert crawl_frontier.has_next_request() is True


def test_get_next_request_should_return_none_when_queue_is_empty() -> None:
    crawler_configuration = CrawlerConfiguration([])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    assert crawl_frontier.get_next_request() is None


def test_get_next_request_should_return_next_request_when_queue_is_not_empty() -> None:
    crawler_configuration = CrawlerConfiguration([request])
    crawl_frontier = CrawlFrontier(crawler_configuration)

    assert crawl_frontier.get_next_request() is request
