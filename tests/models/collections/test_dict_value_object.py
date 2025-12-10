"""
Test DictValueObject value object.
"""

from typing import Any, ForwardRef, TypeVar

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

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
