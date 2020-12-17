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


class BrowserPage:
    """Represents a page in the browser."""

    def __init__(self, index: int, url: str, title: str) -> None:
        """
        Creates a new page instance.

        :param index: the page index
        :param url: the page URL
        :param title: the page title
        """

        self._index = index
        self._url = url
        self._title = title

    @property
    def index(self) -> int:
        """
        Returns the index of the page.

        :return: the index of the page
        """

        return self._index

    @property
    def url(self) -> str:
        """
        Returns the URL of the page.

        :return: the URL of the page
        """

        return self._url

    @property
    def title(self) -> str:
        """
        Returns the title of the page.

        :return: the title of the page
        """

        return self._title

    def __str__(self) -> str:
        """
        Returns the string representation of the page.

        :return: the string representation of the page
        """

        return f'BrowserPage(index={self._index}, url={self._url}, title={self._title})'
