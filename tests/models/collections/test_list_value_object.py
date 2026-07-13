"""
Test ListValueObject value object.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from typing import Any, ForwardRef, NoReturn, TypeVar, cast

from object_mother_pattern import IntegerMother
from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from value_object_pattern import BaseModel, ValueObject
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.models.collections.list_value_object import _ListValueObjectAlias


class IntListValueObject(ListValueObject[int]):
    """
    List value object storing integers.
    """


class CustomListTypeError(TypeError):
    """
    Custom error used to verify ListValueObject error-hook delegation.
    """


class CustomErrorListValueObject(ListValueObject[int]):
    """
    List value object with a custom container type error.
    """

    @override
    def _raise_value_is_not_list(self, value: Any) -> NoReturn:
        """
        Raise the custom list type error.
        """
        raise CustomListTypeError(value)


class Age(ValueObject[int]):
    """
    Value object used to test conversions from primitives.
    """


class AgeListValueObject(ListValueObject[Age]):
    """
    List value object storing Age instances.
    """


class IntStrListValueObject(ListValueObject[int | str]):
    """
    List value object storing ints or strings.
    """


class AnyOrIntListValueObject(ListValueObject[int | Any]):
    """
    List value object storing ints or anything (exercises union with Any).
    """


class ObjOrIntListValueObject(ListValueObject[int | object]):
    """
    List value object storing ints or any object (used to exercise union conversion path).
    """


class Tag(BaseModel):
    """
    Simple BaseModel used to exercise from_primitives conversions.
    """

    def __init__(self, name: str) -> None:
        """
        Tag model constructor.
        """
        self.name = name


class TagListValueObject(ListValueObject[Tag]):
    """
    List value object storing Tag models.
    """


class TagStatus(Enum):
    """
    Enum used to validate union conversion in list from_primitives.
    """

    OPEN = 'open'
    CLOSED = 'closed'


class TagOrStatusListValueObject(ListValueObject[Tag | TagStatus]):
    """
    List value object storing Tag models or TagStatus members.
    """


class AnyListValueObject(ListValueObject[Any]):
    """
    List value object storing any items (used for representation and conversion coverage).
    """


class Color(Enum):
    """
    Simple Enum used to exercise representation coverage.
    """

    RED = 'red'
    BLUE = 'blue'


class Holder:
    """
    Simple class holding an Enum used to exercise representation coverage.
    """

    def __init__(self, value: Enum) -> None:
        """
        Simple holder constructor.
        """
        self.value = value


class PlainObject:
    """
    Simple class used to exercise representation coverage.
    """

    @override
    def __str__(self) -> str:
        """
        String representation of the plain object.
        """
        return 'PlainObjectStr'

    @override
    def __repr__(self) -> str:
        """
        Official string representation of the plain object.
        """
        return 'PlainObjectRepr'


class CustomObj:
    """
    Custom object for testing.
    """

    @override
    def __repr__(self) -> str:
        """
        Custom representation.
        """
        return 'custom-object'


class CustomObjectList(ListValueObject[CustomObj]):
    """
    List value object storing CustomObj instances.
    """


class NestedListValueObject(ListValueObject[list[int]]):
    """
    List value object storing lists of integers.
    """


class MixedValueObjectList(ListValueObject[int | Age | Tag]):
    """
    List value object storing mixed types.
    """


class NoneableListValueObject(ListValueObject[int | None]):
    """
    List value object that can store None.
    """


class BytesListValueObject(ListValueObject[bytes]):
    """
    List value object storing bytes.
    """


class EnumList(ListValueObject[Color]):
    """
    List value object storing Enum instances.
    """


class BoolListValueObject(ListValueObject[bool]):
    """
    List value object storing booleans.
    """


class FloatListValueObject(ListValueObject[float]):
    """
    List value object storing floats.
    """


class StrListValueObject(ListValueObject[str]):
    """
    List value object storing strings.
    """


@mark.unit_testing
def test_list_value_object_contains_existing_item() -> None:
    """
    Test that __contains__ returns True for existing items.
    """
    values = [IntegerMother.create()]

    assert values[0] in IntListValueObject(value=values)


@mark.unit_testing
def test_list_value_object_iter_returns_items() -> None:
    """
    Test that __iter__ returns the underlying items.
    """
    values = [IntegerMother.create(), IntegerMother.create()]

    assert list(IntListValueObject(value=values)) == values


@mark.unit_testing
def test_list_value_object_len_counts_items() -> None:
    """
    Test that __len__ returns the list length.
    """
    values = [IntegerMother.create(), IntegerMother.create(), IntegerMother.create()]

    assert len(IntListValueObject(value=values)) == 3


@mark.unit_testing
def test_list_value_object_reversed_returns_reversed_items() -> None:
    """
    Test that __reversed__ yields items in reverse order.
    """
    values = [1, 2, 3]

    assert list(reversed(IntListValueObject(value=values))) == [3, 2, 1]


@mark.unit_testing
def test_list_value_object_str_matches_underlying_list() -> None:
    """
    Test that __str__ mirrors the underlying list.
    """
    values = [1, 2, 3]

    assert str(IntListValueObject(value=values)) == str(values)


@mark.unit_testing
def test_list_value_object_repr_matches_underlying_list() -> None:
    """
    Test that __repr__ mirrors the underlying list.
    """
    values = [1, 2]

    assert repr(IntListValueObject(value=values)) == repr(values)


@mark.unit_testing
def test_list_value_object_is_empty_returns_true_for_empty_list() -> None:
    """
    Test that is_empty returns True for an empty list.
    """
    assert IntListValueObject(value=[]).is_empty()


@mark.unit_testing
def test_list_value_object_is_empty_returns_false_for_non_empty_list() -> None:
    """
    Test that is_empty returns False for a non-empty list.
    """
    assert not IntListValueObject(value=[IntegerMother.create(value=1)]).is_empty()


@mark.unit_testing
def test_list_value_object_requires_parameterization() -> None:
    """
    Test that __init_subclass__ raises TypeError when the class is not parameterized.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject must be parameterized, e\.g\. "class InIntListValueObject\(ListValueObject\[int\]\)".',
    ):

        class _InvalidListValueObject(ListValueObject):  # type: ignore[type-arg]  # pragma: no cover
            pass


