"""
Test union value object module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from typing import Any, ForwardRef, NoReturn, TypeVar, Union, cast
from unittest.mock import patch

from pytest import mark, raises as assert_raises

from value_object_pattern import BaseModel, EnumerationValueObject, UnionValueObject, ValueObject, validation
from value_object_pattern.models.union_value_object import _UnionValueObjectAlias
from value_object_pattern.usables import IntegerValueObject, StringValueObject

TGenericUnion = TypeVar('TGenericUnion')


class LongStringValueObject(ValueObject[str]):
    """
    String value object that requires at least 4 characters.
    """

    @validation(order=0)
    def _ensure_value_is_string(self, value: str) -> None:
        """
        Ensures the provided value is a string.
        """
        if not isinstance(value, str):
            raise TypeError(f'LongStringValueObject value <<<{value}>>> must be a string. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_value_is_long_enough(self, value: str) -> None:
        """
        Ensures the provided value has at least 4 characters.
        """
        if len(value) < 4:
            raise ValueError(f'LongStringValueObject value <<<{value}>>> must have at least 4 characters.')


class Tag(BaseModel):
    """
    Simple base model used in union tests.
    """

    def __init__(self, name: str) -> None:
        """
        Model constructor.
        """
        self.name = name


class Status(Enum):
    """
    Enumeration used in union tests.
    """

    ON = 'on'
    OFF = 'off'


class StatusValueObject(EnumerationValueObject[Status]):
    """
    Enumeration value object for Status.
    """


class StringOrIntegerValueObject(UnionValueObject[LongStringValueObject | IntegerValueObject]):
    """
    Union value object that accepts long strings or integers.
    """


class CustomUnionTypeError(TypeError):
    """
    Custom error used to verify UnionValueObject error-hook delegation.
    """


class CustomErrorUnionValueObject(UnionValueObject[int | str]):
    """
    Union value object with a custom type error.
    """

    @override
    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raise the custom union type error.
        """
        raise CustomUnionTypeError(value)


class ModelOrEnumOrValueObject(UnionValueObject[Tag | Status | LongStringValueObject]):
    """
    Union value object that accepts BaseModel, Enum, or ValueObject values.
    """


class ModelOrEnumerationValueObject(UnionValueObject[Tag | StatusValueObject]):
    """
    Union value object that accepts a BaseModel or EnumerationValueObject.
    """


class IntOrAnyUnionValueObject(UnionValueObject[int | Any]):
    """
    Union value object used to exercise Any handling.
    """


class IntOrStrUnionValueObject(UnionValueObject[int | str]):
    """
    Union value object used to test primitive unions with int.
    """


class IntOrBoolUnionValueObject(UnionValueObject[int | bool]):
    """
    Union value object used to test explicit int | bool unions.
    """


class ModelOrEnumValueObject(UnionValueObject[Tag | Status]):
    """
    Union value object used to test direct Enum candidates.
    """


class AnyOnlyUnionValueObject(UnionValueObject[Any]):
    """
    Union value object with only Any as allowed type.
    """


class SingleIntUnionValueObject(UnionValueObject[int]):
    """
    Union value object with a single primitive candidate.
    """


class GenericTypedUnionValueObject(UnionValueObject[TGenericUnion]):
    """
    Generic union value object to exercise TypeVar subclass registration.
    """


class _HelperBase:
    """
    Helper base class used to exercise __orig_bases__ iteration branches.
    """


class MixedBasesUnionValueObject(_HelperBase, UnionValueObject[int]):
    """
    Union value object with an extra generic base.
    """


class NamePayloadValueObject(ValueObject[dict[str, str]]):
    """
    Wrapper value object to test unwrapping into BaseModel primitives.
    """


@mark.unit_testing
def test_union_value_object_accepts_first_valid_candidate() -> None:
    """
    Test that the union stores the value as the first candidate that validates.
    """
    union = StringOrIntegerValueObject(value=cast(Any, 'hello'))

    assert isinstance(union.value, LongStringValueObject)
    assert union.value.value == 'hello'


@mark.unit_testing
def test_union_value_object_falls_back_when_first_candidate_fails() -> None:
    """
    Test that a later candidate is used when the first candidate fails.
    """
    union = StringOrIntegerValueObject(value=cast(Any, 42))

    assert isinstance(union.value, IntegerValueObject)
    assert union.value.value == 42


