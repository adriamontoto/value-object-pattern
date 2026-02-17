"""
Test DictValueObject value object.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from typing import Any, ForwardRef, TypeVar

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from value_object_pattern import BaseModel, EnumerationValueObject, ValueObject
from value_object_pattern.models.collections import DictValueObject


class StrIntDictValueObject(DictValueObject[str, int]):
    """
    Dict value object storing string keys and integer values.
    """


class AnyKeyDictValueObject(DictValueObject[Any, int]):
    """
    Dict value object storing any keys and integer values.
    """


class AnyValueDictValueObject(DictValueObject[str, Any]):
    """
    Dict value object storing string keys and any values.
    """


class AnyDictValueObject(DictValueObject[Any, Any]):
    """
    Dict value object storing any keys and any values.
    """


class IntOrStrKeyDictValueObject(DictValueObject[int | str, int]):
    """
    Dict value object storing int or str keys and integer values.
    """


class StrIntOrStrValueDictValueObject(DictValueObject[str, int | str]):
    """
    Dict value object storing string keys and int or str values.
    """


class AnyOrIntKeyDictValueObject(DictValueObject[int | Any, int]):
    """
    Dict value object storing any or int keys.
    """


class StrIntOrAnyValueDictValueObject(DictValueObject[str, int | Any]):
    """
    Dict value object storing string keys and any or int values.
    """


class IntOrStrIntOrStrDictValueObject(DictValueObject[int | str, int | str]):
    """
    Dict value object storing int or str keys and int or str values.
    """


class SimpleValueObject(ValueObject[int]):
    """
    Simple integer value object.
    """


class StrValueObjectDict(DictValueObject[str, SimpleValueObject]):
    """
    Dict value object storing string keys and SimpleValueObject values.
    """


class NestedModel(BaseModel):
    """
    Nested BaseModel used to check recursive conversion.
    """

    def __init__(self, code: int) -> None:
        """
        Nested model constructor.
        """
        self.code = code


class StrNestedModelDict(DictValueObject[str, NestedModel]):
    """
    Dict value object storing string keys and NestedModel values.
    """


class CustomObject:
    """
    Helper object used to exercise the string conversion branch.
    """

    @override
    def __repr__(self) -> str:
        """
        Custom representation.
        """
        return 'custom-object'


class StrCustomObjectDict(DictValueObject[str, CustomObject]):
    """
    Dict value object storing string keys and CustomObject values.
    """


class ValueObjectIntDict(DictValueObject[SimpleValueObject, int]):
    """
    Dict value object with ValueObject keys.
    """


class DummyEnum(Enum):
    """
    Enumeration used in DictValueObject tests.
    """

    ADMIN = 'admin'
    USER = 'user'


class EnumIntDict(DictValueObject[DummyEnum, int]):
    """
    Dict value object with Enum keys.
    """


class Status(Enum):
    """
    Status enumeration used in DictValueObject tests.
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'


class StrEnumDict(DictValueObject[str, Status]):
    """
    Dict value object with Enum values.
    """


class CustomKeyWithToPrimitives:
    """
    Custom key class that has to_primitives method but doesn't inherit from BaseModel.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize CustomKeyWithToPrimitives.
        """
        self.value = value

    def to_primitives(self) -> str:
        """
        Convert to primitive representation.
        """
        return f'custom-{self.value}'

    @override
    def __hash__(self) -> int:
        return hash(self.value)

    @override
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CustomKeyWithToPrimitives) and self.value == other.value


class CustomKeyWithToPrimitivesIntDict(DictValueObject[CustomKeyWithToPrimitives, int]):
    """
    Dict value object with custom key type that has to_primitives.
    """


class CustomValueWithToPrimitives:
    """
    Custom value class that has to_primitives method but doesn't inherit from BaseModel.
    """

    def __init__(self, data: str) -> None:
        """
        Initialize CustomValueWithToPrimitives.
        """
        self.data = data

    def to_primitives(self) -> str:
        """
        Convert to primitive representation.
        """
        return f'custom-{self.data}'


class StrCustomValueDict(DictValueObject[str, CustomValueWithToPrimitives]):
    """
    Dict value object with custom value type.
    """


