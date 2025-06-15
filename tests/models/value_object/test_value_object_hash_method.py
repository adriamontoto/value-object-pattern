"""
Test value object hash method.
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
def test_value_object_string_hash_method() -> None:
    """
    Test value object string hash method.
    """
    string_value = StringMother.create()
    string = StringValueObject(value=string_value)

    assert hash(string) == hash(string_value)


@mark.unit_testing
def test_value_object_bytes_hash_method() -> None:
    """
    Test value object bytes hash method.
    """
    bytes_value = BytesMother.create()
    bytes_ = BytesValueObject(value=bytes_value)

    assert hash(bytes_) == hash(bytes_value)


@mark.unit_testing
def test_value_object_bool_hash_method() -> None:
    """
    Test value object bool hash method.
    """
    boolean_value = BooleanMother.create()
    boolean = BooleanValueObject(value=boolean_value)

    assert hash(boolean) == hash(boolean_value)


@mark.unit_testing
def test_value_object_integer_hash_method() -> None:
    """
    Test value object integer hash method.
    """
    integer_value = IntegerMother.create()
    integer = IntegerValueObject(value=integer_value)

    assert hash(integer) == hash(integer_value)


@mark.unit_testing
def test_value_object_float_hash_method() -> None:
    """
    Test value object float hash method.
    """
    float_value = FloatMother.create()
    float_ = FloatValueObject(value=float_value)

    assert hash(float_) == hash(float_value)


@mark.unit_testing
def test_value_object_date_hash_method() -> None:
    """
    Test value object date hash method.
    """
    date_value = DateMother.create()
    date = DateValueObject(value=date_value)

    assert hash(date) == hash(date_value)


@mark.unit_testing
def test_value_object_string_date_hash_method() -> None:
    """
    Test value object string date hash method.
    """
    string_date_value = StringDateMother.create()
    string_date = StringDateValueObject(value=string_date_value)

    assert hash(string_date) == hash(string_date_value)


@mark.unit_testing
def test_value_object_datetime_hash_method() -> None:
    """
    Test value object datetime hash method.
    """
    datetime_value = DatetimeMother.create()
    datetime = DatetimeValueObject(value=datetime_value)

    assert hash(datetime) == hash(datetime_value)


@mark.unit_testing
def test_value_object_string_datetime_hash_method() -> None:
    """
    Test value object string datetime hash method.
    """
    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetimeValueObject(value=string_datetime_value)

    assert hash(string_datetime) == hash(string_datetime_value)


@mark.unit_testing
def test_value_object_uuid_hash_method() -> None:
    """
    Test value object uuid hash method.
    """
    uuid_value = UuidMother.create()
    uuid = UuidValueObject(value=uuid_value)

    assert hash(uuid) == hash(uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_hash_method() -> None:
    """
    Test value object string uuid hash method.
    """
    string_uuid_value = StringUuidMother.create()
    string_uuid = StringUuidValueObject(value=string_uuid_value)

    assert hash(string_uuid) == hash(string_uuid_value)
