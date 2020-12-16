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

from silene.errors import CrawlerNotRunningError, NoSuchPageError, NoSuchElementError, WaitTimeoutError, \
    NavigationTimeoutError


class TestCrawlerNotRunningError:
    error: CrawlerNotRunningError = CrawlerNotRunningError()

    def test_message_should_return_error_message(self) -> None:
        assert self.error.message == 'Crawler is not running'

    def test_str_should_return_string_representation(self) -> None:
        assert str(self.error) == 'Crawler is not running'


class TestNoSuchPageError:
    error: NoSuchPageError = NoSuchPageError(index=0)

    def test_message_should_return_error_message(self) -> None:
        assert self.error.message == 'No page exists with index 0'

    def test_str_should_return_string_representation(self) -> None:
        assert str(self.error) == 'No page exists with index 0'


class TestNoSuchElementError:
    error: NoSuchElementError = NoSuchElementError(selector='#test')

    def test_message_should_return_error_message(self) -> None:
        assert self.error.message == 'Unable to locate element using selector #test'

    def test_str_should_return_string_representation(self) -> None:
        assert str(self.error) == 'Unable to locate element using selector #test'


class TestWaitTimeoutError:
    error: WaitTimeoutError = WaitTimeoutError(selector='#test', timeout=1000)

    def test_message_should_return_error_message(self) -> None:
        assert self.error.message == 'Timeout 1000ms exceeded waiting for selector #test'

    def test_str_should_return_string_representation(self) -> None:
        assert str(self.error) == 'Timeout 1000ms exceeded waiting for selector #test'


class TestNavigationTimeoutError:
    error: NavigationTimeoutError = NavigationTimeoutError(timeout=1000)

    def test_message_should_return_error_message(self) -> None:
        assert self.error.message == 'Timeout 1000ms exceeded waiting for navigation'

    def test_str_should_return_string_representation(self) -> None:
        assert str(self.error) == 'Timeout 1000ms exceeded waiting for navigation'