@mark.unit_testing
def test_list_value_object_requires_type_argument_to_be_type() -> None:
    """
    Test that __init_subclass__ raises TypeError when the generic argument is not a type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject\[\.\.\.\] <<<.*>>> must be a type\. Got <<<.*>>> type\.',
    ):

        class _InvalidTypeListValueObject(ListValueObject[IntegerMother.create()]):  # type: ignore[misc]  # pragma: no cover
            pass


@mark.unit_testing
def test_list_value_object_allows_typevar_parameterization() -> None:
    """
    Test that __init_subclass__ accepts a TypeVar argument without raising.
    """
    TItem = TypeVar('TItem')

    class _GenericListValueObject(ListValueObject[TItem]):  # pragma: no cover
        pass

    assert _GenericListValueObject._type is TItem  # type: ignore[misc]


@mark.unit_testing
def test_list_value_object_raises_type_error_when_value_is_not_list() -> None:
    """
    Test that a TypeError is raised when the provided value is not a list.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject value <<<.*>>> must be a list\. Got <<<.*>>> type\.',
    ):
        IntListValueObject(value=BaseMother.invalid_type(remove_types=(list,)))


@mark.unit_testing
def test_list_value_object_raises_type_error_when_item_has_wrong_type() -> None:
    """
    Test that a TypeError is raised when list items do not match the annotated type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        IntListValueObject(value=[1, IntegerMother.invalid_type(remove_types=(bool,))])


@mark.unit_testing
def test_list_value_object_repr_cover_all_item_kinds() -> None:
    """
    Test __repr__ branches with BaseModel, Enum, ValueObject, has-value, primitives, collections, and others.
    """
    sequence = AnyListValueObject(
        value=[
            Tag(name='bug'),
            Color.RED,
            Age(value=42),
            Holder(value=Color.BLUE),
            'x',
            (1, 2),
            PlainObject(),
        ]
    )

    assert repr(sequence) == str(["Tag(name='bug')", 'red', '42', "'blue'", 'x', '(1, 2)', 'PlainObjectRepr'])


@mark.unit_testing
def test_list_value_object_str_cover_all_item_kinds() -> None:
    """
    Test __str__ branches with BaseModel, Enum, ValueObject, has-value, primitives, collections, and others.
    """
    sequence = AnyListValueObject(
        value=[
            Tag(name='bug'),
            Color.RED,
            Age(value=42),
            Holder(value=Color.BLUE),
            'x',
            (1, 2),
            PlainObject(),
        ]
    )

    assert str(sequence) == str(['Tag(name=bug)', 'red', '42', 'blue', 'x', '(1, 2)', 'PlainObjectStr'])


@mark.unit_testing
def test_list_value_object_accepts_union_type() -> None:
    """
    Test that ListValueObject accepts union element types (int | str).
    """
    sequence = IntStrListValueObject(value=[1, 'a', 2])

    assert list(sequence) == [1, 'a', 2]


@mark.unit_testing
def test_list_value_object_union_add_and_extend_updates_values() -> None:
    """
    Test that add/extend work with union element types.
    """
    sequence = IntStrListValueObject(value=[1])

    updated = sequence.add(item='a').extend(items=[2, 'b'])

    assert updated.value == [1, 'a', 2, 'b']


@mark.unit_testing
def test_list_value_object_union_add_and_extend_preserves_original_value() -> None:
    """
    Test that add/extend do not mutate the original instance.
    """
    sequence = IntStrListValueObject(value=[1])
    sequence.add(item='a').extend(items=[2])

    assert sequence.value == [1]


@mark.unit_testing
def test_list_value_object_union_rejects_out_of_union_type() -> None:
    """
    Test that union-typed ListValueObject rejects items outside the union.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<.*>>> must be of type <<<int \| str>>> type\. Got <<<.*>>> type\.',
    ):
        IntStrListValueObject(value=[1, IntegerMother.invalid_type(remove_types=(bool, str))])


