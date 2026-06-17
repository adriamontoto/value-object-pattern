"""
Test HttpHttpsUrlValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import HttpHttpsUrlValueObject


@mark.unit_testing
def test_http_https_url_value_object_accepts_http_url() -> None:
    """
    Test HttpHttpsUrlValueObject value object accepts HTTP URLs.
    """
    assert HttpHttpsUrlValueObject(value='http://example.com').scheme == 'http'


@mark.unit_testing
def test_http_https_url_value_object_accepts_https_url() -> None:
    """
    Test HttpHttpsUrlValueObject value object accepts HTTPS URLs.
    """
    assert HttpHttpsUrlValueObject(value='https://example.com').scheme == 'https'


@mark.unit_testing
def test_http_https_url_value_object_invalid_scheme() -> None:
    """
    Test HttpHttpsUrlValueObject value object raises ValueError when scheme is not HTTP or HTTPS.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'HttpHttpsUrlValueObject value <<<ftp://example.com>>> scheme is not HTTP or HTTPS',
    ):
        HttpHttpsUrlValueObject(value='ftp://example.com')
