"""
Test StringUuidV5ValueObject value object.
"""

from object_mother_pattern import StringMother
from object_mother_pattern.mothers.identifiers import StringUuidMother, StringUuidV5Mother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers.uuid import StringUuidV5ValueObject


@mark.unit_testing
def test_string_uuid5_value_object_happy_path() -> None:
    """
    Test StringUuidV5ValueObject value object happy path.
    """
    uuid_value = StringUuidV5ValueObject(value=StringUuidV5Mother.create())

    assert type(uuid_value.value) is str
    assert uuid_value.value.islower()


@mark.unit_testing
def test_string_uuid5_value_object_invalid_type() -> None:
    """
    Test StringUuidV5ValueObject value object raises TypeError when value is not a string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringUuidV5ValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringUuidV5ValueObject(value=StringUuidV5Mother.invalid_type())


@mark.unit_testing
def test_string_uuid5_value_object_empty_string() -> None:
    """
    Test StringUuidV5ValueObject value object raises ValueError when value is empty string.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV5ValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        StringUuidV5ValueObject(value=StringMother.empty())


@mark.unit_testing
def test_string_uuid5_value_object_invalid_uuid() -> None:
    """
    Test StringUuidV5ValueObject value object raises ValueError when value is not a valid UUID.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV5ValueObject value <<<.*>>> is not a valid UUID.',
    ):
        StringUuidV5ValueObject(value=StringMother.create())


@mark.unit_testing
def test_string_uuid5_value_object_invalid_version() -> None:
    """
    Test StringUuidV5ValueObject value object raises ValueError when value is not UUID version 5.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidV5ValueObject value <<<.*>>> must be a UUID version 5. Got version <<<.*>>>.',
    ):
        StringUuidV5ValueObject(value=StringUuidMother.create(exclude_versions={5}))
