"""
Test Iso3166NumericCodeValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world import Iso3166NumericCodeValueObject


@mark.unit_testing
def test_iso3166_numeric_code_value_object_happy_path() -> None:
    """
    Test Iso3166NumericCodeValueObject value object happy path.
    """
    country_code = Iso3166NumericCodeValueObject(value=724)

    assert type(country_code.value) is int
    assert country_code.value == 724


@mark.unit_testing
def test_iso3166_numeric_code_value_object_conversions() -> None:
    """
    Test Iso3166NumericCodeValueObject value object conversions.
    """
    country_code = Iso3166NumericCodeValueObject(value=724)

    assert country_code.to_alpha2_code().value == 'ES'
    assert country_code.to_alpha3_code().value == 'ESP'
    assert country_code.to_phone_code().value == '34'
    assert country_code.to_tld().value == 'es'


@mark.unit_testing
def test_iso3166_numeric_code_value_object_invalid_value() -> None:
    """
    Test Iso3166NumericCodeValueObject value object raises ValueError when value is not a valid ISO numeric code.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Iso3166NumericCodeValueObject value <<<999>>> is not a valid ISO 3166-1 numeric country code.',
    ):
        Iso3166NumericCodeValueObject(value=999)


@mark.unit_testing
def test_iso3166_numeric_code_value_object_without_phone_code_conversion() -> None:
    """
    Test Iso3166NumericCodeValueObject value object raises ValueError when code has no phone code conversion.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Iso3166NumericCodeValueObject value <<<10>>> has no conversion to a phone code.',
    ):
        Iso3166NumericCodeValueObject(value=10).to_phone_code()
