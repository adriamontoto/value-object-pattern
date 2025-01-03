"""
Test value object hash method.
"""

from datetime import date, datetime
from uuid import UUID

from object_mother_pattern.mothers import (
    BoolMother,
    BytesMother,
    DateMother,
    DatetimeMother,
    FloatMother,
    IntegerMother,
    StringDateMother,
    StringDatetimeMother,
    StringMother,
    StringUUIDMother,
    UUIDMother,
)
from pytest import mark

from value_object_pattern import ValueObject


@mark.unit_testing
def test_value_object_string_hash_method() -> None:
    """
    Test value object string hash method.
    """

    class String(ValueObject[str]):
        pass

    string_value = StringMother.create()
    string = String(value=string_value)

    assert hash(string) == hash(string_value)


@mark.unit_testing
def test_value_object_bytes_hash_method() -> None:
    """
    Test value object bytes hash method.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value = BytesMother.create()
    bytes_ = Bytes(value=bytes_value)

    assert hash(bytes_) == hash(bytes_value)


@mark.unit_testing
def test_value_object_bool_hash_method() -> None:
    """
    Test value object bool hash method.
    """

    class Bool(ValueObject[bool]):
        pass

    bool_value = BoolMother.create()
    bool_ = Bool(value=bool_value)

    assert hash(bool_) == hash(bool_value)


@mark.unit_testing
def test_value_object_integer_hash_method() -> None:
    """
    Test value object integer hash method.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value = IntegerMother.create()
    integer = Integer(value=integer_value)

    assert hash(integer) == hash(integer_value)


@mark.unit_testing
def test_value_object_float_hash_method() -> None:
    """
    Test value object float hash method.
    """

    class Float(ValueObject[float]):
        pass

    float_value = FloatMother.create()
    float_ = Float(value=float_value)

    assert hash(float_) == hash(float_value)


@mark.unit_testing
def test_value_object_date_hash_method() -> None:
    """
    Test value object date hash method.
    """

    class Date(ValueObject[date]):
        pass

    date_value = DateMother.create()
    _date = Date(value=date_value)

    assert hash(_date) == hash(date_value)


@mark.unit_testing
def test_value_object_string_date_hash_method() -> None:
    """
    Test value object string date hash method.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value = StringDateMother.create()
    string_date = StringDate(value=string_date_value)

    assert hash(string_date) == hash(string_date_value)


@mark.unit_testing
def test_value_object_datetime_hash_method() -> None:
    """
    Test value object datetime hash method.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value = DatetimeMother.create()
    _datetime = Datetime(value=datetime_value)

    assert hash(_datetime) == hash(datetime_value)


@mark.unit_testing
def test_value_object_string_datetime_hash_method() -> None:
    """
    Test value object string datetime hash method.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetime(value=string_datetime_value)

    assert hash(string_datetime) == hash(string_datetime_value)


@mark.unit_testing
def test_value_object_uuid_hash_method() -> None:
    """
    Test value object uuid hash method.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value = UUIDMother.create()
    uuid = _UUID(value=uuid_value)

    assert hash(uuid) == hash(uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_hash_method() -> None:
    """
    Test value object string uuid hash method.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value = StringUUIDMother.create()
    string_uuid = StringUUID(value=string_uuid_value)

    assert hash(string_uuid) == hash(string_uuid_value)
