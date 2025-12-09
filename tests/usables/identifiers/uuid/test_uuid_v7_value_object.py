"""
Test UuidV7ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV7Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV7ValueObject


@mark.unit_testing
def test_uuid7_value_object_happy_path() -> None:
    """
    Test UuidV7ValueObject value object happy path.
    """
    uuid_value = UuidV7ValueObject(value=UuidV7Mother.create())

    assert isinstance(uuid_value.value, UUID)
    assert uuid_value.value.version == 7


@mark.unit_testing
def test_uuid7_value_object_invalid_type() -> None:
    """
    Test UuidV7ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV7ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV7ValueObject(value=UuidV7Mother.invalid_type())


@mark.unit_testing
def test_uuid7_value_object_invalid_version() -> None:
    """
    Test UuidV7ValueObject value object raises ValueError when value is not UUID version 7.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV7ValueObject value <<<.*>>> must be a UUID version 7. Got version <<<.*>>>.',
    ):
        UuidV7ValueObject(value=UuidMother.create(exclude_versions={7}))