@mark.unit_testing
def test_list_value_object_union_rejects_bool_when_union_contains_int() -> None:
    """
    Test that bool values are rejected for int | str unions.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<True>>> must be of type <<<int \| str>>> type\. Got <<<bool>>> type\.',
    ):
        IntStrListValueObject(value=[1, True])


@mark.unit_testing
def test_list_value_object_union_with_any_allows_anything() -> None:
    """
    Test that union containing Any returns early in validation.
    """
    value = BaseMother.invalid_type(remove_types=(int, bool))
    instance = AnyOrIntListValueObject(value=[value, 1])

    assert value in instance


@mark.unit_testing
def test_list_value_object_union_convert_from_primitives_returns_value_unchanged() -> None:
    """
    Test that _convert_from_primitives returns raw value for unions.
    """
    value = BaseMother.invalid_type(remove_types=(int, bool))
    sequence = ObjOrIntListValueObject(value=[1])

    assert sequence.add_from_primitives(item=value).value[-1] is value


@mark.unit_testing
def test_list_value_object_from_primitives_converts_union_items_to_matching_candidates() -> None:
    """
    Test from_primitives converts each union item to the first matching candidate.
    """
    sequence = TagOrStatusListValueObject.from_primitives(value=[{'name': 'feature'}, 'open'])

    assert isinstance(sequence.value[0], Tag)
    assert sequence.value[0].name == 'feature'
    assert sequence.value[1] is TagStatus.OPEN


@mark.unit_testing
def test_list_value_object_type_label_formats_union_with_any() -> None:
    """
    Test that _type_label formats union containing Any.
    """
    label = AnyOrIntListValueObject(value=[1])._type_label()

    assert label == 'int | Any'


@mark.unit_testing
def test_list_value_object_format_single_type_handles_forward_ref() -> None:
    """
    Test that _format_single_type covers branch without __name__.
    """
    assert AnyListValueObject._format_single_type(type=ForwardRef('SomeType')) == "ForwardRef('SomeType')"


@mark.unit_testing
def test_list_value_object_add_appends_item_to_new_instance_value() -> None:
    """
    Test that add returns a new value object with the item appended.
    """
    updated_sequence = IntListValueObject(value=[1, 2]).add(item=3)

    assert updated_sequence.value == [1, 2, 3]


@mark.unit_testing
def test_list_value_object_add_does_not_mutate_original_value() -> None:
    """
    Test that add leaves the original instance untouched.
    """
    sequence = IntListValueObject(value=[1, 2])
    sequence.add(item=3)

    assert sequence.value == [1, 2]


@mark.unit_testing
def test_list_value_object_add_returns_different_instance() -> None:
    """
    Test that add returns a different instance.
    """
    sequence = IntListValueObject(value=[1, 2])

    assert sequence.add(item=3) is not sequence


@mark.unit_testing
def test_list_value_object_add_from_primitives_converts_value_object_values() -> None:
    """
    Test that add_from_primitives converts primitives to the underlying ValueObject type.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])

    assert [age.value for age in age_list.add_from_primitives(item=20)] == [10, 20]


