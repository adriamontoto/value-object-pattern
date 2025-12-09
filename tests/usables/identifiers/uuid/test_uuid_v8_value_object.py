"""
Test UuidV8ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV8Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV8ValueObject


@mark.unit_testing
def test_uuid8_value_object_happy_path() -> None:
    """
    Test UuidV8ValueObject value object happy path.
    """
    uuid_value = UuidV8ValueObject(value=UuidV8Mother.create())

    assert isinstance(uuid_value.value, UUID)
    assert uuid_value.value.version == 8


@mark.unit_testing
def test_uuid8_value_object_invalid_type() -> None:
    """
    Test UuidV8ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV8ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV8ValueObject(value=UuidV8Mother.invalid_type())


@mark.unit_testing
def test_uuid8_value_object_invalid_version() -> None:
    """
    Test UuidV8ValueObject value object raises ValueError when value is not UUID version 8.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV8ValueObject value <<<.*>>> must be a UUID version 8. Got version <<<.*>>>.',
    ):
        UuidV8ValueObject(value=UuidMother.create(exclude_versions={8}))
