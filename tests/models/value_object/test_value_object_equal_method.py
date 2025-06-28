"""
Test value object equal method.
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
def test_value_object_string_equal_method() -> None:
    """
    Test value object string equal method.
    """
    string_value = StringMother.create()

    assert StringValueObject(value=string_value) == StringValueObject(value=string_value)


@mark.unit_testing
def test_value_object_string_equal_method_with_different_values() -> None:
    """
    Test value object string equal method with different values.
    """
    string_value_a = StringMother.create()
    string_value_b = StringMother.create()

    assert StringValueObject(value=string_value_a) != StringValueObject(value=string_value_b)


@mark.unit_testing
def test_value_object_string_equal_method_different_types() -> None:
    """
    Test value object string equal method with different types.
    """
    string_value = StringMother.create()

    assert StringValueObject(value=string_value) != string_value


@mark.unit_testing
def test_value_object_bytes_equal_method() -> None:
    """
    Test value object bytes equal method.
    """
    bytes_value = BytesMother.create()

    assert BytesValueObject(value=bytes_value) == BytesValueObject(value=bytes_value)


@mark.unit_testing
def test_value_object_bytes_equal_method_with_different_values() -> None:
    """
    Test value object bytes equal method with different values.
    """
    bytes_value_a = BytesMother.create()
    bytes_value_b = BytesMother.create()

    assert BytesValueObject(value=bytes_value_a) != BytesValueObject(value=bytes_value_b)


@mark.unit_testing
def test_value_object_bytes_equal_method_different_types() -> None:
    """
    Test value object bytes equal method with different types.
    """
    bytes_value = BytesMother.create()

    assert BytesValueObject(value=bytes_value) != bytes_value


@mark.unit_testing
def test_value_object_bool_equal_method() -> None:
    """
    Test value object bool equal method.
    """
    bool_value = BooleanMother.create()

    assert BooleanValueObject(value=bool_value) == BooleanValueObject(value=bool_value)


@mark.unit_testing
def test_value_object_bool_equal_method_with_different_values() -> None:
    """
    Test value object bool equal method with different values.
    """
    assert BooleanValueObject(value=True) != BooleanValueObject(value=False)


@mark.unit_testing
def test_value_object_bool_equal_method_different_types() -> None:
    """
    Test value object bool equal method with different types.
    """
    bool_value = BooleanMother.create()

    assert BooleanValueObject(value=bool_value) != bool_value


@mark.unit_testing
def test_value_object_integer_equal_method() -> None:
    """
    Test value object integer equal method.
    """
    integer_value = IntegerMother.create()

    assert IntegerValueObject(value=integer_value) == IntegerValueObject(value=integer_value)


@mark.unit_testing
def test_value_object_integer_equal_method_with_different_values() -> None:
    """
    Test value object integer equal method with different values.
    """
    integer_value_a = IntegerMother.create(min=0, max=16)
    integer_value_b = IntegerMother.create(min=17, max=32)

    assert IntegerValueObject(value=integer_value_a) != IntegerValueObject(value=integer_value_b)


@mark.unit_testing
def test_value_object_integer_equal_method_different_types() -> None:
    """
    Test value object integer equal method with different types.
    """
    integer_value = IntegerMother.create()

    assert IntegerValueObject(value=integer_value) != integer_value


@mark.unit_testing
def test_value_object_float_equal_method() -> None:
    """
    Test value object float equal method.
    """
    float_value = FloatMother.create()

    assert FloatValueObject(value=float_value) == FloatValueObject(value=float_value)


@mark.unit_testing
def test_value_object_float_equal_method_with_different_values() -> None:
    """
    Test value object float equal method with different values.
    """
    float_value_a = FloatMother.create(min=-100, max=100)
    float_value_b = FloatMother.create(min=-100, max=100)

    assert FloatValueObject(value=float_value_a) != FloatValueObject(value=float_value_b)


@mark.unit_testing
def test_value_object_float_equal_method_different_types() -> None:
    """
    Test value object float equal method with different types.
    """
    float_value = FloatMother.create()

    assert FloatValueObject(value=float_value) != float_value


@mark.unit_testing
def test_value_object_date_equal_method() -> None:
    """
    Test value object date equal method.
    """
    date_value = DateMother.create()

    assert DateValueObject(value=date_value) == DateValueObject(value=date_value)


@mark.unit_testing
def test_value_object_date_equal_method_with_different_values() -> None:
    """
    Test value object date equal method with different values.
    """
    date_value_a = DateMother.create()
    date_value_b = DateMother.create()

    assert DateValueObject(value=date_value_a) != DateValueObject(value=date_value_b)


@mark.unit_testing
def test_value_object_date_equal_method_different_types() -> None:
    """
    Test value object date equal method with different types.
    """
    date_value = DateMother.create()

    assert DateValueObject(value=date_value) != date_value


@mark.unit_testing
def test_value_object_string_date_equal_method() -> None:
    """
    Test value object string date equal method.
    """
    string_date_value = StringDateMother.create()

    assert StringDateValueObject(value=string_date_value) == StringDateValueObject(value=string_date_value)


@mark.unit_testing
def test_value_object_string_date_equal_method_with_different_values() -> None:
    """
    Test value object string date equal method with different values.
    """
    string_date_value_a = StringDateMother.create()
    string_date_value_b = StringDateMother.create()

    assert StringDateValueObject(value=string_date_value_a) != StringDateValueObject(value=string_date_value_b)


@mark.unit_testing
def test_value_object_string_date_equal_method_different_types() -> None:
    """
    Test value object string date equal method with different types.
    """
    string_date_value = StringDateMother.create()

    assert StringDateValueObject(value=string_date_value) != string_date_value


@mark.unit_testing
def test_value_object_datetime_equal_method() -> None:
    """
    Test value object datetime equal method.
    """
    datetime_value = DatetimeMother.create()

    assert DatetimeValueObject(value=datetime_value) == DatetimeValueObject(value=datetime_value)


@mark.unit_testing
def test_value_object_datetime_equal_method_with_different_values() -> None:
    """
    Test value object datetime equal method with different values.
    """
    datetime_value_a = DatetimeMother.create()
    datetime_value_b = DatetimeMother.create()

    assert DatetimeValueObject(value=datetime_value_a) != DatetimeValueObject(value=datetime_value_b)


@mark.unit_testing
def test_value_object_datetime_equal_method_different_types() -> None:
    """
    Test value object datetime equal method with different types.
    """
    datetime_value = DatetimeMother.create()

    assert DatetimeValueObject(value=datetime_value) != datetime_value


@mark.unit_testing
def test_value_object_string_datetime_equal_method() -> None:
    """
    Test value object string datetime equal method.
    """
    string_datetime_value = StringDatetimeMother.create()

    assert StringDatetimeValueObject(
        value=string_datetime_value,
    ) == StringDatetimeValueObject(
        value=string_datetime_value,
    )


@mark.unit_testing
def test_value_object_string_datetime_equal_method_with_different_values() -> None:
    """
    Test value object string datetime equal method with different values.
    """
    string_datetime_value_a = StringDatetimeMother.create()
    string_datetime_value_b = StringDatetimeMother.create()

    assert StringDatetimeValueObject(
        value=string_datetime_value_a,
    ) != StringDatetimeValueObject(
        value=string_datetime_value_b,
    )


@mark.unit_testing
def test_value_object_string_datetime_equal_method_different_types() -> None:
    """
    Test value object string datetime equal method with different types.
    """
    string_datetime_value = StringDatetimeMother.create()

    assert StringDatetimeValueObject(value=string_datetime_value) != string_datetime_value


@mark.unit_testing
def test_value_object_uuid_equal_method() -> None:
    """
    Test value object uuid equal method.
    """
    uuid_value = UuidMother.create()

    assert UuidValueObject(value=uuid_value) == UuidValueObject(value=uuid_value)


@mark.unit_testing
def test_value_object_uuid_equal_method_with_different_values() -> None:
    """
    Test value object uuid equal method with different values.
    """
    uuid_value_a = UuidMother.create()
    uuid_value_b = UuidMother.create()

    assert UuidValueObject(value=uuid_value_a) != UuidValueObject(value=uuid_value_b)


@mark.unit_testing
def test_value_object_uuid_equal_method_different_types() -> None:
    """
    Test value object uuid equal method with different types.
    """
    uuid_value = UuidMother.create()

    assert UuidValueObject(value=uuid_value) != uuid_value


@mark.unit_testing
def test_value_object_string_uuid_equal_method() -> None:
    """
    Test value object string uuid equal method.
    """
    string_uuid_value = StringUuidMother.create()

    assert StringUuidValueObject(value=string_uuid_value) == StringUuidValueObject(value=string_uuid_value)


@mark.unit_testing
def test_value_object_string_uuid_equal_method_with_different_values() -> None:
    """
    Test value object string uuid equal method with different values.
    """
    string_uuid_value_a = StringUuidMother.create()
    string_uuid_value_b = StringUuidMother.create()

    assert StringUuidValueObject(value=string_uuid_value_a) != StringUuidValueObject(value=string_uuid_value_b)


@mark.unit_testing
def test_value_object_string_uuid_equal_method_different_types() -> None:
    """
    Test value object string uuid equal method with different types.
    """
    string_uuid_value = StringUuidMother.create()

    assert StringUuidValueObject(value=string_uuid_value) != string_uuid_value
