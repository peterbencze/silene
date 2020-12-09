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

from silene.browser_page import BrowserPage

index = 0
url = 'https://example.com'
title = 'Example'
page = BrowserPage(0, url, title)


def test_index_should_return_page_index():
    assert page.index == index


def test_url_should_return_page_url():
    assert page.url == url


def test_title_should_return_page_title():
    assert page.title == title
