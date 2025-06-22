"""
Test NotNoneValueObject value object.
"""

from object_mother_pattern.models import BaseMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import NotNoneValueObject


@mark.unit_testing
def test_not_none_value_object_happy_path() -> None:
    """
    Test NotNoneValueObject value object happy path.
    """
    not_none_value = NotNoneValueObject(value=BaseMother.invalid_type())

    assert not_none_value.value is not None


@mark.unit_testing
def test_not_none_value_object_invalid_type() -> None:
    """
    Test NotNoneValueObject value object raises TypeError when value is None.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'NotNoneValueObject value <<<.*>>> must be not None',
    ):
        NotNoneValueObject(value=None)
