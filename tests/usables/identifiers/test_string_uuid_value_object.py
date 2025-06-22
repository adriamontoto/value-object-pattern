"""
Test StringUuidValueObject value object.
"""

from object_mother_pattern import StringMother, StringUuidMother
from pytest import mark, raises as assert_raises

from value_object_pattern.usables.identifiers import StringUuidValueObject


@mark.unit_testing
def test_uuid_value_object_happy_path() -> None:
    """
    Test StringUuidValueObject value object happy path.
    """
    uuid_value = StringUuidValueObject(value=StringUuidMother.create())

    assert type(uuid_value.value) is str
    assert uuid_value.value.islower()


@mark.unit_testing
def test_uuid_value_object_empty_value() -> None:
    """
    Test StringUuidValueObject value object raises ValueError when value is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidValueObject value <<<.*>>> is an empty string. Only non-empty strings are allowed.',
    ):
        StringUuidValueObject(value=StringMother.empty())


@mark.unit_testing
def test_uuid_value_object_invalid_value() -> None:
    """
    Test StringUuidValueObject value object raises ValueError when value is not a valid UUID.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'StringUuidValueObject value <<<.*>>> is not a valid UUID.',
    ):
        StringUuidValueObject(value=StringMother.create())


@mark.unit_testing
def test_uuid_value_object_invalid_type() -> None:
    """
    Test StringUuidValueObject value object raises TypeError when value is not an string.
    """
    with assert_raises(
        expected_exception=TypeError,
        match=r'StringUuidValueObject value <<<.*>>> must be a string. Got <<<.*>>> type.',
    ):
        StringUuidValueObject(value=StringUuidMother.invalid_type())
