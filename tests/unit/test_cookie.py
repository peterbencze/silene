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

import pytest

from silene.cookie import Cookie

cookie = Cookie('cookie_name', 'cookie_value', domain='example.com', path='/', expires=-1, session=True)

cookie_dict = {
    'name': 'cookie_name',
    'value': 'cookie_value',
    'domain': 'example.com',
    'path': '/',
    'expires': -1,
    'session': True
}


def test_name_should_return_cookie_name() -> None:
    assert cookie.name == 'cookie_name'


def test_value_should_return_cookie_value() -> None:
    assert cookie.value == 'cookie_value'


def test_domain_should_return_cookie_domain() -> None:
    assert cookie.domain == 'example.com'


def test_path_should_return_cookie_path() -> None:
    assert cookie.path == '/'


def test_expires_should_return_cookie_lifetime_timestamp() -> None:
    assert cookie.expires == -1


def test_http_only_should_return_cookie_http_only_flag_value() -> None:
    assert cookie.http_only is None


def test_secure_should_return_cookie_secure_flag_value() -> None:
    assert cookie.secure is None


def test_session_should_return_cookie_session_flag_value() -> None:
    assert cookie.session is True


def test_same_site_should_return_cookie_same_site_value() -> None:
    assert cookie.same_site is None


def test_as_dict_should_return_cookie_as_a_dictionary() -> None:
    assert cookie.as_dict() == cookie_dict


def test_from_dict_should_return_cookie_object_when_dictionary_contains_required_items() -> None:
    result = Cookie.from_dict(cookie_dict)

    assert result.name == cookie_dict['name']
    assert result.value == cookie_dict['value']
    assert result.domain == cookie_dict['domain']
    assert result.path == cookie_dict['path']
    assert result.expires == cookie_dict['expires']
    assert result.http_only is None
    assert result.secure is None
    assert result.session is cookie_dict['session']
    assert result.same_site is None


def test_from_dict_should_raise_value_error_when_dictionary_is_missing_required_key() -> None:
    with pytest.raises(ValueError) as exc_info:
        Cookie.from_dict({'value': 'cookie_value'})

    assert str(exc_info.value) == f'Cookie dictionary is missing required key "name"'

    with pytest.raises(ValueError) as exc_info:
        Cookie.from_dict({'name': 'cookie_name'})

    assert str(exc_info.value) == f'Cookie dictionary is missing required key "value"'
