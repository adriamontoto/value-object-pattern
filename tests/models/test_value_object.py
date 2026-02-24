"""
Test value object equal method.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from copy import copy, deepcopy
from typing import Any

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
from pytest import mark, raises as assert_raises

from value_object_pattern import ValueObject, process, validation
from value_object_pattern.usables import (
    BooleanValueObject,
    BytesValueObject,
    FloatValueObject,
    IntegerValueObject,
    StringValueObject,
    TrimmedStringValueObject,
)
from value_object_pattern.usables.dates import (
    DateValueObject,
    DatetimeValueObject,
    StringDateValueObject,
    StringDatetimeValueObject,
)
from value_object_pattern.usables.identifiers import StringUuidValueObject, UuidValueObject


class ListValueObject(ValueObject[list[int]]):
    """
    List value object used for deepcopy tests.
    """


class UntypedValueObject(ValueObject[Any]):
    """
    Value object without explicit generic parameter.
    """


class ValueObjectA(ValueObject[str]):
    """
    ValueObjectA value object class.
    """

    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'A1'

    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'A2'

    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'A3'

    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'A4'

    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'A5'


class ValueObjectB(ValueObject[str]):
    """
    ValueObjectB value object class.
    """

    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'B1'

    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'B2'

    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'B3'

    @process()
    def _concat_four(self, value: str) -> str:
        return value + 'B4'

    @process()
    def _aconcat_five(self, value: str) -> str:
        return value + 'B5'


class ValueObjectC(ValueObjectA, ValueObjectB):
    """
    ValueObjectC value object class.
    """

    @override
    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'C1'

    @override
    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'C2'

    @override
    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'C3'

    @override
    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'C4'

    @override
    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'C5'


class ValueObjectD(ValueObjectB, ValueObjectA):
    """
    ValueObjectD value object class.
    """

    @override
    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'D1'

    @override
    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'D2'

    @override
    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'D3'

    @override
    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'D4'

    @override
    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'D5'


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


@mark.unit_testing
def test_value_object_get_attribute() -> None:
    """
    Test that a value object value can be accessed.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    value_object.value  # noqa: B018


@mark.unit_testing
def test_value_object_get_title_attribute() -> None:
    """
    Test that a value object title can be accessed.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    value_object.title  # noqa: B018


@mark.unit_testing
def test_value_object_get_protected_attribute() -> None:
    """
    Test that a value object protected value can be accessed.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    value_object._value  # noqa: B018


@mark.unit_testing
def test_value_object_cannot_get_unexistent_attribute() -> None:
    """
    Test that a value object value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match=f"'{value_object.__class__.__name__}' object has no attribute 'not_existent_attribute'",
    ):
        value_object.not_existent_attribute  # type: ignore[attr-defined]  # noqa: B018


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


@mark.unit_testing
def test_value_object_parameter_attribute_equals_default_value_object_name() -> None:
    """
    Test that a value object parameter attribute equals the default value object name if not provided.
    """
    value_object = TrimmedStringValueObject(value=StringMother.create())

    assert value_object.parameter == 'value'


@mark.unit_testing
def test_value_object_parameter_attribute_equals_custom_value_object_name() -> None:
    """
    Test that a value object parameter attribute equals the custom value object name.
    """
    parameter = StringMother.create()
    value_object = TrimmedStringValueObject(value=StringMother.create(), parameter=parameter)

    assert value_object.parameter == parameter


@mark.unit_testing
def test_value_object_parameter_attribute_accepts_empty_string() -> None:
    """
    Test that a value object parameter attribute accepts an empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject parameter <<<.*>>> must not be an empty string.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.empty())