@mark.unit_testing
def test_union_value_object_raises_type_error_when_no_candidate_matches() -> None:
    """
    Test that a TypeError is raised when every union candidate fails.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringOrIntegerValueObject value <<<abc>>> must be of type <<<LongStringValueObject \| IntegerValueObject>>> type\. Got <<<str>>> type\.',  # noqa: E501
    ):
        StringOrIntegerValueObject(value=cast(Any, 'abc'))


@mark.unit_testing
def test_union_value_object_delegates_failed_candidates_to_custom_error_hook() -> None:
    """
    Test that a subclass can customize the error raised when no union candidate matches.
    """
    with assert_raises(expected_exception=CustomUnionTypeError):
        CustomErrorUnionValueObject(value=cast(Any, None))


@mark.unit_testing
def test_union_value_object_converts_base_model_from_primitives() -> None:
    """
    Test that BaseModel candidates are created from primitives dictionaries.
    """
    union = ModelOrEnumOrValueObject(value=cast(Any, {'name': 'feature'}))

    assert isinstance(union.value, Tag)
    assert union.value.name == 'feature'


@mark.unit_testing
def test_union_value_object_converts_enum_from_raw_value() -> None:
    """
    Test that Enum candidates accept raw enum values.
    """
    union = ModelOrEnumOrValueObject(value=cast(Any, 'on'))

    assert union.value is Status.ON


@mark.unit_testing
def test_union_value_object_converts_enumeration_value_object() -> None:
    """
    Test that EnumerationValueObject candidates are supported inside the union.
    """
    union = ModelOrEnumerationValueObject(value=cast(Any, 'off'))

    assert isinstance(union.value, StatusValueObject)
    assert union.value.value is Status.OFF


@mark.unit_testing
def test_union_value_object_from_primitives_uses_union_conversion() -> None:
    """
    Test that from_primitives creates the proper union candidate.
    """
    union = ModelOrEnumerationValueObject.from_primitives(value={'name': 'task'})

    assert isinstance(union.value, Tag)
    assert union.value.name == 'task'


@mark.unit_testing
def test_union_value_object_union_with_any_allows_anything() -> None:
    """
    Test that union containing Any accepts any value.
    """
    payload = {'name': 'dynamic'}
    union = IntOrAnyUnionValueObject(value=payload)

    assert union.value is payload


@mark.unit_testing
def test_union_value_object_rejects_bool_when_type_is_int() -> None:
    """
    Test that UnionValueObject[int | str] rejects booleans.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntOrStrUnionValueObject value <<<True>>> must be of type <<<int \| str>>> type\. Got <<<bool>>> type\.',  # noqa: E501
    ):
        IntOrStrUnionValueObject(value=True)


@mark.unit_testing
def test_union_value_object_accepts_explicit_int_or_bool_union() -> None:
    """
    Test that UnionValueObject[int | bool] accepts both explicit candidates.
    """
    int_value = IntOrBoolUnionValueObject(value=7)
    bool_value = IntOrBoolUnionValueObject(value=False)

    assert int_value.value == 7
    assert bool_value.value is False


@mark.unit_testing
def test_union_value_object_unwraps_value_object_for_primitive_candidate() -> None:
    """
    Test that primitive candidates use the inner value from incoming ValueObject wrappers.
    """
    wrapped = IntegerValueObject(value=33)
    union = IntOrStrUnionValueObject(value=cast(Any, wrapped))

    assert union.value == 33
    assert isinstance(union.value, int)


@mark.unit_testing
def test_union_value_object_unwraps_value_object_for_base_model_candidate() -> None:
    """
    Test that BaseModel candidates can be built from ValueObject-wrapped dictionaries.
    """
    payload = NamePayloadValueObject(value={'name': 'refactor'})
    union = ModelOrEnumOrValueObject(value=cast(Any, payload))

    assert isinstance(union.value, Tag)
    assert union.value.name == 'refactor'


@mark.unit_testing
def test_union_value_object_unwraps_enumeration_value_object_for_enum_candidate() -> None:
    """
    Test that Enum candidates can match from an incoming EnumerationValueObject.
    """
    wrapped_status = StatusValueObject(value='on')
    union = ModelOrEnumValueObject(value=cast(Any, wrapped_status))

    assert union.value is Status.ON


@mark.unit_testing
def test_union_value_object_init_subclass_keeps_typevar_for_generic_unions() -> None:
    """
    Test that __init_subclass__ stores TypeVar on generic union subclasses.
    """
    assert GenericTypedUnionValueObject._type is TGenericUnion  # type: ignore[misc]


