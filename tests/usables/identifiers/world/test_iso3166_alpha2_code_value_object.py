"""
Test Iso3166Alpha2CodeValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject


@mark.unit_testing
def test_iso3166_alpha2_code_value_object_happy_path() -> None:
    """
    Test Iso3166Alpha2CodeValueObject value object happy path.
    """
    country_code = Iso3166Alpha2CodeValueObject(value='es')

    assert type(country_code.value) is str
    assert country_code.value == 'ES'


@mark.unit_testing
def test_iso3166_alpha2_code_value_object_conversions() -> None:
    """
    Test Iso3166Alpha2CodeValueObject value object conversions.
    """
    country_code = Iso3166Alpha2CodeValueObject(value='es')

    assert country_code.to_alpha3().value == 'ESP'
    assert country_code.to_numeric().value == 724
    assert country_code.to_phone_code().value == '34'
    assert country_code.to_tld().value == 'es'


@mark.unit_testing
def test_iso3166_alpha2_code_value_object_invalid_value() -> None:
    """
    Test Iso3166Alpha2CodeValueObject value object raises ValueError when value is not a valid ISO alpha-2 code.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Iso3166Alpha2CodeValueObject value <<<ZZ>>> is not a valid ISO 3166-1 alpha-2 country code.',
    ):
        Iso3166Alpha2CodeValueObject(value='ZZ')


@mark.unit_testing
def test_iso3166_alpha2_code_value_object_without_phone_code_conversion() -> None:
    """
    Test Iso3166Alpha2CodeValueObject value object raises ValueError when code has no phone code conversion.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Iso3166Alpha2CodeValueObject value <<<AQ>>> has no conversion to a phone code.',
    ):
        Iso3166Alpha2CodeValueObject(value='AQ').to_phone_code()
