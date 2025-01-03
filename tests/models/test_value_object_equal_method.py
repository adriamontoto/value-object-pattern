"""
Test value object equal method.
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
def test_value_object_string_equal_method() -> None:
    """
    Test value object string equal method.
    """

    class String(ValueObject[str]):
        pass

    string_value = StringMother.create()

    assert String(value=string_value) == String(value=string_value)


@mark.unit_testing
def test_value_object_string_equal_method_with_different_values() -> None:
    """
    Test value object string equal method with different values.
    """

    class String(ValueObject[str]):
        pass

    string_value_a = StringMother.create()
    string_value_b = StringMother.create()

    assert String(value=string_value_a) != String(value=string_value_b)


@mark.unit_testing
def test_value_object_string_equal_method_different_types() -> None:
    """
    Test value object string equal method with different types.
    """

    class String(ValueObject[str]):
        pass

    string_value = StringMother.create()

    assert String(value=string_value) != string_value


@mark.unit_testing
def test_value_object_bytes_equal_method() -> None:
    """
    Test value object bytes equal method.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value = BytesMother.create()

    assert Bytes(value=bytes_value) == Bytes(value=bytes_value)


@mark.unit_testing
def test_value_object_bytes_equal_method_with_different_values() -> None:
    """
    Test value object bytes equal method with different values.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value_a = BytesMother.create()
    bytes_value_b = BytesMother.create()

    assert Bytes(value=bytes_value_a) != Bytes(value=bytes_value_b)


@mark.unit_testing
def test_value_object_bytes_equal_method_different_types() -> None:
    """
    Test value object bytes equal method with different types.
    """

    class Bytes(ValueObject[bytes]):
        pass

    bytes_value = BytesMother.create()

    assert Bytes(value=bytes_value) != bytes_value


@mark.unit_testing
def test_value_object_bool_equal_method() -> None:
    """
    Test value object bool equal method.
    """

    class Bool(ValueObject[bool]):
        pass

    bool_value = BoolMother.create()

    assert Bool(value=bool_value) == Bool(value=bool_value)


@mark.unit_testing
def test_value_object_bool_equal_method_with_different_values() -> None:
    """
    Test value object bool equal method with different values.
    """

    class Bool(ValueObject[bool]):
        pass

    assert Bool(value=True) != Bool(value=False)


@mark.unit_testing
def test_value_object_bool_equal_method_different_types() -> None:
    """
    Test value object bool equal method with different types.
    """

    class Bool(ValueObject[bool]):
        pass

    bool_value = BoolMother.create()

    assert Bool(value=bool_value) != bool_value


@mark.unit_testing
def test_value_object_integer_equal_method() -> None:
    """
    Test value object integer equal method.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value = IntegerMother.create()

    assert Integer(value=integer_value) == Integer(value=integer_value)


@mark.unit_testing
def test_value_object_integer_equal_method_with_different_values() -> None:
    """
    Test value object integer equal method with different values.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value_a = IntegerMother.create()
    integer_value_b = IntegerMother.create()

    assert Integer(value=integer_value_a) != Integer(value=integer_value_b)


@mark.unit_testing
def test_value_object_integer_equal_method_different_types() -> None:
    """
    Test value object integer equal method with different types.
    """

    class Integer(ValueObject[int]):
        pass

    integer_value = IntegerMother.create()

    assert Integer(value=integer_value) != integer_value


@mark.unit_testing
def test_value_object_float_equal_method() -> None:
    """
    Test value object float equal method.
    """

    class Float(ValueObject[float]):
        pass

    float_value = FloatMother.create()

    assert Float(value=float_value) == Float(value=float_value)


@mark.unit_testing
def test_value_object_float_equal_method_with_different_values() -> None:
    """
    Test value object float equal method with different values.
    """

    class Float(ValueObject[float]):
        pass

    float_value_a = FloatMother.create(min=-100, max=100)
    float_value_b = FloatMother.create(min=-100, max=100)

    assert Float(value=float_value_a) != Float(value=float_value_b)


@mark.unit_testing
def test_value_object_float_equal_method_different_types() -> None:
    """
    Test value object float equal method with different types.
    """

    class Float(ValueObject[float]):
        pass

    float_value = FloatMother.create()

    assert Float(value=float_value) != float_value


@mark.unit_testing
def test_value_object_date_equal_method() -> None:
    """
    Test value object date equal method.
    """

    class Date(ValueObject[date]):
        pass

    date_value = DateMother.create()

    assert Date(value=date_value) == Date(value=date_value)


@mark.unit_testing
def test_value_object_date_equal_method_with_different_values() -> None:
    """
    Test value object date equal method with different values.
    """

    class Date(ValueObject[date]):
        pass

    date_value_a = DateMother.create()
    date_value_b = DateMother.create()

    assert Date(value=date_value_a) != Date(value=date_value_b)


@mark.unit_testing
def test_value_object_date_equal_method_different_types() -> None:
    """
    Test value object date equal method with different types.
    """

    class Date(ValueObject[date]):
        pass

    date_value = DateMother.create()

    assert Date(value=date_value) != date_value


@mark.unit_testing
def test_value_object_string_date_equal_method() -> None:
    """
    Test value object string date equal method.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value = StringDateMother.create()

    assert StringDate(value=string_date_value) == StringDate(value=string_date_value)