class StatusValueObject(ValueObject[Status]):
    """
    Value object wrapping Status enum.
    """


class StatusValueObjectIntDict(DictValueObject[StatusValueObject, int]):
    """
    Dict value object with ValueObject keys that contain enums.
    """


class CustomKey:
    """
    Custom key class without to_primitives.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize CustomKey.
        """
        self.name = name

    @override
    def __repr__(self) -> str:
        return f'CustomKey({self.name})'

    @override
    def __hash__(self) -> int:
        return hash(self.name)

    @override
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CustomKey) and self.name == other.name


class CustomKeyIntDict(DictValueObject[CustomKey, int]):
    """
    Dict value object with custom key type without to_primitives.
    """


class ModelValue(BaseModel):
    """
    BaseModel used as dict value in from_primitives tests.
    """

    def __init__(self, name: str) -> None:
        """
        Initialize ModelValue.
        """
        self.name = name


class StatusEnumValueObject(EnumerationValueObject[Status]):
    """
    Enumeration value object used in from_primitives tests.
    """


class StrModelValueDict(DictValueObject[str, ModelValue]):
    """
    Dict value object using BaseModel for values.
    """


class StatusEnumValueObjectDict(DictValueObject[StatusEnumValueObject, StatusEnumValueObject]):
    """
    Dict value object using EnumerationValueObject for both keys and values.
    """


@mark.unit_testing
def test_dict_value_object_contains_existing_key() -> None:
    """
    Test that __contains__ returns True for existing keys.
    """
    mapping = StrIntDictValueObject(value={'a': 1})

    assert 'a' in mapping


@mark.unit_testing
def test_dict_value_object_iter_returns_keys() -> None:
    """
    Test that __iter__ returns the underlying keys.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert list(mapping) == ['a', 'b']


@mark.unit_testing
def test_dict_value_object_len_counts_items() -> None:
    """
    Test that __len__ returns the dictionary length.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert len(mapping) == 2


@mark.unit_testing
def test_dict_value_object_reversed_returns_reversed_keys() -> None:
    """
    Test that __reversed__ yields keys in reverse order.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert list(reversed(mapping)) == ['b', 'a']


@mark.unit_testing
def test_dict_value_object_getitem_returns_value_for_key() -> None:
    """
    Test that __getitem__ returns the value for a key.
    """
    mapping = StrIntDictValueObject(value={'a': 1})

    assert mapping['a'] == 1


@mark.unit_testing
def test_dict_value_object_items_view_matches_pairs() -> None:
    """
    Test that items() returns key/value pairs.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert list(mapping.items()) == [('a', 1), ('b', 2)]


@mark.unit_testing
def test_dict_value_object_keys_view_matches_keys() -> None:
    """
    Test that keys() returns the dictionary keys.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert list(mapping.keys()) == ['a', 'b']


@mark.unit_testing
def test_dict_value_object_values_view_matches_values() -> None:
    """
    Test that values() returns the dictionary values.
    """
    mapping = StrIntDictValueObject(value={'a': 1, 'b': 2})

    assert list(mapping.values()) == [1, 2]


@mark.unit_testing
def test_dict_value_object_str_matches_underlying_dict() -> None:
    """
    Test that __str__ mirrors the underlying dict.
    """
    values = {'a': 1, 'b': 2}

    assert str(StrIntDictValueObject(value=values)) == str(values)


@mark.unit_testing
def test_dict_value_object_repr_includes_class_and_value() -> None:
    """
    Test that __repr__ includes the class name and value.
    """
    values = {'a': 1}

    assert repr(StrIntDictValueObject(value=values)) == f'StrIntDictValueObject(value={values!r})'


@mark.unit_testing
def test_dict_value_object_is_empty_returns_true_for_empty_dict() -> None:
    """
    Test that is_empty returns True for an empty dict.
    """
    assert StrIntDictValueObject(value={}).is_empty()


@mark.unit_testing
def test_dict_value_object_is_empty_returns_false_for_non_empty_dict() -> None:
    """
    Test that is_empty returns False for a non-empty dict.
    """
    assert not StrIntDictValueObject(value={'a': 1}).is_empty()


@mark.unit_testing
def test_dict_value_object_requires_parameterization() -> None:
    """
    Test that __init_subclass__ raises TypeError when the class is not parameterized.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject must be parameterised, e\.g\. `class StrIntDict\(DictValueObject\[str, int\]\)`.',
    ):

        class _InvalidDictValueObject(DictValueObject):  # type: ignore[type-arg]  # pragma: no cover
            pass


