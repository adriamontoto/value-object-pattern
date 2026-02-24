"""
Test type matching helper.
"""

from typing import Any, cast

from pytest import mark

from value_object_pattern.models.type_matching import matches_expected_type


@mark.unit_testing
def test_matches_expected_type_non_class_expected_type_with_tuple_is_supported() -> None:
    """
    Test that tuple second argument path returns isinstance result for non-class expected values.
    """
    assert matches_expected_type(value=7, expected_type=(int, str))
    assert not matches_expected_type(value=7.5, expected_type=(int, str))


@mark.unit_testing
def test_matches_expected_type_returns_false_when_isinstance_raises_type_error() -> None:
    """
    Test that helper returns False when isinstance raises TypeError for non-class expected values.
    """
    assert not matches_expected_type(value='x', expected_type=cast(Any, object()))
