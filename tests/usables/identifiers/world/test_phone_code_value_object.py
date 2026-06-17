"""
Test PhoneCodeValueObject value object.
"""

from pytest import MonkeyPatch, mark, raises as assert_raises

from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject


@mark.unit_testing
def test_phone_code_value_object_happy_path() -> None:
    """
    Test PhoneCodeValueObject value object happy path.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    assert type(phone_code.value) is str
    assert phone_code.value == '34'


@mark.unit_testing
def test_phone_code_value_object_conversions() -> None:
    """
    Test PhoneCodeValueObject value object conversions.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    assert phone_code.to_alpha2().value == 'ES'
    assert phone_code.to_alpha3().value == 'ESP'
    assert phone_code.to_numeric().value == 724
    assert phone_code.to_tld().value == 'es'


@mark.unit_testing
def test_phone_code_value_object_invalid_value() -> None:
    """
    Test PhoneCodeValueObject value object raises ValueError when value is not a valid phone code.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneCodeValueObject value <<<999999>>> is not a valid phone code.',
    ):
        PhoneCodeValueObject(value='999999')


@mark.unit_testing
def test_phone_code_value_object_without_alpha2_conversion(monkeypatch: MonkeyPatch) -> None:
    """
    Test PhoneCodeValueObject value object raises ValueError when phone code has no alpha-2 conversion.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    monkeypatch.setattr(
        'value_object_pattern.usables.identifiers.world.phone_code_value_object.get_iso3166_alpha2_to_phone_code_mapping',
        lambda: ({}, {}),
    )

    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneCodeValueObject value <<<34>>> has no conversion to ISO 3166-1 alpha-2 code.',
    ):
        phone_code.to_alpha2()


@mark.unit_testing
def test_phone_code_value_object_without_alpha3_conversion(monkeypatch: MonkeyPatch) -> None:
    """
    Test PhoneCodeValueObject value object raises ValueError when phone code has no alpha-3 conversion.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    monkeypatch.setattr(
        'value_object_pattern.usables.identifiers.world.phone_code_value_object.get_iso3166_alpha2_to_phone_code_mapping',
        lambda: ({}, {}),
    )

    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneCodeValueObject value <<<34>>> has no conversion to ISO 3166-1 alpha-2 code.',
    ):
        phone_code.to_alpha3()


@mark.unit_testing
def test_phone_code_value_object_without_numeric_conversion(monkeypatch: MonkeyPatch) -> None:
    """
    Test PhoneCodeValueObject value object raises ValueError when phone code has no numeric conversion.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    monkeypatch.setattr(
        'value_object_pattern.usables.identifiers.world.phone_code_value_object.get_iso3166_alpha2_to_phone_code_mapping',
        lambda: ({}, {}),
    )

    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneCodeValueObject value <<<34>>> has no conversion to ISO 3166-1 alpha-2 code.',
    ):
        phone_code.to_numeric()


@mark.unit_testing
def test_phone_code_value_object_without_tld_conversion(monkeypatch: MonkeyPatch) -> None:
    """
    Test PhoneCodeValueObject value object raises ValueError when phone code has no TLD conversion.
    """
    phone_code = PhoneCodeValueObject(value='+34')

    monkeypatch.setattr(
        'value_object_pattern.usables.identifiers.world.phone_code_value_object.get_iso3166_alpha2_to_phone_code_mapping',
        lambda: ({}, {}),
    )

    with assert_raises(
        expected_exception=ValueError,
        match=r'PhoneCodeValueObject value <<<34>>> has no conversion to ISO 3166-1 alpha-2 code.',
    ):
        phone_code.to_tld()
