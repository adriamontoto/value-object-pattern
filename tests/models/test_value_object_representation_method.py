"""
Test value object representation method.
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
def test_value_object_string_representation_method() -> None:
    """
    Test value object string representation method.
    """

    class String(ValueObject[str]):
        value: str

    string_value = StringMother.create()
    string = String(value=string_value)

    assert repr(string) == f'String(value={string_value})'


@mark.unit_testing
def test_value_object_bytes_representation_method() -> None:
    """
    Test value object bytes representation method.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value = BytesMother.create()
    bytes_ = Bytes(value=bytes_value)

    assert repr(bytes_) == f'Bytes(value={bytes_value!s})'


@mark.unit_testing
def test_value_object_bool_representation_method() -> None:
    """
    Test value object bool representation method.
    """

    class Bool(ValueObject[bool]):
        pass

    bool_value = BoolMother.create()
    bool_ = Bool(value=bool_value)

    assert repr(bool_) == f'Bool(value={bool_value})'


@mark.unit_testing
def test_value_object_integer_representation_method() -> None:
    """
    Test value object integer representation method.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value = IntegerMother.create()
    integer = Integer(value=integer_value)

    assert repr(integer) == f'Integer(value={integer_value})'


@mark.unit_testing
def test_value_object_float_representation_method() -> None:
    """
    Test value object float representation method.
    """

    class Float(ValueObject[float]):
        pass

    float_value = FloatMother.create()
    float_ = Float(value=float_value)

    assert repr(float_) == f'Float(value={float_value})'


@mark.unit_testing
def test_value_object_date_representation_method() -> None:
    """
    Test value object date representation method.
    """

    class Date(ValueObject[date]):
        pass

    date_value = DateMother.create()
    _date = Date(value=date_value)

    assert repr(_date) == f'Date(value={date_value})'


@mark.unit_testing
def test_value_object_string_date_representation_method() -> None:
    """
    Test value object string date representation method.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value = StringDateMother.create()
    string_date = StringDate(value=string_date_value)

    assert repr(string_date) == f'StringDate(value={string_date_value})'


@mark.unit_testing
def test_value_object_datetime_representation_method() -> None:
    """
    Test value object datetime representation method.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value = DatetimeMother.create()
    _datetime = Datetime(value=datetime_value)

    assert repr(_datetime) == f'Datetime(value={datetime_value})'


@mark.unit_testing
def test_value_object_string_datetime_representation_method() -> None:
    """
    Test value object string datetime representation method.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetime(value=string_datetime_value)

    assert repr(string_datetime) == f'StringDatetime(value={string_datetime_value})'


@mark.unit_testing
def test_value_object_uuid_representation_method() -> None:
    """
    Test value object UUID representation method.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value = UUIDMother.create()
    uuid_ = _UUID(value=uuid_value)

    assert repr(uuid_) == f'_UUID(value={uuid_value})'


@mark.unit_testing
def test_value_object_string_uuid_representation_method() -> None:
    """
    Test value object string UUID representation method.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value = StringUUIDMother.create()
    string_uuid = StringUUID(value=string_uuid_value)

    assert repr(string_uuid) == f'StringUUID(value={string_uuid_value})'
