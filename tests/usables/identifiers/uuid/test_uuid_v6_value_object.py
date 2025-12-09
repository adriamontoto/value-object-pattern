"""
Test UuidV6ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV6Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV6ValueObject


@mark.unit_testing
def test_uuid6_value_object_happy_path() -> None:
    """
    Test UuidV6ValueObject value object happy path.
    """
    uuid_value = UuidV6ValueObject(value=UuidV6Mother.create())

    assert isinstance(uuid_value.value, UUID)
    assert uuid_value.value.version == 6


@mark.unit_testing
def test_uuid6_value_object_invalid_type() -> None:
    """
    Test UuidV6ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV6ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV6ValueObject(value=UuidV6Mother.invalid_type())


@mark.unit_testing
def test_uuid6_value_object_invalid_version() -> None:
    """
    Test UuidV6ValueObject value object raises ValueError when value is not UUID version 6.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV6ValueObject value <<<.*>>> must be a UUID version 6. Got version <<<.*>>>.',
    ):
        UuidV6ValueObject(value=UuidMother.create(exclude_versions={6}))