@mark.unit_testing
def test_list_value_object_add_from_primitives_preserves_original_value() -> None:
    """
    Test that add_from_primitives does not mutate the original list.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])
    age_list.add_from_primitives(item=20)

    assert [age.value for age in age_list] == [10]


@mark.unit_testing
def test_list_value_object_add_raises_type_error_on_wrong_item_type() -> None:
    """
    Test that add raises TypeError when the new item does not match the annotated type.
    """
    sequence = IntListValueObject(value=[1])

    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        sequence.add(item=IntegerMother.invalid_type(remove_types=(bool,)))


@mark.unit_testing
def test_list_value_object_add_from_primitives_raises_type_error_on_wrong_item_type() -> None:
    """
    Test that add_from_primitives raises TypeError when the converted item does not match the annotated type.
    """
    sequence = IntListValueObject(value=[1])

    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        sequence.add_from_primitives(item=IntegerMother.invalid_type(remove_types=(bool,)))


@mark.unit_testing
def test_list_value_object_add_from_primitives_with_any_type_adds_value() -> None:
    """
    Test that add_from_primitives returns the provided value unchanged when the type is Any.
    """
    updated_sequence = AnyListValueObject(value=[]).add_from_primitives(item={'k': 1})

    assert updated_sequence.value == [{'k': 1}]


@mark.unit_testing
def test_list_value_object_add_from_primitives_with_any_type_preserves_original_value() -> None:
    """
    Test that add_from_primitives does not mutate the original when type is Any.
    """
    sequence = AnyListValueObject(value=[])
    sequence.add_from_primitives(item={'k': 1})

    assert sequence.value == []


@mark.unit_testing
def test_list_value_object_extend_appends_items() -> None:
    """
    Test that extend returns a new value object with items appended.
    """
    extended_sequence = IntListValueObject(value=[1]).extend(items=[2, 3])

    assert extended_sequence.value == [1, 2, 3]


@mark.unit_testing
def test_list_value_object_extend_does_not_mutate_original_value() -> None:
    """
    Test that extend leaves the original instance untouched.
    """
    sequence = IntListValueObject(value=[1])
    sequence.extend(items=[2, 3])

    assert sequence.value == [1]


@mark.unit_testing
def test_list_value_object_extend_returns_new_instance() -> None:
    """
    Test that extend returns a different instance.
    """
    sequence = IntListValueObject(value=[1])

    assert sequence.extend(items=[2]) is not sequence


@mark.unit_testing
def test_list_value_object_extend_from_primitives_converts_value_object_values() -> None:
    """
    Test that extend_from_primitives converts primitives to the underlying ValueObject type.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])

    assert [age.value for age in age_list.extend_from_primitives(items=[20, 30])] == [10, 20, 30]


@mark.unit_testing
def test_list_value_object_extend_from_primitives_preserves_original_value() -> None:
    """
    Test that extend_from_primitives does not mutate the original list.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])
    age_list.extend_from_primitives(items=[20, 30])

    assert [age.value for age in age_list] == [10]


@mark.unit_testing
def test_list_value_object_extend_from_primitives_returns_new_instance() -> None:
    """
    Test that extend_from_primitives returns a different instance.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])

    assert age_list.extend_from_primitives(items=[20]) is not age_list


@mark.unit_testing
def test_list_value_object_extend_from_primitives_builds_base_model_list() -> None:
    """
    Test that extend_from_primitives converts primitives to BaseModels when the type exposes from_primitives.
    """
    tag_list = TagListValueObject(value=[Tag(name='feature')])

    assert [tag.name for tag in tag_list.extend_from_primitives(items=[{'name': 'bug'}, {'name': 'chore'}])] == [
        'feature',
        'bug',
        'chore',
    ]


