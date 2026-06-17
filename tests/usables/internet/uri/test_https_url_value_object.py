"""
Test HttpsUrlValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import HttpsUrlValueObject


@mark.unit_testing
def test_https_url_value_object_happy_path() -> None:
    """
    Test HttpsUrlValueObject value object happy path.
    """
    url = HttpsUrlValueObject(value='https://example.com')

    assert type(url.value) is str
    assert url.scheme == 'https'


@mark.unit_testing
def test_https_url_value_object_invalid_scheme() -> None:
    """
    Test HttpsUrlValueObject value object raises ValueError when scheme is not HTTPS.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'HttpsUrlValueObject value <<<http://example.com>>> scheme is not HTTPS',
    ):
        HttpsUrlValueObject(value='http://example.com')
