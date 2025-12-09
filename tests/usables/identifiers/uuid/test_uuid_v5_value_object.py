"""
Test UuidV5ValueObject value object.
"""

from uuid import UUID

from object_mother_pattern.mothers.identifiers import UuidMother, UuidV5Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers import UuidV5ValueObject


@mark.unit_testing
def test_uuid5_value_object_happy_path() -> None:
    """
    Test UuidV5ValueObject value object happy path.
    """
    uuid_value = UuidV5ValueObject(value=UuidV5Mother.create())

    assert type(uuid_value.value) is UUID
    assert uuid_value.value.version == 5


@mark.unit_testing
def test_uuid5_value_object_invalid_type() -> None:
    """
    Test UuidV5ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV5ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV5ValueObject(value=UuidV5Mother.invalid_type())


@mark.unit_testing
def test_uuid5_value_object_invalid_version() -> None:
    """
    Test UuidV5ValueObject value object raises ValueError when value is not UUID version 5.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV5ValueObject value <<<.*>>> must be a UUID version 5. Got version <<<.*>>>.',
    ):
        UuidV5ValueObject(value=UuidMother.create(exclude_versions={5}))