@mark.unit_testing
def test_list_value_object_extend_from_primitives_base_model_preserves_original() -> None:
    """
    Test that extend_from_primitives with BaseModels does not mutate the original list.
    """
    tag_list = TagListValueObject(value=[Tag(name='feature')])
    tag_list.extend_from_primitives(items=[{'name': 'bug'}])

    assert [tag.name for tag in tag_list] == ['feature']


@mark.unit_testing
def test_list_value_object_extend_from_primitives_base_model_returns_new_instance() -> None:
    """
    Test that extend_from_primitives with BaseModels returns a new instance.
    """
    tag_list = TagListValueObject(value=[Tag(name='feature')])

    assert tag_list.extend_from_primitives(items=[{'name': 'bug'}]) is not tag_list


@mark.unit_testing
def test_list_value_object_extend_raises_type_error_on_wrong_item_type() -> None:
    """
    Test that extend raises TypeError when any new item does not match the annotated type.
    """
    sequence = IntListValueObject(value=[1])

    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        sequence.extend(items=[2, IntegerMother.invalid_type(remove_types=(bool,))])


@mark.unit_testing
def test_list_value_object_extend_from_primitives_raises_type_error_on_wrong_item_type() -> None:
    """
    Test that extend_from_primitives raises TypeError when a converted item does not match the annotated type.
    """
    sequence = IntListValueObject(value=[1])

    with assert_raises(
        expected_exception=TypeError,
        match=r'.* value <<<.*>>> must be of type <<<int>>> type\. Got <<<.*>>> type\.',
    ):
        sequence.extend_from_primitives(items=[2, IntegerMother.invalid_type(remove_types=(bool,))])


@mark.unit_testing
def test_list_value_object_delete_removes_first_occurrence() -> None:
    """
    Test that delete removes only the first matching item.
    """
    updated_sequence = IntListValueObject(value=[1, 2, 2, 3]).delete(item=2)

    assert updated_sequence.value == [1, 2, 3]


@mark.unit_testing
def test_list_value_object_delete_does_not_mutate_original_value() -> None:
    """
    Test that delete does not mutate the original list.
    """
    sequence = IntListValueObject(value=[1, 2, 2, 3])
    sequence.delete(item=2)

    assert sequence.value == [1, 2, 2, 3]


@mark.unit_testing
def test_list_value_object_delete_raises_when_item_missing() -> None:
    """
    Test that delete raises a ValueError when the item is not present.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ListValueObject item <<<.*>>> not found in thelist when attempting to delete it.',
    ):
        IntListValueObject(value=[1, 2]).delete(item=3)


@mark.unit_testing
def test_list_value_object_delete_from_primitives_removes_first_occurrence() -> None:
    """
    Test that delete_from_primitives removes the first matching item.
    """
    age_list = AgeListValueObject(value=[Age(value=10), Age(value=20), Age(value=10)])

    assert [age.value for age in age_list.delete_from_primitives(item=10)] == [20, 10]


@mark.unit_testing
def test_list_value_object_delete_from_primitives_preserves_original_value() -> None:
    """
    Test that delete_from_primitives does not mutate the original list.
    """
    age_list = AgeListValueObject(value=[Age(value=10), Age(value=20), Age(value=10)])
    age_list.delete_from_primitives(item=10)

    assert [age.value for age in age_list] == [10, 20, 10]


@mark.unit_testing
def test_list_value_object_delete_from_primitives_returns_new_instance() -> None:
    """
    Test that delete_from_primitives returns a new instance.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])

    assert age_list.delete_from_primitives(item=10) is not age_list


@mark.unit_testing
def test_list_value_object_delete_from_primitives_raises_when_item_missing() -> None:
    """
    Test that delete_from_primitives raises a ValueError when the item is not present.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ListValueObject item <<<.*>>> not found in thelist when attempting to delete it.',
    ):
        AgeListValueObject(value=[Age(value=10)]).delete_from_primitives(item=20)


@mark.unit_testing
def test_list_value_object_delete_all_removes_all_occurrences() -> None:
    """
    Test that delete_all removes every occurrence of the provided items.
    """
    updated_sequence = IntListValueObject(value=[1, 2, 3, 2, 4]).delete_all(items=[2, 4])

    assert updated_sequence.value == [1, 3]


@mark.unit_testing
def test_list_value_object_delete_all_preserves_original_value() -> None:
    """
    Test that delete_all does not mutate the original list.
    """
    sequence = IntListValueObject(value=[1, 2, 3, 2, 4])
    sequence.delete_all(items=[2])

    assert sequence.value == [1, 2, 3, 2, 4]


@mark.unit_testing
def test_list_value_object_delete_all_raises_when_missing_items() -> None:
    """
    Test that delete_all raises a ValueError when any of the items are missing.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ListValueObject item <<<.*>>> not found in thelist when attempting to delete it.',
    ):
        IntListValueObject(value=[1, 2]).delete_all(items=[1, 3])


