"""
Test UuidV1ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV1Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV1ValueObject


@mark.unit_testing
def test_uuid1_value_object_happy_path() -> None:
    """
    Test UuidV1ValueObject value object happy path.
    """
    uuid_value = UuidV1ValueObject(value=UuidV1Mother.create())

    assert type(uuid_value.value) is UUID
    assert uuid_value.value.version == 1


@mark.unit_testing
def test_uuid1_value_object_invalid_type() -> None:
    """
    Test UuidV1ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV1ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV1ValueObject(value=UuidV1Mother.invalid_type())


@mark.unit_testing
def test_uuid1_value_object_invalid_version() -> None:
    """
    Test UuidV1ValueObject value object raises ValueError when value is not UUID version 1.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV1ValueObject value <<<.*>>> must be a UUID version 1. Got version <<<.*>>>.',
    ):
        UuidV1ValueObject(value=UuidMother.create(exclude_versions={1}))