@mark.unit_testing
def test_value_object_parameter_attribute_raises_type_error_when_not_string() -> None:
    """
    Test that a value object parameter attribute raises TypeError when not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ValueObject parameter <<<.*>>> must be a string. Got <<<.*>>> instead.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.invalid_type())


@mark.unit_testing
def test_value_object_parameter_attribute_can_not_contain_leading_or_trailing_whitespaces() -> None:
    """
    Test that a value object parameter attribute can not contain leading or trailing whitespaces.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject parameter <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',  # noqa: E501
    ):
        TrimmedStringValueObject(value=StringMother.create(), parameter=StringMother.not_trimmed())


@mark.unit_testing
def test_value_object_process_method_order_happy_path() -> None:
    """
    Test value object process method invalid type.
    """

    class UpperStringValueObject(ValueObject[str]):
        @process(order=IntegerMother.create(min=0))
        def ensure_value_is_upper(self, value: str) -> str:
            return value.upper()


@mark.unit_testing
def test_value_object_process_method_order_invalid_type() -> None:
    """
    Test value object process method invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Process order <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=IntegerMother.invalid_type())
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()


@mark.unit_testing
def test_value_object_process_method_order_invalid_value() -> None:
    """
    Test value object process method invalid value.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Process order <<<.*>>> must be equal or greater than 0.',
    ):

        class UpperStringValueObject(ValueObject[str]):
            @process(order=IntegerMother.negative())
            def ensure_value_is_upper(self, value: str) -> str:
                return value.upper()


@mark.unit_testing
def test_value_object_string_representation_method() -> None:
    """
    Test value object string representation method.
    """
    string_value = StringMother.create()
    string = StringValueObject(value=string_value)

    assert repr(string) == f'StringValueObject(value={string_value!r})'


@mark.unit_testing
def test_value_object_bytes_representation_method() -> None:
    """
    Test value object bytes representation method.
    """
    bytes_value = BytesMother.create()
    bytes_ = BytesValueObject(value=bytes_value)

    assert repr(bytes_) == f'BytesValueObject(value={bytes_value!r})'


@mark.unit_testing
def test_value_object_bool_representation_method() -> None:
    """
    Test value object bool representation method.
    """
    boolean_value = BooleanMother.create()
    boolean = BooleanValueObject(value=boolean_value)

    assert repr(boolean) == f'BooleanValueObject(value={boolean_value!r})'


@mark.unit_testing
def test_value_object_integer_representation_method() -> None:
    """
    Test value object integer representation method.
    """
    integer_value = IntegerMother.create()
    integer = IntegerValueObject(value=integer_value)

    assert repr(integer) == f'IntegerValueObject(value={integer_value!r})'


@mark.unit_testing
def test_value_object_float_representation_method() -> None:
    """
    Test value object float representation method.
    """
    float_value = FloatMother.create()
    float_ = FloatValueObject(value=float_value)

    assert repr(float_) == f'FloatValueObject(value={float_value!r})'


@mark.unit_testing
def test_value_object_date_representation_method() -> None:
    """
    Test value object date representation method.
    """
    date_value = DateMother.create()
    date = DateValueObject(value=date_value)

    assert repr(date) == f'DateValueObject(value={date_value!r})'


@mark.unit_testing
def test_value_object_string_date_representation_method() -> None:
    """
    Test value object string date representation method.
    """
    string_date_value = StringDateMother.create()
    string_date = StringDateValueObject(value=string_date_value)

    assert repr(string_date) == f'StringDateValueObject(value={string_date_value!r})'


@mark.unit_testing
def test_value_object_datetime_representation_method() -> None:
    """
    Test value object datetime representation method.
    """
    datetime_value = DatetimeMother.create()
    datetime = DatetimeValueObject(value=datetime_value)

    assert repr(datetime) == f'DatetimeValueObject(value={datetime_value!r})'


@mark.unit_testing
def test_value_object_string_datetime_representation_method() -> None:
    """
    Test value object string datetime representation method.
    """
    string_datetime_value = StringDatetimeMother.create()
    string_datetime = StringDatetimeValueObject(value=string_datetime_value)

    assert repr(string_datetime) == f'StringDatetimeValueObject(value={string_datetime_value!r})'


