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

from silene.crawl_request import CrawlRequest


def redirect_func():
    # Intentionally left empty
    pass


def success_func():
    # Intentionally left empty
    pass


def error_func():
    # Intentionally left empty
    pass


def test_merge_should_return_new_combined_crawl_request() -> None:
    request = CrawlRequest('https://example.com')
    other_request = CrawlRequest('https://test.com', priority=1, redirect_func=redirect_func, success_func=success_func,
                                 error_func=error_func)

    combined_request = request.merge(other_request)

    assert combined_request.url == request.url
    assert combined_request.domain == request.domain
    assert combined_request.priority == other_request.priority
    assert combined_request.redirect_func == other_request.redirect_func
    assert combined_request.success_func == other_request.success_func
    assert combined_request.error_func == other_request.error_func


def test_url_should_return_request_url() -> None:
    url = 'https://example.com'

    assert CrawlRequest(url).url == url


def test_domain_should_return_request_domain() -> None:
    assert CrawlRequest('https://example.com').domain == 'example.com'


def test_priority_should_return_request_priority() -> None:
    priority = 1

    assert CrawlRequest('https://example.com', priority=priority).priority == priority


def test_redirect_func_should_return_alternative_redirect_function() -> None:
    assert CrawlRequest('https://example.com', redirect_func=redirect_func).redirect_func == redirect_func


def test_success_func_should_return_alternative_success_function() -> None:
    assert CrawlRequest('https://example.com', success_func=success_func).success_func == success_func


def test_error_func_should_return_alternative_error_function() -> None:
    assert CrawlRequest('https://example.com', error_func=error_func).error_func == error_func


def test_str_should_return_string_representation() -> None:
    assert str(CrawlRequest('https://example.com', priority=1)) == \
           'CrawlRequest(url=https://example.com, domain=example.com, priority=1)'
