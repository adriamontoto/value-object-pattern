"""
Test value object string method.
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
def test_value_object_string_string_method() -> None:
    """
    Test value object string string method.
    """

    class String(ValueObject[str]):
        pass

    string_value = StringMother.create()
    string = String(value=string_value)

    assert str(string) == str(string_value)


@mark.unit_testing
def test_value_object_bytes_string_method() -> None:
    """
    Test value object bytes string method.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value = BytesMother.create()
    bytes_ = Bytes(value=bytes_value)

    assert str(bytes_) == str(bytes_value)


@mark.unit_testing
def test_value_object_bool_string_method() -> None:
    """
    Test value object bool string method.
    """

    class Bool(ValueObject[bool]):
        pass

    bool_value = BoolMother.create()
    bool_ = Bool(value=bool_value)

    assert str(bool_) == str(bool_value)


@mark.unit_testing
def test_value_object_integer_string_method() -> None:
    """
    Test value object integer string method.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value = IntegerMother.create()
    integer = Integer(value=integer_value)

    assert str(integer) == str(integer_value)


@mark.unit_testing
def test_value_object_float_string_method() -> None:
    """
    Test value object float string method.
    """

    class Float(ValueObject[float]):
        pass

    float_value = FloatMother.create()
    float_ = Float(value=float_value)

    assert str(float_) == str(float_value)


@mark.unit_testing
def test_value_object_date_string_method() -> None:
    """
    Test value object date string method.
    """

    class Date(ValueObject[date]):
        pass

    date_value = DateMother.create()
    _date = Date(value=date_value)

    assert str(_date) == str(date_value)


@mark.unit_testing
def test_value_object_string_date_string_method() -> None:
    """
    Test value object string date string method.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value = StringDateMother.create()
    string_date = StringDate(value=string_date_value)

    assert str(string_date) == str(string_date_value)


@mark.unit_testing
def test_value_object_datetime_string_method() -> None:
    """
    Test value object datetime string method.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value = DatetimeMother.create()
    _datetime = Datetime(value=datetime_value)

    assert str(_datetime) == str(datetime_value)


@mark.unit_testing
def test_value_object_string_datetime_string_method() -> None:
    """
    Test value object string datetime string method.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetime(value=string_datetime_value)

    assert str(string_datetime) == str(string_datetime_value)


@mark.unit_testing
def test_value_object_uuid_string_method() -> None:
    """
    Test value object uuid string method.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value = UUIDMother.create()
    uuid = _UUID(value=uuid_value)

    assert str(uuid) == str(uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_string_method() -> None:
    """
    Test value object string uuid string method.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value = StringUUIDMother.create()
    string_uuid = StringUUID(value=string_uuid_value)

    assert str(string_uuid) == str(string_uuid_value)