@mark.unit_testing
def test_list_value_object_delete_all_from_primitives_removes_all_occurrences() -> None:
    """
    Test that delete_all_from_primitives removes every matching item converted from primitives.
    """
    updated_age_list = AgeListValueObject(
        value=[Age(value=10), Age(value=20), Age(value=30), Age(value=20), Age(value=40)]
    ).delete_all_from_primitives(items=[20, 30])

    assert [age.value for age in updated_age_list] == [10, 40]


@mark.unit_testing
def test_list_value_object_delete_all_from_primitives_preserves_original_values() -> None:
    """
    Test that delete_all_from_primitives does not mutate the original list.
    """
    age_list = AgeListValueObject(value=[Age(value=10), Age(value=20), Age(value=30), Age(value=20), Age(value=40)])
    age_list.delete_all_from_primitives(items=[20])

    assert [age.value for age in age_list] == [10, 20, 30, 20, 40]


@mark.unit_testing
def test_list_value_object_delete_all_from_primitives_returns_new_instance() -> None:
    """
    Test that delete_all_from_primitives returns a new instance.
    """
    age_list = AgeListValueObject(value=[Age(value=10)])

    assert age_list.delete_all_from_primitives(items=[10]) is not age_list


@mark.unit_testing
def test_list_value_object_delete_all_from_primitives_raises_when_missing_items() -> None:
    """
    Test that delete_all_from_primitives raises a ValueError when any item is missing.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'ListValueObject item <<<.*>>> not found in thelist when attempting to delete it.',
    ):
        AgeListValueObject(value=[Age(value=10)]).delete_all_from_primitives(items=[10, 20])


@mark.unit_testing
def test_list_value_object_from_primitives_builds_value_object_list() -> None:
    """
    Test that from_primitives creates a list of ValueObjects from primitives.
    """
    age_list = AgeListValueObject.from_primitives(value=[10, 20])

    assert [age.value for age in age_list] == [10, 20]


@mark.unit_testing
def test_list_value_object_from_primitives_rejects_non_list() -> None:
    """
    Test that from_primitives validates its container before converting items.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject value <<<invalid>>> must be a list\. Got <<<str>>> type\.',
    ):
        IntListValueObject.from_primitives(value=cast(Any, 'invalid'))


@mark.unit_testing
def test_list_value_object_from_primitives_delegates_to_custom_error_hook() -> None:
    """
    Test that from_primitives preserves subclass container error hooks.
    """
    with assert_raises(expected_exception=CustomListTypeError):
        CustomErrorListValueObject.from_primitives(value=BaseMother.invalid_type(remove_types=(list,)))


@mark.unit_testing
def test_list_value_object_from_primitives_creates_value_object_instances() -> None:
    """
    Test that from_primitives creates ValueObject instances.
    """
    age_list = AgeListValueObject.from_primitives(value=[10, 20])

    assert all(isinstance(age, Age) for age in age_list)


@mark.unit_testing
def test_list_value_object_from_primitives_builds_base_model_list() -> None:
    """
    Test that from_primitives creates a list of BaseModels when the type exposes from_primitives.
    """
    tag_list = TagListValueObject.from_primitives(value=[{'name': 'feature'}, {'name': 'bug'}])

    assert [tag.name for tag in tag_list] == ['feature', 'bug']


@mark.unit_testing
def test_list_value_object_from_primitives_creates_base_model_instances() -> None:
    """
    Test that from_primitives creates BaseModel instances.
    """
    tag_list = TagListValueObject.from_primitives(value=[{'name': 'feature'}])

    assert all(isinstance(tag, Tag) for tag in tag_list)


