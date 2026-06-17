"""
Test BaseModel model.
"""

from __future__ import annotations

from copy import copy, deepcopy
from typing import Any, ForwardRef

from pytest import MonkeyPatch, mark, raises as assert_raises

from value_object_pattern import BaseModel


class Profile(BaseModel):
    """
    Base model used to test representation, copy, and primitive conversion branches.
    """

    name: str
    _age: int
    __private_note: str

    def __init__(self, name: str, age: int, private_note: str = 'hidden') -> None:
        """
        Initialize the profile model.
        """
        self.name = name
        self._age = age
        self.__private_note = private_note


class IntOrStrModel(BaseModel):
    """
    Base model with a union field.
    """

    payload: int | str

    def __init__(self, payload: int | str) -> None:
        """
        Initialize the union model.
        """
        self.payload = payload


@mark.unit_testing
def test_base_model_repr_filters_private_attributes() -> None:
    """
    Test BaseModel repr filters private attributes.
    """
    assert repr(Profile(name='Ada', age=37, private_note='marker')) == "Profile(age=37, name='Ada')"


@mark.unit_testing
def test_base_model_str_filters_private_attributes() -> None:
    """
    Test BaseModel str filters private attributes.
    """
    assert str(Profile(name='Ada', age=37, private_note='marker')) == 'Profile(age=37, name=Ada)'


@mark.unit_testing
def test_base_model_hash_uses_public_attributes() -> None:
    """
    Test BaseModel hash uses public attributes.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')
    same_public_profile = Profile(name='Ada', age=37, private_note='another-marker')

    assert hash(profile) == hash(same_public_profile)


@mark.unit_testing
def test_base_model_equality_uses_public_attributes() -> None:
    """
    Test BaseModel equality uses public attributes.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')
    same_public_profile = Profile(name='Ada', age=37, private_note='another-marker')

    assert profile == same_public_profile
    assert profile != object()


@mark.unit_testing
def test_base_model_to_dict_can_include_private_attributes() -> None:
    """
    Test BaseModel _to_dict can include private attributes.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')

    assert profile._to_dict(ignore_private=False) == {'private_note': 'marker', 'age': 37, 'name': 'Ada'}


@mark.unit_testing
def test_base_model_copy() -> None:
    """
    Test BaseModel shallow copy.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')

    shallow_clone = copy(profile)

    assert shallow_clone == profile
    assert shallow_clone is not profile


@mark.unit_testing
def test_base_model_deepcopy() -> None:
    """
    Test BaseModel deep copy.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')

    deep_clone = deepcopy(profile)

    assert deep_clone == profile
    assert deep_clone is not profile


@mark.unit_testing
def test_base_model_deepcopy_returns_memoized_value() -> None:
    """
    Test BaseModel deepcopy returns memoized values.
    """
    profile = Profile(name='Ada', age=37, private_note='marker')

    assert profile.__deepcopy__({id(profile): 'cached'}) == 'cached'


@mark.unit_testing
def test_base_model_from_primitives_uses_optional_constructor_parameter_default() -> None:
    """
    Test BaseModel.from_primitives handles optional constructor parameters.
    """
    assert Profile.from_primitives(primitives={'name': 'Ada', 'age': 37}).to_primitives() == {
        'age': 37,
        'name': 'Ada',
    }


@mark.unit_testing
def test_base_model_from_primitives_rejects_non_dictionary_primitives() -> None:
    """
    Test BaseModel.from_primitives raises TypeError when primitives is not a dictionary.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Profile primitives <<<.*>>> must be a dictionary of strings. Got <<<list>>> type.',
    ):
        Profile.from_primitives(primitives=[])  # type: ignore[arg-type]


@mark.unit_testing
def test_base_model_from_primitives_rejects_non_string_keys() -> None:
    """
    Test BaseModel.from_primitives raises TypeError when primitives keys are not strings.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'Profile primitives <<<.*>>> must be a dictionary of strings. Got <<<dict>>> type.',
    ):
        Profile.from_primitives(primitives={1: 'Ada'})  # type: ignore[dict-item]


@mark.unit_testing
def test_base_model_from_primitives_rejects_missing_constructor_parameters() -> None:
    """
    Test BaseModel.from_primitives raises ValueError when constructor parameters are missing.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'Profile primitives <<<extra, name>>> must contain all constructor parameters.',
    ):
        Profile.from_primitives(primitives={'name': 'Ada', 'extra': True})


@mark.unit_testing
def test_base_model_from_primitives_rejects_union_type_mismatch() -> None:
    """
    Test BaseModel.from_primitives raises TypeError when a union field value has an invalid type.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'IntOrStrModel parameter <<<payload>>> value <<<1\.5>>> must be of type <<<int \| str>>> type.',
    ):
        IntOrStrModel.from_primitives(primitives={'payload': 1.5})


@mark.unit_testing
def test_base_model_get_constructor_annotations_returns_empty_dictionary_when_type_hints_fail(
    monkeypatch: MonkeyPatch,
) -> None:
    """
    Test BaseModel constructor annotation fallback when type hint resolution fails.
    """
    monkeypatch.setattr(
        'value_object_pattern.models.base_model.get_type_hints',
        lambda _: (_ for _ in ()).throw(RuntimeError),
    )

    assert Profile._get_constructor_annotations() == {}


@mark.unit_testing
def test_base_model_type_label_any() -> None:
    """
    Test BaseModel type label for Any.
    """
    assert BaseModel._type_label(type=Any) == 'Any'


@mark.unit_testing
def test_base_model_type_label_forward_ref() -> None:
    """
    Test BaseModel type label for ForwardRef.
    """
    assert BaseModel._type_label(type=ForwardRef('Later')) == "ForwardRef('Later')"