@mark.unit_testing
def test_union_value_object_init_subclass_skips_non_union_bases_before_union_base() -> None:
    """
    Test that __init_subclass__ handles non-union bases in __orig_bases__ before the union base.
    """
    union = MixedBasesUnionValueObject(value=1)

    assert union.value == 1


@mark.unit_testing
def test_union_value_object_requires_parameterization() -> None:
    """
    Test that __init_subclass__ raises TypeError when class is not parameterized.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject must be parameterized, e\.g\. "class IntOrStrValueObject\(UnionValueObject\[int \| str\]\)".',  # noqa: E501
    ):

        class _InvalidUnionValueObject(UnionValueObject):  # type: ignore[type-arg]  # pragma: no cover
            pass


@mark.unit_testing
def test_union_value_object_requires_type_argument_to_be_type() -> None:
    """
    Test that __init_subclass__ raises TypeError when generic argument is not a type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject\[\.\.\.\] <<<.*>>> must be a type\. Got <<<.*>>> type\.',
    ):

        class _InvalidTypeUnionValueObject(UnionValueObject[cast(Any, 1)]):  # type: ignore[misc]  # pragma: no cover
            pass


@mark.unit_testing
def test_union_value_object_with_only_any_returns_raw_value() -> None:
    """
    Test that UnionValueObject[Any] returns the original value without coercion.
    """
    payload = {'name': 'dynamic'}
    union = AnyOnlyUnionValueObject(value=payload)

    assert union.value is payload


@mark.unit_testing
def test_union_value_object_unwrap_candidate_value_unwraps_enum_by_default() -> None:
    """
    Test that _unwrap_candidate_value converts enum members to their primitive value by default.
    """
    union = ModelOrEnumValueObject(value=Tag(name='demo'))

    assert union._unwrap_candidate_value(value=Status.ON) == 'on'


@mark.unit_testing
def test_union_value_object_coerce_value_to_union_expected_type_branch() -> None:
    """
    Test _coerce_value_to_type union-recursion branch raises TypeError when candidates fail.
    """
    union = IntOrStrUnionValueObject(value=1)

    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject value <<<1\.5>>> must be of type <<<.*>>> type\. Got <<<float>>> type\.',
    ):
        union._coerce_value_to_type(value=1.5, expected_type=int | str)


@mark.unit_testing
def test_union_value_object_coerce_none_expected_type_branch() -> None:
    """
    Test _coerce_value_to_type branch for type(None) on both matching and non-matching values.
    """
    union = IntOrStrUnionValueObject(value=1)

    assert union._coerce_value_to_type(value=None, expected_type=type(None)) is None

    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject value <<<x>>> must be of type <<<None>>> type\. Got <<<str>>> type\.',
    ):
        union._coerce_value_to_type(value='x', expected_type=type(None))


@mark.unit_testing
def test_union_value_object_coerce_non_class_expected_type_branch_raises() -> None:
    """
    Test _coerce_value_to_type raises TypeError when non-class expected type does not match.
    """
    union = IntOrStrUnionValueObject(value=1)

    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject value <<<x>>> must be of type <<<not-a-type>>> type\. Got <<<str>>> type\.',
    ):
        union._coerce_value_to_type(value='x', expected_type=cast(Any, 'not-a-type'))


@mark.unit_testing
def test_union_value_object_coerce_non_class_expected_type_branch_accepts_match() -> None:
    """
    Test _coerce_value_to_type returns candidate when non-class expected type matches.
    """
    union = IntOrStrUnionValueObject(value=1)

    assert union._coerce_value_to_type(value='x', expected_type=(str, int)) == 'x'


@mark.unit_testing
def test_union_value_object_coerce_value_object_branch_raises_when_conversion_returns_wrong_type() -> None:
    """
    Test _coerce_value_to_type ValueObject branch raises when conversion does not return expected type.
    """
    union = StringOrIntegerValueObject(value=cast(Any, 7))

    with (
        patch('value_object_pattern.models.union_value_object.from_primitive', return_value=object()),
        assert_raises(
            expected_exception=TypeError,
            match=r'UnionValueObject value <<<.*>>> must be of type <<<LongStringValueObject>>> type\. Got <<<object>>> type\.',  # noqa: E501
        ),
    ):
        union._coerce_value_to_type(value='hello', expected_type=LongStringValueObject)