@mark.unit_testing
def test_list_value_object_from_primitives_with_any_type_returns_values_unchanged() -> None:
    """
    Test that from_primitives returns the provided primitives unchanged when the type is Any.
    """
    values = [1, 'a', {True: 2}]

    assert AnyListValueObject.from_primitives(value=values).value == values


@mark.unit_testing
def test_list_value_object_to_primitives_with_primitive_types() -> None:
    """
    Test to_primitives with primitive types (int, float, str, bool, None).
    """
    list_vo = IntListValueObject(value=[1, 2, 3, 4, 5])

    primitives = list_vo.to_primitives()

    assert primitives == [1, 2, 3, 4, 5]
    assert isinstance(primitives, list)


@mark.unit_testing
def test_list_value_object_to_primitives_with_value_objects() -> None:
    """
    Test to_primitives correctly extracts values from ValueObject instances.
    """
    list_vo = AgeListValueObject(value=[Age(value=10), Age(value=20), Age(value=30)])

    primitives = list_vo.to_primitives()

    assert primitives == [10, 20, 30]


@mark.unit_testing
def test_list_value_object_to_primitives_with_base_models() -> None:
    """
    Test to_primitives correctly converts BaseModel instances to their primitive dictionaries.
    """
    list_vo = TagListValueObject(value=[Tag(name='feature'), Tag(name='bugfix'), Tag(name='hotfix')])

    primitives = list_vo.to_primitives()

    assert primitives == [{'name': 'feature'}, {'name': 'bugfix'}, {'name': 'hotfix'}]


@mark.unit_testing
def test_list_value_object_to_primitives_with_custom_objects() -> None:
    """
    Test to_primitives converts unknown objects to strings.
    """
    list_vo = CustomObjectList(value=[CustomObj(), CustomObj()])

    primitives = list_vo.to_primitives()

    assert primitives == ['custom-object', 'custom-object']


@mark.unit_testing
def test_list_value_object_to_primitives_with_nested_collections() -> None:
    """
    Test to_primitives handles nested collections (lists, dicts, tuples).
    """
    list_vo = NestedListValueObject(value=[[1, 2], [3, 4], [5, 6]])

    primitives = list_vo.to_primitives()

    assert primitives == [[1, 2], [3, 4], [5, 6]]


@mark.unit_testing
def test_list_value_object_to_primitives_recursively_converts_nested_value_objects_in_collections() -> None:
    """
    Test to_primitives recursively converts nested ValueObject values inside collections.
    """
    list_vo = AnyListValueObject(value=[[Age(value=1), Age(value=2)], {'age': Age(value=3)}])

    assert list_vo.to_primitives() == [[1, 2], {'age': 3}]


@mark.unit_testing
def test_list_value_object_to_primitives_with_mixed_types() -> None:
    """
    Test to_primitives handles mixed types including primitives, ValueObjects, and BaseModels.
    """
    list_vo = MixedValueObjectList(value=[1, Age(value=2), Tag(name='test')])

    primitives = list_vo.to_primitives()

    assert primitives == [1, 2, {'name': 'test'}]


@mark.unit_testing
def test_list_value_object_to_primitives_with_empty_list() -> None:
    """
    Test to_primitives returns an empty list when the value object is empty.
    """
    list_vo = IntListValueObject(value=[])

    primitives = list_vo.to_primitives()

    assert primitives == []
    assert isinstance(primitives, list)


@mark.unit_testing
def test_list_value_object_to_primitives_with_none_values() -> None:
    """
    Test to_primitives correctly handles None values in the list.
    """
    list_vo = NoneableListValueObject(value=[1, None, 3, None, 5])

    primitives = list_vo.to_primitives()

    assert primitives == [1, None, 3, None, 5]


@mark.unit_testing
def test_list_value_object_to_primitives_with_bytes() -> None:
    """
    Test to_primitives correctly handles bytes values.
    """
    list_vo = BytesListValueObject(value=[b'hello', b'world'])

    primitives = list_vo.to_primitives()

    assert primitives == [b'hello', b'world']


@mark.unit_testing
def test_list_value_object_to_primitives_preserves_order() -> None:
    """
    Test to_primitives preserves the order of items in the list.
    """
    list_vo = IntListValueObject(value=[5, 3, 1, 4, 2])

    primitives = list_vo.to_primitives()

    assert primitives == [5, 3, 1, 4, 2]


