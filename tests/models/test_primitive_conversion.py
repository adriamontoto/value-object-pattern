"""
Test primitive conversion helpers.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum

from pytest import mark

from value_object_pattern import BaseModel, UnionValueObject, ValueObject
from value_object_pattern.models.collections import DictValueObject, ListValueObject
from value_object_pattern.models.primitive_conversion import from_primitive, to_primitive


class SelfToPrimitives:
    """
    Helper object whose to_primitives returns itself.
    """

    def to_primitives(self) -> SelfToPrimitives:
        """
        Return itself to exercise the self-reference guard.
        """
        return self

    @override
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

    @override
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


class NumberMatrix(ListValueObject[list[Number]]):
    """
    List value object storing nested lists of Number items.
    """


class NestedNumberMap(DictValueObject[str, dict[str, Number]]):
    """
    Dict value object storing nested dictionaries of Number items.
    """


class Status(Enum):
    """
    Enumeration used in union from_primitives tests.
    """

    ON = 'on'
    OFF = 'off'


class Tag(BaseModel):
    """
    Simple model used in union from_primitives tests.
    """

    def __init__(self, name: str) -> None:
        """
        Tag model constructor.
        """
        self.name = name


class TagOrStatus(UnionValueObject[Tag | Status]):
    """
    Union value object used in from_primitives tests.
    """


class SecondaryStatus(Enum):
    """
    Secondary enum used to exercise union fallback paths.
    """

    UP = 'up'
    DOWN = 'down'


class ClassWithValueAttribute:
    """
    Class exposing a class-level value descriptor and value constructor.
    """

    _value: str

    def __init__(self, value: str) -> None:
        """
        Initialize class with value.
        """
        self._value = value

    @property
    def value(self) -> str:
        """
        Expose value as a property.
        """
        return self._value


class ClassWithStrictFromPrimitives:
    """
    Class with strict from_primitives validation used to exercise fallback paths.
    """

    raw: dict[str, int]

    def __init__(self, raw: dict[str, int]) -> None:
        """
        Initialize with validated raw payload.
        """
        self.raw = raw

    @classmethod
    def from_primitives(cls, value: dict[str, int]) -> ClassWithStrictFromPrimitives:
        """
        Accept only payloads with the key "ok".
        """
        if 'ok' not in value:
            raise ValueError('Missing key "ok".')

        return cls(raw=value)


class ToPrimitivesInvalidPayload:
    """
    Helper object that produces invalid payload for ClassWithStrictFromPrimitives.
    """

    def to_primitives(self) -> dict[str, int]:
        """
        Return invalid payload to trigger conversion fallback.
        """
        return {'bad': 1}


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


@mark.unit_testing
def test_from_primitive_recursively_converts_nested_list_annotation() -> None:
    """
    Test from_primitive recursively converts nested list annotations.
    """
    converted = from_primitive(value=[[1, 2], [3]], expected_type=list[list[Number]])

    assert all(isinstance(item, list) for item in converted)
    assert [[number.value for number in inner] for inner in converted] == [[1, 2], [3]]


@mark.unit_testing
def test_from_primitive_recursively_converts_nested_dict_annotation() -> None:
    """
    Test from_primitive recursively converts nested dict annotations.
    """
    converted = from_primitive(value={'group': {'a': 1, 'b': 2}}, expected_type=dict[str, dict[str, Number]])

    assert isinstance(converted['group']['a'], Number)
    assert {key: item.value for key, item in converted['group'].items()} == {'a': 1, 'b': 2}


@mark.unit_testing
def test_list_value_object_from_primitives_recursively_converts_nested_inner_types() -> None:
    """
    Test ListValueObject.from_primitives recursively converts nested inner items.
    """
    matrix = NumberMatrix.from_primitives(value=[[1, 2], [3]])

    assert all(isinstance(number, Number) for row in matrix.value for number in row)
    assert matrix.to_primitives() == [[1, 2], [3]]


@mark.unit_testing
def test_dict_value_object_from_primitives_recursively_converts_nested_inner_types() -> None:
    """
    Test DictValueObject.from_primitives recursively converts nested inner values.
    """
    mapping = NestedNumberMap.from_primitives(value={'group': {'a': 1, 'b': 2}})

    assert isinstance(mapping.value['group']['a'], Number)
    assert mapping.to_primitives() == {'group': {'a': 1, 'b': 2}}


@mark.unit_testing
def test_union_value_object_from_primitives_builds_base_model_candidate() -> None:
    """
    Test UnionValueObject.from_primitives builds the matching BaseModel candidate.
    """
    union = TagOrStatus.from_primitives(value={'name': 'feature'})

    assert isinstance(union.value, Tag)
    assert union.value.name == 'feature'


@mark.unit_testing
def test_union_value_object_from_primitives_builds_enum_candidate() -> None:
    """
    Test UnionValueObject.from_primitives builds the matching enum candidate.
    """
    union = TagOrStatus.from_primitives(value='on')

    assert union.value is Status.ON


@mark.unit_testing
def test_from_primitive_union_returns_raw_value_when_all_candidates_fail() -> None:
    """
    Test union conversion fallback to raw value when every candidate raises.
    """
    converted = from_primitive(value='invalid', expected_type=Status | SecondaryStatus)

    assert converted == 'invalid'


@mark.unit_testing
def test_from_primitive_returns_raw_value_for_unsupported_origin() -> None:
    """
    Test unsupported typing origins return the input value unchanged.
    """
    converted = from_primitive(value='x', expected_type=type[int])

    assert converted == 'x'


@mark.unit_testing
def test_from_primitive_list_returns_raw_value_when_input_is_not_list() -> None:
    """
    Test list conversion branch returns raw value when input is not a list.
    """
    converted = from_primitive(value='x', expected_type=list[int])

    assert converted == 'x'


@mark.unit_testing
def test_from_primitive_tuple_returns_raw_value_when_input_is_not_sequence() -> None:
    """
    Test tuple conversion returns raw value when input is not list/tuple.
    """
    converted = from_primitive(value='x', expected_type=tuple[int, ...])

    assert converted == 'x'


@mark.unit_testing
def test_from_primitive_tuple_handles_ellipsis_annotation() -> None:
    """
    Test tuple conversion for variable-length tuple annotations.
    """
    converted = from_primitive(value=[1, 2, 3], expected_type=tuple[int, ...])

    assert converted == (1, 2, 3)


@mark.unit_testing
def test_from_primitive_tuple_returns_sequence_when_length_mismatch() -> None:
    """
    Test tuple conversion returns raw tuple when fixed-length annotation does not match length.
    """
    converted = from_primitive(value=[1, 2], expected_type=tuple[int, str, bool])

    assert converted == (1, 2)


@mark.unit_testing
def test_from_primitive_tuple_converts_fixed_length_tuple() -> None:
    """
    Test tuple conversion for fixed-length tuple annotations.
    """
    converted = from_primitive(value=[1, 'x'], expected_type=tuple[int, str])

    assert converted == (1, 'x')


@mark.unit_testing
def test_from_primitive_set_converts_supported_sequence_inputs() -> None:
    """
    Test set conversion branch for sequence inputs.
    """
    converted = from_primitive(value=[1, 2, 2], expected_type=set[int])

    assert converted == {1, 2}


@mark.unit_testing
def test_from_primitive_set_returns_raw_value_for_unsupported_input_type() -> None:
    """
    Test set conversion returns raw value when input type is unsupported.
    """
    converted = from_primitive(value='not-a-sequence', expected_type=set[int])

    assert converted == 'not-a-sequence'


@mark.unit_testing
def test_from_primitive_frozenset_converts_supported_sequence_inputs() -> None:
    """
    Test frozenset conversion branch for sequence inputs.
    """
    converted = from_primitive(value=[1, 2, 2], expected_type=frozenset[int])

    assert converted == frozenset({1, 2})


@mark.unit_testing
def test_from_primitive_frozenset_returns_raw_value_for_unsupported_input_type() -> None:
    """
    Test frozenset conversion returns raw value when input type is unsupported.
    """
    converted = from_primitive(value='not-a-sequence', expected_type=frozenset[int])

    assert converted == 'not-a-sequence'


@mark.unit_testing
def test_from_primitive_dict_returns_raw_value_when_input_is_not_dict() -> None:
    """
    Test dict conversion branch returns raw value when input is not a dict.
    """
    converted = from_primitive(value=['not', 'a', 'dict'], expected_type=dict[str, int])

    assert converted == ['not', 'a', 'dict']


@mark.unit_testing
def test_from_primitive_type_none_branch_handles_none_and_non_none_values() -> None:
    """
    Test type(None) conversion branch for both matching and non-matching values.
    """
    assert from_primitive(value=None, expected_type=type(None)) is None
    assert from_primitive(value='x', expected_type=type(None)) == 'x'


@mark.unit_testing
def test_from_primitive_non_class_expected_type_returns_raw_value() -> None:
    """
    Test non-class expected types return the input value unchanged.
    """
    converted = from_primitive(value='x', expected_type='not-a-class')

    assert converted == 'x'


@mark.unit_testing
def test_from_primitive_class_with_value_attribute_handles_instance_and_raw_value() -> None:
    """
    Test class-level value attribute branch for existing instances and raw values.
    """
    instance = ClassWithValueAttribute(value='ok')

    assert from_primitive(value=instance, expected_type=ClassWithValueAttribute) is instance
    converted = from_primitive(value='raw', expected_type=ClassWithValueAttribute)
    assert isinstance(converted, ClassWithValueAttribute)
    assert converted.value == 'raw'


@mark.unit_testing
def test_from_primitive_enum_branch_returns_existing_member() -> None:
    """
    Test enum conversion branch returns existing enum members unchanged.
    """
    assert from_primitive(value=Status.ON, expected_type=Status) is Status.ON


@mark.unit_testing
def test_from_primitive_value_object_branch_returns_existing_instance() -> None:
    """
    Test value object conversion branch returns existing instances unchanged.
    """
    number = Number(value=7)

    assert from_primitive(value=number, expected_type=Number) is number


@mark.unit_testing
def test_from_primitive_to_primitives_fallback_returns_raw_value_when_conversion_fails() -> None:
    """
    Test fallback path returns raw value when to_primitives payload cannot be converted.
    """
    source = ToPrimitivesInvalidPayload()

    assert from_primitive(value=source, expected_type=ClassWithStrictFromPrimitives) is source
