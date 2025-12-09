"""
Test StringUuidV1ValueObject value object.
"""

from object_mother_pattern import StringMother
from object_mother_pattern.mothers.identifiers import StringUuidMother, StringUuidV1Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import StringUuidV1ValueObject


@mark.unit_testing
def test_string_uuid1_value_object_happy_path() -> None:
    """
    Test StringUuidV1ValueObject value object happy path.
    """
    uuid_value = StringUuidV1ValueObject(value=StringUuidV1Mother.create())

    assert type(uuid_value.value) is str
    assert uuid_value.value.islower()


@mark.unit_testing
def test_string_uuid1_value_object_invalid_type() -> None:
    """
    Test StringUuidV1ValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringUuidV1ValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringUuidV1ValueObject(value=StringUuidV1Mother.invalid_type())


@mark.unit_testing
def test_string_uuid1_value_object_empty_string() -> None:
    """
    Test StringUuidV1ValueObject value object raises ValueError when value is empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV1ValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        StringUuidV1ValueObject(value=StringMother.empty())


@mark.unit_testing
def test_string_uuid1_value_object_invalid_uuid() -> None:
    """
    Test StringUuidV1ValueObject value object raises ValueError when value is not a valid UUID.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV1ValueObject value <<<.*>>> is not a valid UUID.',
    ):
        StringUuidV1ValueObject(value=StringMother.create())


@mark.unit_testing
def test_string_uuid1_value_object_invalid_version() -> None:
    """
    Test StringUuidV1ValueObject value object raises ValueError when value is not UUID version 1.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV1ValueObject value <<<.*>>> must be a UUID version 1. Got version <<<.*>>>.',
    ):
        StringUuidV1ValueObject(value=StringUuidMother.create(exclude_versions={1}))