@mark.unit_testing
def test_value_object_uuid_representation_method() -> None:
    """
    Test value object UUID representation method.
    """
    uuid_value = UuidMother.create()
    uuid = UuidValueObject(value=uuid_value)

    assert repr(uuid) == f'UuidValueObject(value={uuid_value!r})'


@mark.unit_testing
def test_value_object_string_uuid_representation_method() -> None:
    """
    Test value object string UUID representation method.
    """
    string_uuid_value = StringUuidMother.create()
    string_uuid = StringUuidValueObject(value=string_uuid_value)

    assert repr(string_uuid) == f'StringUuidValueObject(value={string_uuid_value!r})'


@mark.unit_testing
def test_value_object_cannot_modify_value() -> None:
    """
    Test that a value object value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "value" of immutable instance',
    ):
        value_object.value = IntegerMother.create()  # type: ignore[misc]


@mark.unit_testing
def test_value_object_cannot_modify_title() -> None:
    """
    Test that a value object title cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "title" of immutable instance',
    ):
        value_object.title = StringMother.create()  # type: ignore[misc]


@mark.unit_testing
def test_value_object_cannot_modify_protected_value() -> None:
    """
    Test that a value object protected value cannot be modified after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match='Cannot modify attribute "_value" of immutable instance',
    ):
        value_object._value = IntegerMother.create()


@mark.unit_testing
def test_value_object_cannot_add_new_attribute() -> None:
    """
    Test that cannot add a new attribute to a value object after initialization.
    """
    value_object = IntegerValueObject(value=IntegerMother.create())

    with assert_raises(
        expected_exception=AttributeError,
        match=f'{value_object.__class__.__name__} object has no attribute "new_attribute"',
    ):
        value_object.new_attribute = IntegerMother.create()


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


@mark.unit_testing
def test_value_object_title_attribute_equals_default_value_object_name() -> None:
    """
    Test that a value object title attribute equals the default value object name if not provided.
    """
    value_object = TrimmedStringValueObject(value=StringMother.create())

    assert value_object.title == 'TrimmedStringValueObject'


@mark.unit_testing
def test_value_object_title_attribute_equals_custom_value_object_name() -> None:
    """
    Test that a value object title attribute equals the custom value object name.
    """
    title_name = StringMother.create()
    value_object = TrimmedStringValueObject(value=StringMother.create(), title=title_name)

    assert value_object.title == title_name


@mark.unit_testing
def test_value_object_title_attribute_raises_value_error_when_empty_string() -> None:
    """
    Test that a value object title attribute raises ValueError when an empty string is provided.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject title <<<.*>>> must not be an empty string.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.empty())


@mark.unit_testing
def test_value_object_title_attribute_raises_type_error_when_not_string() -> None:
    """
    Test that a value object title attribute raises TypeError when not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ValueObject title <<<.*>>> must be a string. Got <<<.*>>> instead.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.invalid_type())


@mark.unit_testing
def test_value_object_title_attribute_can_not_contain_leading_or_trailing_whitespaces() -> None:
    """
    Test that a value object title attribute can not contain leading or trailing whitespaces.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ValueObject title <<<.*>>> contains leading or trailing whitespaces. Only trimmed values are allowed.',
    ):
        TrimmedStringValueObject(value=StringMother.create(), title=StringMother.not_trimmed())


@mark.unit_testing
def test_value_object_validation_method_order_happy_path() -> None:
    """
    Test value object validation method invalid type.
    """

    class PositiveIntegerValueObject(ValueObject[int]):
        @validation()
        def ensure_value_is_integer(self, value: int) -> None:
            if type(value) is not int:
                raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_type() -> None:
    """
    Test value object validation method invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Validation order <<<.*>>> must be an integer. Got <<<.*>>> type.',
    ):

        class PositiveIntegerValueObject(ValueObject[int]):
            @validation(order=IntegerMother.invalid_type())
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


@mark.unit_testing
def test_value_object_validation_method_order_invalid_value() -> None:
    """
    Test value object validation method invalid value.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Validation order <<<.*>>> must be equal or greater than 0.',
    ):

        class PositiveIntegerValueObject(ValueObject[int]):
            @validation(order=IntegerMother.negative())
            def ensure_value_is_integer(self, value: int) -> None:
                if type(value) is not int:
                    raise TypeError(f'Value object must be an integer, not {type(value).__name__}.')


