"""
Test CountryTldValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world import CountryTldValueObject


@mark.unit_testing
def test_country_tld_value_object_happy_path() -> None:
    """
    Test CountryTldValueObject value object happy path.
    """
    tld = CountryTldValueObject(value='.ES')

    assert type(tld.value) is str
    assert tld.value == 'es'


@mark.unit_testing
def test_country_tld_value_object_conversions() -> None:
    """
    Test CountryTldValueObject value object conversions.
    """
    tld = CountryTldValueObject(value='.ES')

    assert tld.to_alpha2().value == 'ES'
    assert tld.to_alpha3().value == 'ESP'
    assert tld.to_numeric().value == 724
    assert tld.to_phone_code().value == '34'


@mark.unit_testing
def test_country_tld_value_object_invalid_value() -> None:
    """
    Test CountryTldValueObject value object raises ValueError when value is not a valid country TLD.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CountryTldValueObject value <<<invalid>>> is not a valid country TLD.',
    ):
        CountryTldValueObject(value='invalid')


@mark.unit_testing
def test_country_tld_value_object_without_phone_code_conversion() -> None:
    """
    Test CountryTldValueObject value object raises ValueError when TLD has no phone code conversion.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'CountryTldValueObject value <<<aq>>> has no conversion to a phone code.',
    ):
        CountryTldValueObject(value='.AQ').to_phone_code()
