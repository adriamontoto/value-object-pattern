"""
Test HttpUrlValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import HttpUrlValueObject


@mark.unit_testing
def test_http_url_value_object_happy_path() -> None:
    """
    Test HttpUrlValueObject value object happy path.
    """
    url = HttpUrlValueObject(value='http://example.com')

    assert type(url.value) is str
    assert url.scheme == 'http'


@mark.unit_testing
def test_http_url_value_object_invalid_scheme() -> None:
    """
    Test HttpUrlValueObject value object raises ValueError when scheme is not HTTP.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'HttpUrlValueObject value <<<https://example.com>>> scheme is not HTTP',
    ):
        HttpUrlValueObject(value='https://example.com')
