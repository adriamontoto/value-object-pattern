"""
Test value object string method.
"""

from object_mother_pattern import (
    BooleanMother,
    BytesMother,
    DateMother,
    DatetimeMother,
    FloatMother,
    IntegerMother,
    StringDateMother,
    StringDatetimeMother,
    StringMother,
)
from object_mother_pattern.mothers.identifiers import StringUuidMother, UuidMother
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
def test_value_object_string_string_method() -> None:
    """
    Test value object string string method.
    """
    string_value = StringMother.create()
    string = StringValueObject(value=string_value)

    assert str(string) == str(string_value)


@mark.unit_testing
def test_value_object_bytes_string_method() -> None:
    """
    Test value object bytes string method.
    """
    bytes_value = BytesMother.create()
    bytes_ = BytesValueObject(value=bytes_value)

    assert str(bytes_) == str(bytes_value)


@mark.unit_testing
def test_value_object_bool_string_method() -> None:
    """
    Test value object bool string method.
    """
    boolean_value = BooleanMother.create()
    boolean = BooleanValueObject(value=boolean_value)

    assert str(boolean) == str(boolean_value)


@mark.unit_testing
def test_value_object_integer_string_method() -> None:
    """
    Test value object integer string method.
    """
    integer_value = IntegerMother.create()
    integer = IntegerValueObject(value=integer_value)

    assert str(integer) == str(integer_value)


@mark.unit_testing
def test_value_object_float_string_method() -> None:
    """
    Test value object float string method.
    """
    float_value = FloatMother.create()
    float_ = FloatValueObject(value=float_value)

    assert str(float_) == str(float_value)


@mark.unit_testing
def test_value_object_date_string_method() -> None:
    """
    Test value object date string method.
    """
    date_value = DateMother.create()
    date = DateValueObject(value=date_value)

    assert str(date) == str(date_value)


@mark.unit_testing
def test_value_object_string_date_string_method() -> None:
    """
    Test value object string date string method.
    """
    string_date_value = StringDateMother.create()
    string_date = StringDateValueObject(value=string_date_value)

    assert str(string_date) == str(string_date_value)


@mark.unit_testing
def test_value_object_datetime_string_method() -> None:
    """
    Test value object datetime string method.
    """
    datetime_value = DatetimeMother.create()
    datetime = DatetimeValueObject(value=datetime_value)

    assert str(datetime) == str(datetime_value)


@mark.unit_testing
def test_value_object_string_datetime_string_method() -> None:
    """
    Test value object string datetime string method.
    """
    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetimeValueObject(value=string_datetime_value)

    assert str(string_datetime) == str(string_datetime_value)


@mark.unit_testing
def test_value_object_uuid_string_method() -> None:
    """
    Test value object uuid string method.
    """
    uuid_value = UuidMother.create()
    uuid = UuidValueObject(value=uuid_value)

    assert str(uuid) == str(uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_string_method() -> None:
    """
    Test value object string uuid string method.
    """
    string_uuid_value = StringUuidMother.create()
    string_uuid = StringUuidValueObject(value=string_uuid_value)

    assert str(string_uuid) == str(string_uuid_value)
