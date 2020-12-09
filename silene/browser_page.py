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
    def __init__(self, index: int, url: str, title: str) -> None:
        self._index = index
        self._url = url
        self._title = title

    @property
    def index(self) -> int:
        return self._index

    @property
    def url(self) -> str:
        return self._url

    @property
    def title(self) -> str:
        return self._title

    def __str__(self) -> str:
        return f'BrowserPage(index={self._index}, url={self._url}, title={self._title})'
