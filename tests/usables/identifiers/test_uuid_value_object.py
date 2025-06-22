"""
Test UuidValueObject value object.
"""

from uuid import UUID

from object_mother_pattern import UuidMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers import UuidValueObject


@mark.unit_testing
def test_uuid_value_object_happy_path() -> None:
    """
    Test UuidValueObject value object happy path.
    """
    uuid_value = UuidValueObject(value=UuidMother.create())

    assert type(uuid_value.value) is UUID


@mark.unit_testing
def test_uuid_value_object_invalid_type() -> None:
    """
    Test UuidValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidValueObject(value=UuidMother.invalid_type())
