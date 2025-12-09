"""
Test UuidV3ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV3Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV3ValueObject


@mark.unit_testing
def test_uuid3_value_object_happy_path() -> None:
    """
    Test UuidV3ValueObject value object happy path.
    """
    uuid_value = UuidV3ValueObject(value=UuidV3Mother.create())

    assert type(uuid_value.value) is UUID
    assert uuid_value.value.version == 3


@mark.unit_testing
def test_uuid3_value_object_invalid_type() -> None:
    """
    Test UuidV3ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV3ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV3ValueObject(value=UuidV3Mother.invalid_type())


@mark.unit_testing
def test_uuid3_value_object_invalid_version() -> None:
    """
    Test UuidV3ValueObject value object raises ValueError when value is not UUID version 3.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV3ValueObject value <<<.*>>> must be a UUID version 3. Got version <<<.*>>>.',
    ):
        UuidV3ValueObject(value=UuidMother.create(exclude_versions={3}))
