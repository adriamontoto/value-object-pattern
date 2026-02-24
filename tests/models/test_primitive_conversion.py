"""
Test primitive conversion helpers.
"""

from __future__ import annotations

from pytest import mark

from value_object_pattern import BaseModel, ValueObject
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.models.primitive_conversion import to_primitive


class SelfToPrimitives:
    """
    Helper object whose to_primitives returns itself.
    """

    def to_primitives(self) -> SelfToPrimitives:
        """
        Return itself to exercise the self-reference guard.
        """
        return self

    def __str__(self) -> str:
        """
        Stable string representation.
        """
        return 'self-to-primitives'


class SelfValueAttribute:
    """
    Helper object whose value attribute points to itself.
    """

    def __init__(self) -> None:
        """
        Initialize with a self-referential value attribute.
        """
        self.value = self

    def __str__(self) -> str:
        """
        Stable string representation.
        """
        return 'self-value-attribute'


@mark.unit_testing
def test_to_primitive_returns_string_when_to_primitives_returns_self() -> None:
    """
    Test the guard branch where to_primitives returns the same object instance.
    """
    assert to_primitive(value=SelfToPrimitives()) == 'self-to-primitives'


@mark.unit_testing
def test_to_primitive_returns_string_when_value_attribute_points_to_self() -> None:
    """
    Test the guard branch where a value attribute references the same object instance.
    """
    assert to_primitive(value=SelfValueAttribute()) == 'self-value-attribute'


@mark.unit_testing
def test_to_primitive_converts_set_values() -> None:
    """
    Test set conversion branch.
    """
    assert to_primitive(value={1, 2, 3}) == {1, 2, 3}


@mark.unit_testing
def test_to_primitive_converts_frozenset_values() -> None:
    """
    Test frozenset conversion branch.
    """
    assert to_primitive(value=frozenset({1, 2, 3})) == frozenset({1, 2, 3})


class Number(ValueObject[int]):
    """
    Simple integer value object.
    """


class NumberList(ListValueObject[Number]):
    """
    List value object storing Number items.
    """


class LeafModel(BaseModel):
    """
    Nested model with a value object field.
    """

    def __init__(self, code: Number) -> None:
        """
        Leaf model constructor.
        """
        self.code = code


class RootModel(BaseModel):
    """
    Root model that nests models, value objects, lists and dictionaries.
    """

    def __init__(
        self,
        leaf: LeafModel,
        leaf_list: list[LeafModel],
        leaf_map: dict[str, LeafModel],
        nested_number_lists: list[NumberList],
    ) -> None:
        """
        Root model constructor.
        """
        self.leaf = leaf
        self.leaf_list = leaf_list
        self.leaf_map = leaf_map
        self.nested_number_lists = nested_number_lists


class Depth3Level3(BaseModel):
    """
    Third level model used to test 3-level nesting.
    """

    def __init__(self, code: Number) -> None:
        """
        Third level constructor.
        """
        self.code = code


class Depth3Level2(BaseModel):
    """
    Second level model used to test 3-level nesting.
    """

    def __init__(self, level3: Depth3Level3) -> None:
        """
        Second level constructor.
        """
        self.level3 = level3


class Depth3Root(BaseModel):
    """
    Root model used to test 3-level nesting.
    """

    def __init__(self, level2: Depth3Level2) -> None:
        """
        Root constructor.
        """
        self.level2 = level2


class Depth4Level4(BaseModel):
    """
    Fourth level model used to test 4-level nesting.
    """

    def __init__(self, code: Number) -> None:
        """
        Fourth level constructor.
        """
        self.code = code


class Depth4Level3(BaseModel):
    """
    Third level model used to test 4-level nesting.
    """

    def __init__(self, level4: Depth4Level4) -> None:
        """
        Third level constructor.
        """
        self.level4 = level4


class Depth4Level2(BaseModel):
    """
    Second level model used to test 4-level nesting.
    """

    def __init__(self, level3: Depth4Level3) -> None:
        """
        Second level constructor.
        """
        self.level3 = level3


class Depth4Root(BaseModel):
    """
    Root model used to test 4-level nesting.
    """

    def __init__(self, level2: Depth4Level2) -> None:
        """
        Root constructor.
        """
        self.level2 = level2


@mark.unit_testing
def test_base_model_to_primitives_recursively_converts_nested_models_and_value_objects() -> None:
    """
    Test to_primitives recursively converts nested models/value objects inside collections.
    """
    model = RootModel(
        leaf=LeafModel(code=Number(value=1)),
        leaf_list=[LeafModel(code=Number(value=2)), LeafModel(code=Number(value=3))],
        leaf_map={'a': LeafModel(code=Number(value=4))},
        nested_number_lists=[
            NumberList(value=[Number(value=5), Number(value=6)]),
            NumberList(value=[Number(value=7)]),
        ],
    )

    assert model.to_primitives() == {
        'leaf': {'code': 1},
        'leaf_list': [{'code': 2}, {'code': 3}],
        'leaf_map': {'a': {'code': 4}},
        'nested_number_lists': [[5, 6], [7]],
    }


@mark.unit_testing
def test_base_model_from_primitives_recursively_converts_nested_models_and_value_objects() -> None:
    """
    Test from_primitives recursively converts nested primitives using constructor annotations.
    """
    primitives = {
        'leaf': {'code': 1},
        'leaf_list': [{'code': 2}, {'code': 3}],
        'leaf_map': {'a': {'code': 4}},
        'nested_number_lists': [[5, 6], [7]],
    }

    model = RootModel.from_primitives(primitives=primitives)

    assert isinstance(model.leaf, LeafModel)
    assert isinstance(model.leaf.code, Number)
    assert [item.code.value for item in model.leaf_list] == [2, 3]
    assert isinstance(model.leaf_map['a'], LeafModel)
    assert isinstance(model.leaf_map['a'].code, Number)
    assert all(isinstance(item, NumberList) for item in model.nested_number_lists)
    assert [[number.value for number in number_list] for number_list in model.nested_number_lists] == [[5, 6], [7]]
    assert model.to_primitives() == primitives


@mark.unit_testing
def test_base_model_roundtrip_with_three_nested_levels() -> None:
    """
    Test recursive conversion with 3 nested model levels.
    """
    primitives = {'level2': {'level3': {'code': 31}}}

    model = Depth3Root.from_primitives(primitives=primitives)

    assert isinstance(model.level2, Depth3Level2)
    assert isinstance(model.level2.level3, Depth3Level3)
    assert isinstance(model.level2.level3.code, Number)
    assert model.level2.level3.code.value == 31
    assert model.to_primitives() == primitives


@mark.unit_testing
def test_base_model_roundtrip_with_four_nested_levels() -> None:
    """
    Test recursive conversion with 4 nested model levels.
    """
    primitives = {'level2': {'level3': {'level4': {'code': 41}}}}

    model = Depth4Root.from_primitives(primitives=primitives)

    assert isinstance(model.level2, Depth4Level2)
    assert isinstance(model.level2.level3, Depth4Level3)
    assert isinstance(model.level2.level3.level4, Depth4Level4)
    assert isinstance(model.level2.level3.level4.code, Number)
    assert model.level2.level3.level4.code.value == 41
    assert model.to_primitives() == primitives