@mark.unit_testing
def test_list_value_object_to_primitives_with_enums() -> None:
    """
    Test to_primitives correctly extracts values from Enum instances directly.
    """
    list_vo = EnumList(value=[Color.RED, Color.BLUE, Color.RED])

    primitives = list_vo.to_primitives()

    assert primitives == ['red', 'blue', 'red']


@mark.unit_testing
def test_list_value_object_to_primitives_with_booleans() -> None:
    """
    Test to_primitives correctly handles boolean values.
    """
    list_vo = BoolListValueObject(value=[True, False, True, True, False])

    primitives = list_vo.to_primitives()

    assert primitives == [True, False, True, True, False]


@mark.unit_testing
def test_list_value_object_to_primitives_with_floats() -> None:
    """
    Test to_primitives correctly handles float values.
    """
    list_vo = FloatListValueObject(value=[1.1, 2.2, 3.3, 4.4])

    primitives = list_vo.to_primitives()

    assert primitives == [1.1, 2.2, 3.3, 4.4]


@mark.unit_testing
def test_list_value_object_to_primitives_with_strings() -> None:
    """
    Test to_primitives correctly handles string values.
    """
    list_vo = StrListValueObject(value=['hello', 'world', 'test'])

    primitives = list_vo.to_primitives()

    assert primitives == ['hello', 'world', 'test']


@mark.unit_testing
def test_list_value_object_inline_constructor_stores_items() -> None:
    """
    Test that ListValueObject[T](...) works without declaring a named subclass.
    """
    value = ListValueObject[int](value=[1, 2])

    assert value.value == [1, 2]


@mark.unit_testing
def test_list_value_object_inline_constructor_supports_union_item_type() -> None:
    """
    Test that inline construction preserves union item validation.
    """
    value = ListValueObject[int | str](value=[1, 'name'])

    assert value.value == [1, 'name']


@mark.unit_testing
def test_list_value_object_inline_constructor_reuses_runtime_class_for_equality() -> None:
    """
    Test that repeated inline construction uses the same runtime class for equivalent aliases.
    """
    first = ListValueObject[int](value=[1])
    second = ListValueObject[int](value=[1])

    assert first == second


@mark.unit_testing
def test_list_value_object_inline_from_primitives_converts_items() -> None:
    """
    Test that inline aliases expose class helpers through the generated runtime subclass.
    """
    value = ListValueObject[Age].from_primitives(value=[1, 2])

    assert [item.value for item in value] == [1, 2]
    assert all(isinstance(item, Age) for item in value)


@mark.unit_testing
def test_list_value_object_inline_add_from_primitives_converts_item() -> None:
    """
    Test that inline instances can use primitive-converting list helpers.
    """
    value = ListValueObject[Age].from_primitives(value=[1])
    updated = value.add_from_primitives(item=2)

    assert [item.value for item in updated] == [1, 2]
    assert [item.value for item in value] == [1]


@mark.unit_testing
def test_list_value_object_inline_constructor_rejects_invalid_type_argument() -> None:
    """
    Test that inline construction preserves type argument validation.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject\[\.\.\.\] <<<1>>> must be a type\. Got <<<int>>> type\.',
    ):
        invalid_list_value_object = cast(Any, ListValueObject)[1]
        invalid_list_value_object(value=[1])


@mark.unit_testing
def test_list_value_object_inline_constructor_rejects_invalid_value() -> None:
    """
    Test that inline construction reports list validation errors.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'ListValueObject\[int\] value <<<name>>> must be of type <<<int>>> type\. Got <<<str>>> type\.',
    ):
        ListValueObject[int](value=cast(Any, ['name']))


@mark.unit_testing
def test_list_value_object_inline_constructor_allows_any() -> None:
    """
    Test that inline construction preserves Any handling.
    """
    payload = object()
    value = ListValueObject[Any](value=[payload])

    assert value.value == [payload]


@mark.unit_testing
def test_list_value_object_inline_type_argument_label_uses_string_fallback() -> None:
    """
    Test that generated inline class labels handle type-like objects without names.
    """
    assert _ListValueObjectAlias._format_type_argument(type=ForwardRef('SomeType')) == "ForwardRef('SomeType')"
