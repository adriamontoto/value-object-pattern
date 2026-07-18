"""
Test UrlValueObject value object.
"""

from typing import Any

from pytest import MonkeyPatch, mark, raises as assert_raises

from value_object_pattern.usables.internet import UrlValueObject
from value_object_pattern.usables.internet.uri import url_value_object as url_module
from value_object_pattern.usables.internet.uri.url_value_object import join_url, split_netloc, split_url


@mark.unit_testing
def test_join_url_with_all_parts() -> None:
    """
    Test join_url helper with all URL parts.
    """
    assert join_url('https', 'example.com', 443, 'user:pass', 'path', 'a=1', 'fragment') == (
        'https://user:pass@example.com:443/path?a=1#fragment'
    )


@mark.unit_testing
def test_join_url_with_required_parts() -> None:
    """
    Test join_url helper with required URL parts.
    """
    assert join_url('https', 'example.com', None, None, '', '', '') == 'https://example.com'


@mark.unit_testing
def test_join_url_with_ipv6_host() -> None:
    """
    Test join_url helper encloses an IPv6 host in brackets.
    """
    assert join_url('http', '::1', 8000, None, '', '', '') == 'http://[::1]:8000'


@mark.unit_testing
def test_split_url() -> None:
    """
    Test split_url helper.
    """
    scheme, netloc, path, query, fragment = split_url(value='https://example.com/path?a=1#fragment')

    assert scheme == 'https'
    assert netloc == 'example.com'
    assert path == '/path'
    assert query == 'a=1'
    assert fragment == 'fragment'


@mark.unit_testing
def test_split_netloc_with_user_information_and_port() -> None:
    """
    Test split_netloc helper with user information and port.
    """
    assert split_netloc(value='user:pass@example.com:443') == ('user:pass', 'example.com', 443)


@mark.unit_testing
def test_split_netloc_with_ipv6_address() -> None:
    """
    Test split_netloc helper with a bracketed IPv6 address and port.
    """
    assert split_netloc(value='[::1]:8000') == (None, '::1', 8000)


@mark.unit_testing
def test_split_netloc_rejects_unbracketed_ipv6_address() -> None:
    """
    Test split_netloc helper rejects an unbracketed IPv6 address.
    """
    with assert_raises(expected_exception=ValueError, match='IPv6 URL hosts must be enclosed in brackets.'):
        split_netloc(value='2001:db8::1')


@mark.unit_testing
def test_url_value_object_happy_path() -> None:
    """
    Test UrlValueObject value object happy path.
    """
    url = UrlValueObject(value='HTTPS://User:Pass@Example.COM:443/path/to?q=1#Frag')

    assert type(url.value) is str
    assert url.value == 'https://User:Pass@example.com:443/path/to?q=1#Frag'
    assert url.scheme == 'https'
    assert url.netloc == 'User:Pass@example.com:443'
    assert url.path == '/path/to'
    assert url.query == 'q=1'
    assert url.fragment == 'Frag'


@mark.unit_testing
def test_url_value_object_empty_optional_parts() -> None:
    """
    Test UrlValueObject returns None for empty optional URL parts.
    """
    url = UrlValueObject(value='https://example.com')

    assert url.path is None
    assert url.query is None
    assert url.fragment is None


@mark.unit_testing
def test_url_value_object_accepts_loopback_hosts() -> None:
    """
    Test UrlValueObject accepts localhost, IPv4 loopback, and bracketed IPv6 loopback hosts.
    """
    assert UrlValueObject(value='http://LOCALHOST:8000').value == 'http://localhost:8000'
    assert UrlValueObject(value='http://127.0.0.1:8000').value == 'http://127.0.0.1:8000'
    assert UrlValueObject(value='http://[::1]').value == 'http://[::1]'
    assert UrlValueObject(value='http://[::1]:8000').value == 'http://[::1]:8000'


@mark.unit_testing
def test_url_value_object_rejects_unbracketed_ipv6_host() -> None:
    """
    Test UrlValueObject rejects an unbracketed IPv6 host.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<http://::1>>> is not a valid url.',
    ):
        UrlValueObject(value='http://::1')


@mark.unit_testing
def test_url_value_object_invalid_url() -> None:
    """
    Test UrlValueObject value object raises ValueError when URL cannot be parsed.
    """
    with assert_raises(
        expected_exception=ValueError, match=r'UrlValueObject value <<<http://\[::1>>> is not a valid url.'
    ):
        UrlValueObject(value='http://[::1')


@mark.unit_testing
def test_url_value_object_invalid_scheme() -> None:
    """
    Test UrlValueObject value object raises ValueError when scheme is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<1https://example.com>>> contains an invalid scheme <<<>>>.',
    ):
        UrlValueObject(value='1https://example.com')


@mark.unit_testing
def test_url_value_object_invalid_user_information() -> None:
    """
    Test UrlValueObject value object raises ValueError when user information is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://bad user@example.com>>> has not a valid user information <<<bad user>>>.',  # noqa: E501
    ):
        UrlValueObject(value='https://bad user@example.com')


@mark.unit_testing
def test_url_value_object_invalid_host() -> None:
    """
    Test UrlValueObject value object raises ValueError when host is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://not_a_domain>>> has not a valid host <<<not_a_domain>>>.',
    ):
        UrlValueObject(value='https://not_a_domain')


@mark.unit_testing
def test_url_value_object_invalid_port() -> None:
    """
    Test UrlValueObject value object raises ValueError when port is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://example.com:70000>>> has not a valid port <<<70000>>>.',
    ):
        UrlValueObject(value='https://example.com:70000')


@mark.unit_testing
def test_url_value_object_invalid_path() -> None:
    """
    Test UrlValueObject value object raises ValueError when path is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://example.com/<bad>>> has not a valid path <<</<bad>>>.',
    ):
        UrlValueObject(value='https://example.com/<bad')


@mark.unit_testing
def test_url_value_object_invalid_query() -> None:
    """
    Test UrlValueObject value object raises ValueError when query is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://example.com/\?q=<bad>>> has not a valid query <<<q=<bad>>>.',
    ):
        UrlValueObject(value='https://example.com/?q=<bad')


@mark.unit_testing
def test_url_value_object_invalid_fragment() -> None:
    """
    Test UrlValueObject value object raises ValueError when fragment is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://example.com/#<bad>>> has not a valid fragment <<<<bad>>>.',
    ):
        UrlValueObject(value='https://example.com/#<bad')


@mark.unit_testing
def test_url_value_object_empty_url_validation() -> None:
    """
    Test UrlValueObject defensive validation branch for empty URL values.
    """
    url: Any = UrlValueObject(value='https://example.com')

    with assert_raises(expected_exception=ValueError, match=r'UrlValueObject value <<<>>> is not a valid url.'):
        url._validate_url(value='')


@mark.unit_testing
def test_url_value_object_invalid_query_parser(monkeypatch: MonkeyPatch) -> None:
    """
    Test UrlValueObject defensive query parser error branch.
    """
    url: Any = UrlValueObject(value='https://example.com')

    monkeypatch.setattr(url_module, 'parse_qs', lambda qs: (_ for _ in ()).throw(ValueError))

    with assert_raises(
        expected_exception=ValueError,
        match=r'UrlValueObject value <<<https://example.com/\?q=1>>> has not a valid query <<<q=1>>>.',
    ):
        url._validate_url_query(value='https://example.com/?q=1')
