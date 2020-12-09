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
from silene.crawl_response import CrawlResponse

request = CrawlRequest('https://example.com')


def test_request_should_return_request() -> None:
    assert CrawlResponse(request, 200, {}).request is request


def test_status_should_return_response_status() -> None:
    assert CrawlResponse(request, 200, {}).status == 200


def test_headers_should_return_response_headers() -> None:
    headers = {'Content-Type': 'text/html; charset=utf-8'}

    assert CrawlResponse(request, 200, headers).headers == headers


def test_text_should_return_none_when_text_content_is_not_set() -> None:
    assert CrawlResponse(request, 200, {}).text is None


def test_text_should_return_text_content_when_text_content_is_set() -> None:
    text_content = 'Test'

    assert CrawlResponse(request, 200, {}, text=text_content).text == text_content
