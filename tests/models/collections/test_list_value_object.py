"""
Test ListValueObject value object.
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

from value_object_pattern import BaseModel, ValueObject
from value_object_pattern.models.collections import ListValueObject


class IntListValueObject(ListValueObject[int]):
    """
    List value object storing integers.
    """


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
