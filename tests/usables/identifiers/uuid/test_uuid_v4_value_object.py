"""
Test UuidV4ValueObject value object.
"""

from uuid import UUID, uuid1

from object_mother_pattern.mothers.identifiers import UuidV4Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import UuidV4ValueObject


@mark.unit_testing
def test_uuid4_value_object_happy_path() -> None:
    """
    Test UuidV4ValueObject value object happy path.
    """
    uuid_value = UuidV4ValueObject(value=UuidV4Mother.create())

    assert type(uuid_value.value) is UUID
    assert uuid_value.value.version == 4


@mark.unit_testing
def test_uuid4_value_object_invalid_type() -> None:
    """
    Test UuidV4ValueObject value object raises TypeError when value is not an UUID.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'UuidV4ValueObject value <<<.*>>> must be a UUID. Got <<<.*>>> type.',
    ):
        UuidV4ValueObject(value=UuidV4Mother.invalid_type())


@mark.unit_testing
def test_uuid4_value_object_invalid_version() -> None:
    """
    Test UuidV4ValueObject value object raises ValueError when value is not UUID version 4.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'UuidV4ValueObject value <<<.*>>> must be a UUID version 4. Got version <<<.*>>>.',
    ):
        UuidV4ValueObject(value=uuid1())
