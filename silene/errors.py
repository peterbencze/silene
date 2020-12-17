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
    """Base class for Silene related errors."""

    pass


class CrawlerNotRunningError(SileneError):
    """Error that is raised if a function is called when the crawler is not running."""

    def __init__(self) -> None:
        """Creates a new instance of this class."""

        self._message = 'Crawler is not running'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        :return: the error message
        """

        return self._message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        :return: the string representation of the error
        """

        return self._message


class NoSuchPageError(SileneError):
    """Error that is raised when a page with an index is not found."""

    def __init__(self, index: int) -> None:
        """
        Creates a new instance of this class.

        :param index: the page index that is not found
        """

        self._message = f'No page exists with index {index}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        :return: the error message
        """

        return self._message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        :return: the string representation of the error
        """

        return self._message


class NoSuchElementError(SileneError):
    """Error that is raised when there is no element matching selector"""

    def __init__(self, selector: str) -> None:
        """
        Creates a new instance of this class.

        :param selector: the element selector
        """

        self._message = f'Unable to locate element using selector {selector}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        :return: the error message
        """

        return self._message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        :return: the string representation of the error
        """

        return self._message


class WaitTimeoutError(SileneError):
    """Error that is raised when a timeout occurs."""

    def __init__(self, timeout: int, selector: str) -> None:
        """
        Creates a new instance of this class.

        :param timeout: the timeout (in milliseconds)
        :param selector: the element selector
        """

        self._message = f'Timeout {timeout}ms exceeded waiting for selector {selector}'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        :return: the error message
        """

        return self._message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        :return: the string representation of the error
        """

        return self._message


class NavigationTimeoutError(SileneError):
    """Error that is raised when a navigation timeout occurs."""

    def __init__(self, timeout: int) -> None:
        """
        Creates a new instance of this class.

        :param timeout: the timeout (in milliseconds)
        """

        self._message = f'Timeout {timeout}ms exceeded waiting for navigation'
        super().__init__(self._message)

    @property
    def message(self) -> str:
        """
        Returns the error message.

        :return: the error message
        """

        return self._message

    def __str__(self) -> str:
        """
        Returns the string representation of the error.

        :return: the string representation of the error
        """

        return self._message