@mark.unit_testing
def test_union_value_object_coerce_enum_branch_raises_when_conversion_returns_wrong_type() -> None:
    """
    Test _coerce_value_to_type Enum branch raises when conversion does not return expected enum.
    """
    union = ModelOrEnumValueObject(value=Tag(name='demo'))

    with (
        patch('value_object_pattern.models.union_value_object.from_primitive', return_value='not-enum'),
        assert_raises(
            expected_exception=TypeError,
            match=r'UnionValueObject value <<<on>>> must be of type <<<Status>>> type\. Got <<<str>>> type\.',
        ),
    ):
        union._coerce_value_to_type(value='on', expected_type=Status)


@mark.unit_testing
def test_union_value_object_raises_when_allowed_types_are_empty_due_to_patched_typing_helpers() -> None:
    """
    Test fallback path that calls _raise_value_is_not_of_type when no allowed types are produced.
    """
    with (
        patch('value_object_pattern.models.union_value_object.get_origin', return_value=Union),
        patch('value_object_pattern.models.union_value_object.get_args', return_value=()),
        assert_raises(expected_exception=TypeError),
    ):
        IntOrStrUnionValueObject(value=cast(Any, 'invalid'))


@mark.unit_testing
def test_union_value_object_type_label_non_union_and_any_and_format_fallback() -> None:
    """
    Test _type_label and _format_single_type for non-union, Any, and fallback typing values.
    """
    single_int = SingleIntUnionValueObject(value=1)
    any_union = AnyOnlyUnionValueObject(value='x')

    assert single_int._type_label() == 'int'
    assert any_union._type_label() == 'Any'
    assert single_int._format_single_type(type=ForwardRef('SomeType')) == "ForwardRef('SomeType')"


@mark.unit_testing
def test_union_value_object_inline_constructor_stores_first_matching_value_object_candidate() -> None:
    """
    Test that UnionValueObject[T](...) works without declaring a named subclass.
    """
    value = UnionValueObject[IntegerValueObject | StringValueObject](value=cast(Any, 1))

    assert isinstance(value.value, IntegerValueObject)
    assert value.value.value == 1


@mark.unit_testing
def test_union_value_object_inline_constructor_falls_back_to_later_candidate() -> None:
    """
    Test that inline construction preserves union candidate fallback behavior.
    """
    value = UnionValueObject[IntegerValueObject | StringValueObject](value=cast(Any, 'name'))

    assert isinstance(value.value, StringValueObject)
    assert value.value.value == 'name'


@mark.unit_testing
def test_union_value_object_inline_constructor_reuses_runtime_class_for_equality() -> None:
    """
    Test that repeated inline construction uses the same runtime class for equivalent aliases.
    """
    first = UnionValueObject[int | str](value=1)
    second = UnionValueObject[int | str](value=1)

    assert first == second


@mark.unit_testing
def test_union_value_object_inline_from_primitives_uses_union_conversion() -> None:
    """
    Test that inline aliases expose class helpers through the generated runtime subclass.
    """
    value = UnionValueObject[IntegerValueObject | StringValueObject].from_primitives(value=1)

    assert isinstance(value.value, IntegerValueObject)
    assert value.value.value == 1


@mark.unit_testing
def test_union_value_object_inline_constructor_rejects_invalid_type_argument() -> None:
    """
    Test that inline construction preserves type argument validation.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject\[\.\.\.\] <<<1>>> must be a type\. Got <<<int>>> type\.',
    ):
        invalid_union_value_object = cast(Any, UnionValueObject)[1]
        invalid_union_value_object(value=1)


@mark.unit_testing
def test_union_value_object_inline_constructor_rejects_invalid_value() -> None:
    """
    Test that inline construction reports union validation errors for unmatched values.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UnionValueObject\[int \| str\] value <<<.*>>> must be of type <<<int \| str>>> type\. Got <<<object>>> type\.',  # noqa: E501
    ):
        UnionValueObject[int | str](value=cast(Any, object()))


@mark.unit_testing
def test_union_value_object_inline_constructor_allows_any() -> None:
    """
    Test that inline construction preserves Any handling.
    """
    payload = {'name': 'dynamic'}
    value = UnionValueObject[Any](value=payload)

    assert value.value is payload


@mark.unit_testing
def test_union_value_object_inline_type_argument_label_uses_string_fallback() -> None:
    """
    Test that generated inline class labels handle type-like objects without names.
    """
    assert _UnionValueObjectAlias._format_type_argument(type=ForwardRef('SomeType')) == "ForwardRef('SomeType')"