@mark.unit_testing
def test_dict_value_object_requires_key_type_argument_to_be_type() -> None:
    """
    Test that __init_subclass__ raises TypeError when the key generic argument is not a type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject\[\.\.\.\] <<<.*>>> must be a type\. Got <<<.*>>> type\.',
    ):

        class _InvalidKeyDictValueObject(DictValueObject[IntegerMother.create(), int]):  # type: ignore[misc]  # pragma: no cover
            pass


@mark.unit_testing
def test_dict_value_object_requires_value_type_argument_to_be_type() -> None:
    """
    Test that __init_subclass__ raises TypeError when the value generic argument is not a type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject\[\.\.\.\] <<<.*>>> must be a type\. Got <<<.*>>> type\.',
    ):

        class _InvalidValueDictValueObject(DictValueObject[str, IntegerMother.create()]):  # type: ignore[misc]  # pragma: no cover
            pass


@mark.unit_testing
def test_dict_value_object_allows_typevar_parameterization() -> None:
    """
    Test that __init_subclass__ accepts TypeVar arguments without raising.
    """
    TKey = TypeVar('TKey')
    TValue = TypeVar('TValue')

    class _GenericDictValueObject(DictValueObject[TKey, TValue]):  # pragma: no cover
        pass

    assert _GenericDictValueObject._key_type is TKey  # type: ignore[misc]
    assert _GenericDictValueObject._value_type is TValue  # type: ignore[misc]


@mark.unit_testing
def test_dict_value_object_raises_type_error_when_value_is_not_dict() -> None:
    """
    Test that a TypeError is raised when the provided value is not a dict.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be a dict\. Got <<<.*>>> type\.',
    ):
        StrIntDictValueObject(value=BaseMother.invalid_type(remove_types=(dict,)))


@mark.unit_testing
def test_dict_value_object_raises_type_error_when_key_has_wrong_type() -> None:
    """
    Test that a TypeError is raised when keys do not match the annotated type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<str>>> type\. Got <<<.*>>> type\.',
    ):
        StrIntDictValueObject(value={1: 2})  # type: ignore[dict-item]


