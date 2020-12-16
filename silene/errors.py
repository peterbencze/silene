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

class SileneError(Exception):
    pass


class CrawlerNotRunningError(SileneError):
    def __init__(self) -> None:
        self._message = 'Crawler is not running'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message


class NoSuchPageError(SileneError):
    def __init__(self, index: int) -> None:
        self._message = f'No page exists with index {index}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message


class NoSuchElementError(SileneError):
    def __init__(self, selector: str) -> None:
        self._message = f'Unable to locate element using selector {selector}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message


class WaitTimeoutError(SileneError):
    def __init__(self, timeout: int, selector: str) -> None:
        self._message = f'Timeout {timeout}ms exceeded waiting for selector {selector}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message


class NavigationTimeoutError(SileneError):
    def __init__(self, timeout: int) -> None:
        self._message = f'Timeout {timeout}ms exceeded waiting for navigation'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message
