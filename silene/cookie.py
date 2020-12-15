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

from typing import Dict, Union, Optional


class Cookie:
    def __init__(self,
                 name: str,
                 value: str,
                 domain: Optional[str] = None,
                 path: Optional[str] = None,
                 expires: Optional[int] = None,
                 http_only: Optional[bool] = None,
                 secure: Optional[bool] = None,
                 session: Optional[bool] = None,
                 same_site: Optional[str] = None):
        self._name = name
        self._value = value
        self._domain = domain
        self._path = path
        self._expires = expires
        self._http_only = http_only
        self._secure = secure
        self._session = session
        self._same_site = same_site

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    @property
    def domain(self) -> Optional[str]:
        return self._domain

    @property
    def path(self) -> Optional[str]:
        return self._path

    @property
    def expires(self) -> Optional[int]:
        return self._expires

    @property
    def http_only(self) -> Optional[bool]:
        return self._http_only

    @property
    def secure(self) -> Optional[bool]:
        return self._secure

    @property
    def session(self) -> Optional[bool]:
        return self._session

    @property
    def same_site(self) -> Optional[str]:
        return self._same_site

    def as_dict(self) -> Dict[str, Union[str, int, bool]]:
        cookie_dict = {'name': self._name, 'value': self._value}

        if self._domain is not None:
            cookie_dict['domain'] = self._domain
        if self._path is not None:
            cookie_dict['path'] = self._path
        if self._secure is not None:
            cookie_dict['secure'] = self._secure
        if self._expires is not None:
            cookie_dict['expires'] = self._expires
        if self._http_only is not None:
            cookie_dict['httpOnly'] = self._http_only
        if self._secure is not None:
            cookie_dict['secure'] = self._secure
        if self._session is not None:
            cookie_dict['session'] = self._session
        if self._same_site is not None:
            cookie_dict['sameSite'] = self._same_site

        return cookie_dict

    @staticmethod
    def from_dict(cookie_dict: Dict[str, Union[str, int, bool]]) -> 'Cookie':
        try:
            return Cookie(cookie_dict['name'], cookie_dict['value'], cookie_dict.get('domain'), cookie_dict.get('path'),
                          cookie_dict.get('expires'), cookie_dict.get('httpOnly'), cookie_dict.get('secure'),
                          cookie_dict.get('session'), cookie_dict.get('sameSite'))
        except KeyError as error:
            raise ValueError(f'Cookie dictionary is missing required key "{error.args[0]}"')