@mark.unit_testing
def test_dict_value_object_raises_type_error_when_value_has_wrong_type() -> None:
    """
    Test that a TypeError is raised when values do not match the annotated type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        StrIntDictValueObject(value={'a': 'wrong'})  # type: ignore[dict-item]


@mark.unit_testing
def test_dict_value_object_get_returns_default_when_missing_key() -> None:
    """
    Test that get returns the provided default when the key is missing.
    """
    mapping = StrIntDictValueObject(value={'a': 1})

    assert mapping.get(key='b', default=2) == 2


@mark.unit_testing
def test_dict_value_object_get_returns_none_when_key_missing_and_no_default() -> None:
    """
    Test that get returns None when key is missing and no default is provided.
    """
    mapping = StrIntDictValueObject(value={'a': 1})

    assert mapping.get(key='b') is None


@mark.unit_testing
def test_dict_value_object_get_raises_type_error_when_default_has_wrong_type() -> None:
    """
    Test that get raises TypeError when the default is not of the value type.
    """
    mapping = StrIntDictValueObject(value={'a': 1})

    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        mapping.get(key='b', default=IntegerMother.invalid_type(remove_types=(bool,)))


@mark.unit_testing
def test_dict_value_object_any_accepts_mixed_entries() -> None:
    """
    Test that Any annotations allow mixed key/value types.
    """
    mapping = AnyDictValueObject(value={1: 'one', 'b': 2, ('tuple',): object()})

    assert len(mapping) == 3


@mark.unit_testing
def test_dict_value_object_any_retains_values() -> None:
    """
    Test that Any annotations preserve inserted values.
    """
    mapping = AnyDictValueObject(value={'b': 2})

    assert mapping['b'] == 2


@mark.unit_testing
def test_dict_value_object_any_key_allows_mixed_key_types() -> None:
    """
    Test that Any key type accepts mixed key types.
    """
    mapping = AnyKeyDictValueObject(value={1: 1, 'b': 2})

    assert set(mapping.keys()) == {1, 'b'}


@mark.unit_testing
def test_dict_value_object_any_value_allows_mixed_value_types() -> None:
    """
    Test that Any value type accepts mixed value types.
    """
    mapping = AnyValueDictValueObject(value={'a': 1, 'b': 'two'})

    assert list(mapping.values()) == [1, 'two']


@mark.unit_testing
def test_dict_value_object_get_allows_default_when_value_type_is_any() -> None:
    """
    Test that get accepts any default when value type is Any.
    """
    mapping = AnyValueDictValueObject(value={'a': 1})
    sentinel = object()

    assert mapping.get(key='missing', default=sentinel) is sentinel


@mark.unit_testing
def test_dict_value_object_get_allows_default_when_value_union_contains_any() -> None:
    """
    Test that get accepts any default when value type union contains Any.
    """
    mapping = StrIntOrAnyValueDictValueObject(value={'a': 1})
    sentinel = object()

    assert mapping.get(key='missing', default=sentinel) is sentinel


@mark.unit_testing
def test_dict_value_object_get_rejects_default_outside_union_value_types() -> None:
    """
    Test that get rejects default not in the value union when no Any is present.
    """
    mapping = StrIntOrStrValueDictValueObject(value={'a': 1})

    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<int \| str>>> type\. Got <<<.*>>> type\.',
    ):
        mapping.get(key='missing', default=IntegerMother.invalid_type(remove_types=(int, bool, str)))


@mark.unit_testing
def test_dict_value_object_get_accepts_default_inside_union_value_types() -> None:
    """
    Test that get accepts default that matches the value union.
    """
    mapping = StrIntOrStrValueDictValueObject(value={'a': 1})

    assert mapping.get(key='missing', default='fallback') == 'fallback'


@mark.unit_testing
def test_dict_value_object_format_single_type_handles_forward_ref() -> None:
    """
    Test that _format_single_type covers branch without __name__.
    """
    assert DictValueObject._format_single_type(type=ForwardRef('SomeType')) == "ForwardRef('SomeType')"


@mark.unit_testing
def test_dict_value_object_accepts_union_key_types() -> None:
    """
    Test that DictValueObject accepts union key types (int | str).
    """
    mapping = IntOrStrKeyDictValueObject(value={1: 10, 'b': 20})

    assert set(mapping.keys()) == {1, 'b'}


@mark.unit_testing
def test_dict_value_object_union_key_rejects_out_of_union_type() -> None:
    """
    Test that union-typed keys reject keys outside the union.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<int \| str>>> type\. Got <<<.*>>> type\.',
    ):
        IntOrStrKeyDictValueObject(value={1.5: 1})  # type: ignore[dict-item]


@mark.unit_testing
def test_dict_value_object_accepts_union_value_types() -> None:
    """
    Test that DictValueObject accepts union value types (int | str).
    """
    mapping = StrIntOrStrValueDictValueObject(value={'a': 1, 'b': 'two'})

    assert list(mapping.values()) == [1, 'two']


