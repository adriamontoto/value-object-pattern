"""
Test StringUuidV7ValueObject value object.
"""

from object_mother_pattern import StringMother
from object_mother_pattern.mothers.identifiers import StringUuidMother, StringUuidV7Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import StringUuidV7ValueObject


@mark.unit_testing
def test_string_uuid7_value_object_happy_path() -> None:
    """
    Test StringUuidV7ValueObject value object happy path.
    """
    uuid_value = StringUuidV7ValueObject(value=StringUuidV7Mother.create())

    assert type(uuid_value.value) is str
    assert uuid_value.value.islower()


@mark.unit_testing
def test_string_uuid7_value_object_invalid_type() -> None:
    """
    Test StringUuidV7ValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringUuidV7ValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringUuidV7ValueObject(value=StringUuidV7Mother.invalid_type())


@mark.unit_testing
def test_string_uuid7_value_object_empty_string() -> None:
    """
    Test StringUuidV7ValueObject value object raises ValueError when value is empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV7ValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        StringUuidV7ValueObject(value=StringMother.empty())


@mark.unit_testing
def test_string_uuid7_value_object_invalid_uuid() -> None:
    """
    Test StringUuidV7ValueObject value object raises ValueError when value is not a valid UUID.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV7ValueObject value <<<.*>>> is not a valid UUID.',
    ):
        StringUuidV7ValueObject(value=StringMother.create())


@mark.unit_testing
def test_string_uuid7_value_object_invalid_version() -> None:
    """
    Test StringUuidV7ValueObject value object raises ValueError when value is not UUID version 7.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV7ValueObject value <<<.*>>> must be a UUID version 7. Got version <<<.*>>>.',
    ):
        StringUuidV7ValueObject(value=StringUuidMother.create(exclude_versions={7}))