def test_value_object_a_validation_order() -> None:
    """
    Test ValueObjectA validation order.
    """
    value_object_a = ValueObjectA(value='')
    assert value_object_a.value == 'A1A2A3A4A5'


def test_value_object_b_validation_order() -> None:
    """
    Test ValueObjectB validation order.
    """
    value_object_b = ValueObjectB(value='')
    assert value_object_b.value == 'B1B2B3B5B4'


def test_value_object_c_validation_order() -> None:
    """
    Test value object C validation order. The order should be class hierarchy, method order attribute, and method name.
    """
    value_object_c = ValueObjectC(value='')

    assert value_object_c.value == 'A1A2A3A4A5B1B2B3B5B4C1C2C3C4C5'


def test_value_object_d_validation_order() -> None:
    """
    Test value object D validation order. The order should be class hierarchy, method order attribute, and method name.
    """
    value_object_d = ValueObjectD(value='')

    assert value_object_d.value == 'B1B2B3B5B4A1A2A3A4A5D1D2D3D4D5'


@mark.unit_testing
def test_value_object_copy_returns_new_instance_with_same_metadata() -> None:
    """
    Test that __copy__ creates a new instance preserving value, title and parameter.
    """
    value_object = IntegerValueObject(value=7, title='NumberTitle', parameter='number')

    clone = copy(value_object)

    assert clone is not value_object
    assert clone.value == 7
    assert clone.title == 'NumberTitle'
    assert clone.parameter == 'number'


@mark.unit_testing
def test_value_object_deepcopy_creates_independent_value_and_respects_memo() -> None:
    """
    Test that __deepcopy__ clones nested values and returns memoized entries when present.
    """
    value_object = ListValueObject(value=[1, 2], title='ListTitle', parameter='items')

    deep_clone = deepcopy(value_object)

    assert deep_clone is not value_object
    assert deep_clone.value == [1, 2]
    assert deep_clone.value is not value_object.value
    assert deep_clone.title == value_object.title
    assert deep_clone.parameter == value_object.parameter

    deep_clone.value.append(3)
    assert value_object.value == [1, 2]

    memo: dict[int, Any] = {id(value_object): 'cached'}
    assert value_object.__deepcopy__(memo) == 'cached'


@mark.unit_testing
def test_value_object_type_returns_generic_argument() -> None:
    """
    Test that type method returns the annotated generic argument.
    """
    assert IntegerValueObject.type() is int


@mark.unit_testing
def test_value_object_type_returns_any_when_subclass_is_not_parameterized() -> None:
    """
    Test that type method returns Any when subclass has no generic type arguments.
    """
    assert UntypedValueObject.type() is Any


@mark.unit_testing
def test_value_object_type_returns_any_when_no_generic_arguments_are_available() -> None:
    """
    Test that type method returns Any when orig base contains ValueObject without args.
    """

    class _Placeholder:
        __origin__ = ValueObject
        __args__ = ()

    class NoArgsValueObject(ValueObject[int]):
        pass

    original_bases = NoArgsValueObject.__orig_bases__  # type: ignore[attr-defined]
    NoArgsValueObject.__orig_bases__ = (_Placeholder,)  # type: ignore[attr-defined]

    try:
        assert NoArgsValueObject.type() is Any  # type: ignore[comparison-overlap]

    finally:
        NoArgsValueObject.__orig_bases__ = original_bases  # type: ignore[attr-defined]