@mark.unit_testing
def test_dict_value_object_union_value_rejects_out_of_union_type() -> None:
    """
    Test that union-typed values reject values outside the union.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'DictValueObject value <<<.*>>> must be of type <<<int \| str>>> type\. Got <<<.*>>> type\.',
    ):
        StrIntOrStrValueDictValueObject(value={'a': 1, 'b': 2.5})  # type: ignore[dict-item]


@mark.unit_testing
def test_dict_value_object_union_with_any_key_allows_anything() -> None:
    """
    Test that union containing Any for keys returns early in validation.
    """
    mapping = AnyOrIntKeyDictValueObject(value={1: 1, 'b': 2, 1.5: 3})

    assert len(mapping) == 3


@mark.unit_testing
def test_dict_value_object_union_with_any_value_allows_anything() -> None:
    """
    Test that union containing Any for values returns early in validation.
    """
    mapping = StrIntOrAnyValueDictValueObject(value={'a': 1, 'b': 2.5})

    assert mapping['b'] == 2.5


@mark.unit_testing
def test_dict_value_object_type_label_formats_union_with_any_for_keys() -> None:
    """
    Test that _type_label formats union containing Any for keys.
    """
    mapping = AnyOrIntKeyDictValueObject(value={1: 1})

    assert mapping._type_label(type=mapping._key_type) == 'int | Any'


@mark.unit_testing
def test_dict_value_object_type_label_formats_union_with_any_for_values() -> None:
    """
    Test that _type_label formats union containing Any for values.
    """
    mapping = StrIntOrAnyValueDictValueObject(value={'a': 1})

    assert mapping._type_label(type=mapping._value_type) == 'int | Any'


@mark.unit_testing
def test_dict_value_object_from_primitives_with_primitive_types_keeps_values() -> None:
    """
    Test from_primitives keeps primitive keys and values unchanged.
    """
    mapping = StrIntDictValueObject.from_primitives(value={'a': 1, 'b': 2})

    assert mapping.value == {'a': 1, 'b': 2}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_any_types_keeps_values() -> None:
    """
    Test from_primitives keeps values unchanged when key/value annotations are Any.
    """
    raw = {'a': [1, 2], 3: {'nested': 'value'}}

    mapping = AnyDictValueObject.from_primitives(value=raw)

    assert mapping.value == raw


@mark.unit_testing
def test_dict_value_object_from_primitives_with_value_object_values_builds_instances() -> None:
    """
    Test from_primitives creates ValueObject values.
    """
    mapping = StrValueObjectDict.from_primitives(value={'x': 10, 'y': 20})

    assert all(isinstance(item, SimpleValueObject) for item in mapping.values())
    assert {key: item.value for key, item in mapping.items()} == {'x': 10, 'y': 20}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_value_object_keys_builds_instances() -> None:
    """
    Test from_primitives creates ValueObject keys.
    """
    mapping = ValueObjectIntDict.from_primitives(value={1: 10, 2: 20})

    assert all(isinstance(key, SimpleValueObject) for key in mapping)
    assert {key.value: value for key, value in mapping.items()} == {1: 10, 2: 20}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_base_model_values_builds_instances() -> None:
    """
    Test from_primitives creates BaseModel values from dictionaries.
    """
    mapping = StrModelValueDict.from_primitives(value={'user': {'name': 'alice'}})

    value = next(iter(mapping.values()))

    assert isinstance(value, ModelValue)
    assert value.name == 'alice'


@mark.unit_testing
def test_dict_value_object_from_primitives_with_enum_keys_builds_members() -> None:
    """
    Test from_primitives creates Enum keys from primitive values.
    """
    mapping = EnumIntDict.from_primitives(value={'admin': 1, 'user': 2})

    assert mapping.value == {DummyEnum.ADMIN: 1, DummyEnum.USER: 2}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_enum_values_builds_members() -> None:
    """
    Test from_primitives creates Enum values from primitive values.
    """
    mapping = StrEnumDict.from_primitives(value={'u1': 'active', 'u2': 'inactive'})

    assert mapping.value == {'u1': Status.ACTIVE, 'u2': Status.INACTIVE}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_enumeration_value_object_builds_instances() -> None:
    """
    Test from_primitives creates EnumerationValueObject keys and values from primitive values.
    """
    mapping = StatusEnumValueObjectDict.from_primitives(value={'active': 'inactive'})

    key = next(iter(mapping.keys()))
    value = next(iter(mapping.values()))

    assert isinstance(key, StatusEnumValueObject)
    assert isinstance(value, StatusEnumValueObject)
    assert key.value == Status.ACTIVE
    assert value.value == Status.INACTIVE


@mark.unit_testing
def test_dict_value_object_from_primitives_with_union_key_and_value_returns_raw_items() -> None:
    """
    Test from_primitives keeps raw data when union key/value annotations are used.
    """
    mapping = IntOrStrIntOrStrDictValueObject.from_primitives(value={1: 'a', 'b': 2})

    assert mapping.value == {1: 'a', 'b': 2}


@mark.unit_testing
def test_dict_value_object_from_primitives_with_invalid_enum_key_raises_type_error() -> None:
    """
    Test from_primitives raises when an enum key primitive is invalid.
    """
    with assert_raises(expected_exception=ValueError):
        EnumIntDict.from_primitives(value={'unknown': 1})


@mark.unit_testing
def test_dict_value_object_from_primitives_with_invalid_enum_value_raises_type_error() -> None:
    """
    Test from_primitives raises when an enum value primitive is invalid.
    """
    with assert_raises(expected_exception=ValueError):
        StrEnumDict.from_primitives(value={'u1': 'unknown'})


@mark.unit_testing
def test_dict_value_object_to_primitives_with_primitive_types() -> None:
    """
    Test to_primitives with primitive types (int, float, str, bool, None).
    """
    dict_value_object = StrIntDictValueObject(value={'a': 1, 'b': 2, 'c': 3})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'a': 1, 'b': 2, 'c': 3}
    assert isinstance(primitives, dict)


@mark.unit_testing
def test_dict_value_object_to_primitives_with_value_object_values() -> None:
    """
    Test to_primitives correctly extracts values from ValueObject instances.
    """
    dict_value_object = StrValueObjectDict(value={'x': SimpleValueObject(value=10), 'y': SimpleValueObject(value=20)})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'x': 10, 'y': 20}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_base_model_values() -> None:
    """
    Test to_primitives correctly converts BaseModel values to their primitive dictionaries.
    """
    dict_value_object = StrNestedModelDict(value={'first': NestedModel(code=1), 'second': NestedModel(code=2)})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'first': {'code': 1}, 'second': {'code': 2}}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_custom_object_values() -> None:
    """
    Test to_primitives converts unknown object values to strings.
    """
    dict_value_object = StrCustomObjectDict(value={'obj1': CustomObject(), 'obj2': CustomObject()})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'obj1': 'custom-object', 'obj2': 'custom-object'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_value_object_keys() -> None:
    """
    Test to_primitives correctly extracts values from ValueObject keys.
    """
    dict_value_object = ValueObjectIntDict(value={SimpleValueObject(value=1): 10, SimpleValueObject(value=2): 20})

    primitives = dict_value_object.to_primitives()

    assert primitives == {1: 10, 2: 20}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_enum_keys() -> None:
    """
    Test to_primitives correctly extracts values from Enum keys.
    """
    dict_value_object = EnumIntDict(value={DummyEnum.ADMIN: 1, DummyEnum.USER: 2})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'admin': 1, 'user': 2}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_enum_values() -> None:
    """
    Test to_primitives correctly extracts values from Enum values.
    """
    dict_value_object = StrEnumDict(value={'user1': Status.ACTIVE, 'user2': Status.INACTIVE})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'user1': 'active', 'user2': 'inactive'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_nested_collections() -> None:
    """
    Test to_primitives handles nested collections (lists, dicts) as values.
    """
    dict_value_object = AnyValueDictValueObject(value={'nums1': [1, 2, 3], 'nums2': [4, 5, 6]})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'nums1': [1, 2, 3], 'nums2': [4, 5, 6]}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_empty_dict() -> None:
    """
    Test to_primitives returns an empty dict when the value object is empty.
    """
    dict_value_object = StrIntDictValueObject(value={})

    primitives = dict_value_object.to_primitives()

    assert primitives == {}
    assert isinstance(primitives, dict)


@mark.unit_testing
def test_dict_value_object_to_primitives_with_none_values() -> None:
    """
    Test to_primitives correctly handles None values.
    """
    dict_value_object = AnyValueDictValueObject(value={'a': 1, 'b': None, 'c': 3})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'a': 1, 'b': None, 'c': 3}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_bytes_values() -> None:
    """
    Test to_primitives correctly handles bytes values.
    """
    dict_value_object = AnyValueDictValueObject(value={'data1': b'hello', 'data2': b'world'})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'data1': b'hello', 'data2': b'world'}


@mark.unit_testing
def test_dict_value_object_to_primitives_preserves_all_entries() -> None:
    """
    Test to_primitives preserves all key-value pairs.
    """
    dict_value_object = StrIntDictValueObject(value={'z': 26, 'a': 1, 'm': 13})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'z': 26, 'a': 1, 'm': 13}
    assert len(primitives) == 3


@mark.unit_testing
def test_dict_value_object_to_primitives_with_boolean_values() -> None:
    """
    Test to_primitives correctly handles boolean values.
    """
    dict_value_object = AnyValueDictValueObject(value={'active': True, 'deleted': False, 'enabled': True})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'active': True, 'deleted': False, 'enabled': True}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_float_values() -> None:
    """
    Test to_primitives correctly handles float values.
    """
    dict_value_object = AnyValueDictValueObject(value={'pi': 3.14, 'e': 2.71, 'phi': 1.61})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'pi': 3.14, 'e': 2.71, 'phi': 1.61}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_string_keys_and_values() -> None:
    """
    Test to_primitives correctly handles string keys and values.
    """
    dict_value_object = AnyValueDictValueObject(value={'hello': 'world', 'foo': 'bar', 'key': 'value'})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'hello': 'world', 'foo': 'bar', 'key': 'value'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_integer_keys() -> None:
    """
    Test to_primitives correctly handles integer keys.
    """
    dict_value_object = AnyDictValueObject(value={1: 'one', 2: 'two', 3: 'three'})

    primitives = dict_value_object.to_primitives()

    assert primitives == {1: 'one', 2: 'two', 3: 'three'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_non_base_model_having_to_primitives_as_key() -> None:
    """
    Test to_primitives calls to_primitives on keys that have the method but aren't BaseModel.
    """
    key1 = CustomKeyWithToPrimitives(value='a')
    key2 = CustomKeyWithToPrimitives(value='b')
    dict_value_object = CustomKeyWithToPrimitivesIntDict(value={key1: 1, key2: 2})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'custom-a': 1, 'custom-b': 2}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_non_base_model_having_to_primitives_as_value() -> None:
    """
    Test to_primitives calls to_primitives on values that have the method but aren't BaseModel.
    """
    dict_value_object = StrCustomValueDict(
        value={'a': CustomValueWithToPrimitives(data='x'), 'b': CustomValueWithToPrimitives(data='y')}
    )

    primitives = dict_value_object.to_primitives()

    assert primitives == {'a': 'custom-x', 'b': 'custom-y'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_value_object_key_containing_enum() -> None:
    """
    Test to_primitives extracts enum value when key is ValueObject containing an Enum.
    """
    dict_value_object = StatusValueObjectIntDict(
        value={StatusValueObject(value=Status.ACTIVE): 1, StatusValueObject(value=Status.INACTIVE): 2}
    )

    primitives = dict_value_object.to_primitives()

    assert primitives == {'active': 1, 'inactive': 2}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_value_object_value_containing_enum() -> None:
    """
    Test to_primitives extracts enum value when value is ValueObject containing an Enum.
    """
    # Reuse Status enum with ValueObject inline
    status_vo1 = StatusValueObject(value=Status.ACTIVE)
    status_vo2 = StatusValueObject(value=Status.INACTIVE)
    dict_value_object = AnyValueDictValueObject(value={'task1': status_vo1, 'task2': status_vo2})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'task1': 'active', 'task2': 'inactive'}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_collection_keys() -> None:
    """
    Test to_primitives preserves collection type keys as-is.
    """
    dict_value_object = AnyKeyDictValueObject(value={(1, 2): 10, (3, 4): 20})

    primitives = dict_value_object.to_primitives()

    assert primitives == {(1, 2): 10, (3, 4): 20}


@mark.unit_testing
def test_dict_value_object_to_primitives_with_custom_object_keys() -> None:
    """
    Test to_primitives converts unknown object keys to strings.
    """
    key1 = CustomKey(name='alpha')
    key2 = CustomKey(name='beta')
    dict_value_object = CustomKeyIntDict(value={key1: 1, key2: 2})

    primitives = dict_value_object.to_primitives()

    assert primitives == {'CustomKey(alpha)': 1, 'CustomKey(beta)': 2}
