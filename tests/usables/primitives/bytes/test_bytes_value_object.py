"""
Test BytesValueObject value object.
"""

from object_mother_pattern import BytesMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables import BytesValueObject


@mark.unit_testing
def test_bytes_value_object_happy_path() -> None:
    """
    Test BytesValueObject value object happy path.
    """
    bytes_value = BytesValueObject(value=BytesMother.create())

    assert type(bytes_value.value) is bytes


@mark.unit_testing
def test_bytes_value_object_invalid_type() -> None:
    """
    Test BytesValueObject value object raises TypeError when value is not bytes.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'BytesValueObject value <<<.*>>> must be bytes. Got <<<.*>>> type.',
    ):
        BytesValueObject(value=BytesMother.invalid_type())
