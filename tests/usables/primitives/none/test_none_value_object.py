"""
Test NoneValueObject value object.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import NoneValueObject


@mark.unit_testing
def test_none_value_object_happy_path() -> None:
    """
    Test NoneValueObject value object happy path.
    """
    none_value = NoneValueObject(value=None)

    assert none_value.value is None


@mark.unit_testing
def test_none_value_object_invalid_type() -> None:
    """
    Test NoneValueObject value object raises TypeError when value is not None.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'NoneValueObject value <<<.*>>> must be None. Got <<<.*>>> type.',
    ):
        NoneValueObject(value=BaseMother.invalid_type())