@mark.unit_testing
def test_value_object_string_date_equal_method_with_different_values() -> None:
    """
    Test value object string date equal method with different values.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value_a = StringDateMother.create()
    string_date_value_b = StringDateMother.create()

    assert StringDate(value=string_date_value_a) != StringDate(value=string_date_value_b)


@mark.unit_testing
def test_value_object_string_date_equal_method_different_types() -> None:
    """
    Test value object string date equal method with different types.
    """

    class StringDate(ValueObject[str]):
        pass

    string_date_value = StringDateMother.create()

    assert StringDate(value=string_date_value) != string_date_value


@mark.unit_testing
def test_value_object_datetime_equal_method() -> None:
    """
    Test value object datetime equal method.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value = DatetimeMother.create()

    assert Datetime(value=datetime_value) == Datetime(value=datetime_value)


@mark.unit_testing
def test_value_object_datetime_equal_method_with_different_values() -> None:
    """
    Test value object datetime equal method with different values.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value_a = DatetimeMother.create()
    datetime_value_b = DatetimeMother.create()

    assert Datetime(value=datetime_value_a) != Datetime(value=datetime_value_b)


@mark.unit_testing
def test_value_object_datetime_equal_method_different_types() -> None:
    """
    Test value object datetime equal method with different types.
    """

    class Datetime(ValueObject[datetime]):
        pass

    datetime_value = DatetimeMother.create()

    assert Datetime(value=datetime_value) != datetime_value


@mark.unit_testing
def test_value_object_string_datetime_equal_method() -> None:
    """
    Test value object string datetime equal method.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value = StringDatetimeMother.create()

    assert StringDatetime(value=string_datetime_value) == StringDatetime(value=string_datetime_value)


@mark.unit_testing
def test_value_object_string_datetime_equal_method_with_different_values() -> None:
    """
    Test value object string datetime equal method with different values.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value_a = StringDatetimeMother.create()
    string_datetime_value_b = StringDatetimeMother.create()

    assert StringDatetime(value=string_datetime_value_a) != StringDatetime(value=string_datetime_value_b)


@mark.unit_testing
def test_value_object_string_datetime_equal_method_different_types() -> None:
    """
    Test value object string datetime equal method with different types.
    """

    class StringDatetime(ValueObject[str]):
        pass

    string_datetime_value = StringDatetimeMother.create()

    assert StringDatetime(value=string_datetime_value) != string_datetime_value


@mark.unit_testing
def test_value_object_uuid_equal_method() -> None:
    """
    Test value object uuid equal method.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value = UUIDMother.create()

    assert _UUID(value=uuid_value) == _UUID(value=uuid_value)


@mark.unit_testing
def test_value_object_uuid_equal_method_with_different_values() -> None:
    """
    Test value object uuid equal method with different values.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value_a = UUIDMother.create()
    uuid_value_b = UUIDMother.create()

    assert _UUID(value=uuid_value_a) != _UUID(value=uuid_value_b)


@mark.unit_testing
def test_value_object_uuid_equal_method_different_types() -> None:
    """
    Test value object uuid equal method with different types.
    """

    class _UUID(ValueObject[UUID]):
        pass

    uuid_value = UUIDMother.create()

    assert _UUID(value=uuid_value) != uuid_value


@mark.unit_testing
def test_value_object_string_uuid_equal_method() -> None:
    """
    Test value object string uuid equal method.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value = StringUUIDMother.create()

    assert StringUUID(value=string_uuid_value) == StringUUID(value=string_uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_equal_method_with_different_values() -> None:
    """
    Test value object string uuid equal method with different values.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value_a = StringUUIDMother.create()
    string_uuid_value_b = StringUUIDMother.create()

    assert StringUUID(value=string_uuid_value_a) != StringUUID(value=string_uuid_value_b)


@mark.unit_testing
def test_value_object_string_uuid_equal_method_different_types() -> None:
    """
    Test value object string uuid equal method with different types.
    """

    class StringUUID(ValueObject[str]):
        pass

    string_uuid_value = StringUUIDMother.create()

    assert StringUUID(value=string_uuid_value) != string_uuid_value
