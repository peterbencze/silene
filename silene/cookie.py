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
    """Represents an HTTP cookie."""

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
        """
        Creates a new cookie instance.

        :param name: the name of the cookie
        :param value: the value of the cookie
        :param domain: host to which the cookie will be sent (optional)
        :param path: a path that must exist in the requested URL, or the browser will not send the Cookie header
                     (optional)
        :param expires: the maximum lifetime of the cookie as a timestamp (optional)
        :param http_only: forbids JavaScript from accessing the cookie (optional)
        :param secure: cookie is only sent to the server when a request is made with the https scheme (optional)
        :param session: cookie should be removed when the client shuts down (optional)
        :param same_site: controls whether a cookie is sent with cross-origin requests, possible values are Strict,
                          Lax and None (optional)
        """

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
        """
        Returns the cookie name.

        :return: the cookie name
        """

        return self._name

    @property
    def value(self) -> str:
        """
        Returns the cookie value.

        :return: the cookie value
        """

        return self._value

    @property
    def domain(self) -> Optional[str]:
        """
        Returns the cookie domain.

        :return: the cookie domain if specified, None otherwise
        """

        return self._domain

    @property
    def path(self) -> Optional[str]:
        """
        Returns the cookie path.

        :return: the cookie path if specified, None otherwise
        """

        return self._path

    @property
    def expires(self) -> Optional[int]:
        """
        Returns the cookie expiration date.

        :return: the cookie expiration date if specified, None otherwise
        """

        return self._expires

    @property
    def http_only(self) -> Optional[bool]:
        """
        Returns a value indicating whether the cookie is http-only.

        :return: True if cookie is http-only, False if it isn't, or None if unspecified
        """

        return self._http_only

    @property
    def secure(self) -> Optional[bool]:
        """
        Returns a value indicating whether the cookie is secure.

        :return: True if cookie is secure, False if it isn't, or None if unspecified
        """

        return self._secure

    @property
    def session(self) -> Optional[bool]:
        """
        Returns a value indicating whether this is a session cookie or not

        :return: True if it is a session cookie, False if it isn't, or None if unspecified
        """

        return self._session

    @property
    def same_site(self) -> Optional[str]:
        """
        Returns the cookie SameSite type.

        :return: the cookie SameSite type if specified, None otherwise
        """

        return self._same_site

    def as_dict(self) -> Dict[str, Union[str, int, bool]]:
        """
        Returns the cookie as a dictionary.
        The dictionary will only contain specified attributes.

        :return: the cookie as a dictionary
        """

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
        """
        Creates a cookie object from a dictionary that contains the attributes of a cookie.

        :param cookie_dict: the cookie represented as a dictionary
        :return: a cookie object created from the given dictionary
        """

        try:
            return Cookie(cookie_dict['name'], cookie_dict['value'], cookie_dict.get('domain'), cookie_dict.get('path'),
                          cookie_dict.get('expires'), cookie_dict.get('httpOnly'), cookie_dict.get('secure'),
                          cookie_dict.get('session'), cookie_dict.get('sameSite'))
        except KeyError as error:
            raise ValueError(f'Cookie dictionary is missing required key "{error.args[0]}"')

    def __str__(self) -> str:
        """
        Returns the string representation of the cookie.

        :return: the string representation of the cookie
        """

        return f'Cookie(name={self._name}, value={self._value}, domain={self._domain}, path={self._path}, ' \
               f'expires={self._expires}, http_only={self._http_only}, secure={self._secure}, ' \
               f'session={self._session}, same_site={self._same_site})'
