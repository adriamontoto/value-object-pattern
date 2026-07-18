"""
Test SecretValueObject composition.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from re import escape
from typing import Any

from object_mother_pattern import BooleanMother, IntegerMother, StringMother
from object_mother_pattern.models import DictMother, ListMother
from pytest import mark, raises

from value_object_pattern import BaseModel, SecretValueObject, ValueObject, process
from value_object_pattern.models.collections import DictValueObject, ListValueObject
from value_object_pattern.models.primitive_conversion import to_primitive
from value_object_pattern.usables import BooleanValueObject, IntegerValueObject, StringValueObject


class SecretStringBefore(SecretValueObject, StringValueObject):
    """
    Secret marker before its string value object.
    """


class SecretStringAfter(StringValueObject, SecretValueObject):
    """
    Secret marker after its string value object.
    """


class SecretIntegerBefore(SecretValueObject, IntegerValueObject):
    """
    Secret marker before its integer value object.
    """


class SecretIntegerAfter(IntegerValueObject, SecretValueObject):
    """
    Secret marker after its integer value object.
    """


class SecretBooleanBefore(SecretValueObject, BooleanValueObject):
    """
    Secret marker before its boolean value object.
    """


class SecretBooleanAfter(BooleanValueObject, SecretValueObject):
    """
    Secret marker after its boolean value object.
    """


class SecretListBefore(SecretValueObject, ListValueObject[str]):
    """
    Secret marker before its list value object.
    """


class SecretListAfter(ListValueObject[str], SecretValueObject):
    """
    Secret marker after its list value object.
    """


class SecretDictBefore(SecretValueObject, DictValueObject[str, str]):
    """
    Secret marker before its dictionary value object.
    """


class SecretDictAfter(DictValueObject[str, str], SecretValueObject):
    """
    Secret marker after its dictionary value object.
    """


class AnyListValueObject(ListValueObject[Any]):
    """
    List value object accepting any nested value.
    """


class SecretHolder(BaseModel):
    """
    Model containing a secret value object.
    """

    def __init__(self, *, secret: ValueObject[Any]) -> None:
        """
        Initialize the holder.
        """
        self.secret = secret


class ProcessedStringValueObject(StringValueObject):
    """
    String value object that uppercases its stored value.
    """

    @process(order=0)
    def _uppercase(self, value: str) -> str:
        """
        Return the uppercased value.
        """
        return value.upper()


class SecretProcessedStringBefore(SecretValueObject, ProcessedStringValueObject):
    """
    Secret marker before a processed string value object.
    """


class SecretProcessedStringAfter(ProcessedStringValueObject, SecretValueObject):
    """
    Secret marker after a processed string value object.
    """


class CustomDisplayStringValueObject(StringValueObject):
    """
    String value object with a custom non-secret display value.
    """

    @override
    def _value_for_display(self) -> str:
        """
        Return a custom display value.
        """
        return 'custom-display'


class SecretCustomDisplayString(CustomDisplayStringValueObject, SecretValueObject):
    """
    Secret marker after a custom display value object.
    """


class CustomMaskSecretString(SecretValueObject, StringValueObject):
    """
    Secret string composition with a custom mask.
    """

    _MASK = '[REDACTED]'


@mark.unit_testing
def test_secret_value_object_redacts_all_representative_types_in_either_order() -> None:
    """
    Test secret composition with scalar and collection value objects in either inheritance order.
    """
    string_value = StringMother.create()
    integer_value = IntegerMother.create()
    boolean_value = BooleanMother.create()
    list_value = ListMother.of_length(length=3, item_mother=StringMother.create)
    dict_value = DictMother.of_length(length=3, key_mother=StringMother.create, value_mother=StringMother.create)

    secret_values: tuple[ValueObject[Any], ...] = (
        SecretStringBefore(value=string_value),
        SecretStringAfter(value=string_value),
        SecretIntegerBefore(value=integer_value),
        SecretIntegerAfter(value=integer_value),
        SecretBooleanBefore(value=boolean_value),
        SecretBooleanAfter(value=boolean_value),
        SecretListBefore(value=list_value),
        SecretListAfter(value=list_value),
        SecretDictBefore(value=dict_value),
        SecretDictAfter(value=dict_value),
    )

    for secret in secret_values:
        assert str(secret) == '********'
        assert repr(secret) == f"{secret.__class__.__name__}(value='********')"
        assert to_primitive(value=secret) == secret.value


@mark.unit_testing
def test_secret_value_object_preserves_wrapped_value_types() -> None:
    """
    Test the accompanying value-object bases retain their wrapped types.
    """
    string_before: str = SecretStringBefore(value=StringMother.create()).value
    string_after: str = SecretStringAfter(value=StringMother.create()).value
    integer_before: int = SecretIntegerBefore(value=IntegerMother.create()).value
    integer_after: int = SecretIntegerAfter(value=IntegerMother.create()).value
    boolean_before: bool = SecretBooleanBefore(value=BooleanMother.create()).value
    boolean_after: bool = SecretBooleanAfter(value=BooleanMother.create()).value
    list_before: list[str] = SecretListBefore(value=ListMother.create(item_mother=StringMother.create)).value
    list_after: list[str] = SecretListAfter(value=ListMother.create(item_mother=StringMother.create)).value
    dict_before: dict[str, str] = SecretDictBefore(
        value=DictMother.create(key_mother=StringMother.create, value_mother=StringMother.create)
    ).value
    dict_after: dict[str, str] = SecretDictAfter(
        value=DictMother.create(key_mother=StringMother.create, value_mother=StringMother.create)
    ).value

    assert type(string_before) is type(string_after) is str
    assert type(integer_before) is type(integer_after) is int
    assert type(boolean_before) is type(boolean_after) is bool
    assert type(list_before) is type(list_after) is list
    assert type(dict_before) is type(dict_after) is dict


@mark.unit_testing
def test_secret_value_object_preserves_validation_in_either_order() -> None:
    """
    Test secret composition does not bypass its accompanying value-object validation.
    """
    invalid_value = StringMother.invalid_type()

    for value_object_type in (SecretStringBefore, SecretStringAfter):
        expected_message = (
            f'{value_object_type.__name__} value <<<{invalid_value}>>> must be a string. '
            f'Got <<<{type(invalid_value).__name__}>>> type.'
        )

        with raises(TypeError, match=escape(expected_message)):
            value_object_type(value=invalid_value)


@mark.unit_testing
def test_secret_value_object_preserves_processing_in_either_order() -> None:
    """
    Test secret composition does not bypass its accompanying value-object processing.
    """
    raw_value = StringMother.create(value='hidden-value')

    for value_object_type in (SecretProcessedStringBefore, SecretProcessedStringAfter):
        secret = value_object_type(value=raw_value)

        assert secret.value == raw_value.upper()
        assert str(secret) == '********'


@mark.unit_testing
def test_secret_value_object_redaction_precedes_custom_display_hooks() -> None:
    """
    Test secret redaction takes precedence over a value object's regular display hook.
    """
    raw_value = StringMother.create()
    secret = SecretCustomDisplayString(value=raw_value)

    assert secret.value == raw_value
    assert str(secret) == '********'
    assert repr(secret) == "SecretCustomDisplayString(value='********')"


@mark.unit_testing
def test_secret_value_object_supports_custom_masks() -> None:
    """
    Test secret compositions may customize their fixed display mask.
    """
    raw_value = StringMother.create()
    secret = CustomMaskSecretString(value=raw_value)

    assert secret.value == raw_value
    assert str(secret) == '[REDACTED]'
    assert repr(secret) == "CustomMaskSecretString(value='[REDACTED]')"


@mark.unit_testing
def test_secret_value_object_redacts_nested_model_and_collection_display_paths() -> None:
    """
    Test nested display paths redact secrets while primitive conversion keeps raw values.
    """
    raw_value = StringMother.create()
    secret = SecretStringAfter(value=raw_value)
    holder = SecretHolder(secret=secret)
    sequence = AnyListValueObject(value=[StringMother.create(), secret, StringMother.create()])

    assert holder.to_primitives() == {'secret': raw_value}
    assert sequence.to_primitives()[1] == raw_value

    for displayed_value in (str(holder), repr(holder), str(sequence), repr(sequence)):
        assert raw_value not in displayed_value
        assert '********' in displayed_value
