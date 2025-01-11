"""
Test value object representation method.
"""

from object_mother_pattern.mothers import (
    BooleanMother,
    BytesMother,
    DateMother,
    DatetimeMother,
    FloatMother,
    IntegerMother,
    StringDateMother,
    StringDatetimeMother,
    StringMother,
    StringUuidMother,
    UuidMother,
)
from pytest import mark

from value_object_pattern.usables import (
    BooleanValueObject,
    BytesValueObject,
    FloatValueObject,
    IntegerValueObject,
    StringValueObject,
)
from value_object_pattern.usables.dates import (
    DateValueObject,
    DatetimeValueObject,
    StringDateValueObject,
    StringDatetimeValueObject,
)
from value_object_pattern.usables.identifiers import StringUuidValueObject, UuidValueObject


@mark.unit_testing
def test_value_object_string_representation_method() -> None:
    """
    Test value object string representation method.
    """
    string_value = StringMother.create()
    string = StringValueObject(value=string_value)

    assert repr(string) == f'StringValueObject(value={string_value})'


@mark.unit_testing
def test_value_object_bytes_representation_method() -> None:
    """
    Test value object bytes representation method.
    """
    bytes_value = BytesMother.create()
    bytes_ = BytesValueObject(value=bytes_value)

    assert repr(bytes_) == f'BytesValueObject(value={bytes_value!s})'


@mark.unit_testing
def test_value_object_bool_representation_method() -> None:
    """
    Test value object bool representation method.
    """
    boolean_value = BooleanMother.create()
    boolean = BooleanValueObject(value=boolean_value)

    assert repr(boolean) == f'BooleanValueObject(value={boolean_value})'


@mark.unit_testing
def test_value_object_integer_representation_method() -> None:
    """
    Test value object integer representation method.
    """
    integer_value = IntegerMother.create()
    integer = IntegerValueObject(value=integer_value)

    assert repr(integer) == f'IntegerValueObject(value={integer_value})'


@mark.unit_testing
def test_value_object_float_representation_method() -> None:
    """
    Test value object float representation method.
    """
    float_value = FloatMother.create()
    float_ = FloatValueObject(value=float_value)

    assert repr(float_) == f'FloatValueObject(value={float_value})'


@mark.unit_testing
def test_value_object_date_representation_method() -> None:
    """
    Test value object date representation method.
    """
    date_value = DateMother.create()
    date = DateValueObject(value=date_value)

    assert repr(date) == f'DateValueObject(value={date_value})'


@mark.unit_testing
def test_value_object_string_date_representation_method() -> None:
    """
    Test value object string date representation method.
    """
    string_date_value = StringDateMother.create()
    string_date = StringDateValueObject(value=string_date_value)

    assert repr(string_date) == f'StringDateValueObject(value={string_date_value})'


@mark.unit_testing
def test_value_object_datetime_representation_method() -> None:
    """
    Test value object datetime representation method.
    """
    datetime_value = DatetimeMother.create()
    datetime = DatetimeValueObject(value=datetime_value)

    assert repr(datetime) == f'DatetimeValueObject(value={datetime_value})'


@mark.unit_testing
def test_value_object_string_datetime_representation_method() -> None:
    """
    Test value object string datetime representation method.
    """
    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetimeValueObject(value=string_datetime_value)

    assert repr(string_datetime) == f'StringDatetimeValueObject(value={string_datetime_value})'


@mark.unit_testing
def test_value_object_uuid_representation_method() -> None:
    """
    Test value object UUID representation method.
    """
    uuid_value = UuidMother.create()
    uuid = UuidValueObject(value=uuid_value)

    assert repr(uuid) == f'UuidValueObject(value={uuid_value})'


@mark.unit_testing
def test_value_object_string_uuid_representation_method() -> None:
    """
    Test value object string UUID representation method.
    """
    string_uuid_value = StringUuidMother.create()
    string_uuid = StringUuidValueObject(value=string_uuid_value)

    assert repr(string_uuid) == f'StringUuidValueObject(value={string_uuid_value})'
