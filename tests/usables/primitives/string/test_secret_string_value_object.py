"""
Test SecretStringValueObject value object.
"""

from typing import Any

from pytest import mark

from value_object_pattern import BaseModel
from value_object_pattern.models.collections import ListValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, SecretStringValueObject, TrimmedStringValueObject


class SecretHolder(BaseModel):
    """
    Model holding a secret string value object.
    """

    def __init__(self, secret: SecretStringValueObject) -> None:
        """
        SecretHolder constructor.
        """
        self.secret = secret


class AnyListValueObject(ListValueObject[Any]):
    """
    List value object storing any values.
    """


class SecretListValueObject(ListValueObject[SecretStringValueObject]):
    """
    List value object storing secret string value objects.
    """


class NotEmptyTrimmedSecretStringValueObject(
    NotEmptyStringValueObject,
    TrimmedStringValueObject,
    SecretStringValueObject,
):
    """
    Secret string value object with secret behavior after other string constraints.
    """


class SecretNotEmptyTrimmedStringValueObject(
    SecretStringValueObject,
    NotEmptyStringValueObject,
    TrimmedStringValueObject,
):
    """
    Secret string value object with secret behavior before other string constraints.
    """


class TrimmedSecretNotEmptyStringValueObject(
    TrimmedStringValueObject,
    SecretStringValueObject,
    NotEmptyStringValueObject,
):
    """
    Secret string value object with secret behavior between other string constraints.
    """


@mark.unit_testing
def test_secret_string_value_object_happy_path() -> None:
    """
    Test SecretStringValueObject value object happy path.
    """
    raw_value = 'hidden-value'
    secret = SecretStringValueObject(value=raw_value)

    assert type(secret.value) is str
    assert secret.value == raw_value


@mark.unit_testing
def test_secret_string_value_object_redacts_str_and_repr() -> None:
    """
    Test SecretStringValueObject redacts direct string and repr output.
    """
    raw_value = 'hidden-value'
    secret = SecretStringValueObject(value=raw_value)

    assert str(secret) == '********'
    assert repr(secret) == "SecretStringValueObject(value='********')"
    assert raw_value not in str(secret)
    assert raw_value not in repr(secret)


@mark.unit_testing
def test_secret_string_value_object_uses_fixed_mask_for_all_lengths() -> None:
    """
    Test SecretStringValueObject does not leak the raw secret length.
    """
    short_secret = SecretStringValueObject(value='x')
    long_secret = SecretStringValueObject(value='a-much-longer-hidden-value')

    assert str(short_secret) == str(long_secret) == '********'
    assert repr(short_secret) == "SecretStringValueObject(value='********')"
    assert repr(long_secret) == "SecretStringValueObject(value='********')"


@mark.unit_testing
def test_secret_string_value_object_equality_and_hash_use_raw_value() -> None:
    """
    Test SecretStringValueObject keeps value-object equality and hash semantics.
    """
    raw_value = 'hidden-value'

    assert SecretStringValueObject(value=raw_value) == SecretStringValueObject(value=raw_value)
    assert SecretStringValueObject(value=raw_value) != SecretStringValueObject(value='other-hidden-value')
    assert hash(SecretStringValueObject(value=raw_value)) == hash(raw_value)


@mark.unit_testing
def test_secret_string_value_object_redacts_inside_base_model_display_paths() -> None:
    """
    Test SecretStringValueObject redacts when nested inside BaseModel display paths.
    """
    raw_value = 'hidden-value'
    holder = SecretHolder(secret=SecretStringValueObject(value=raw_value))

    assert holder.to_primitives() == {'secret': '********'}
    assert raw_value not in str(holder)
    assert raw_value not in repr(holder)
    assert '********' in str(holder)
    assert '********' in repr(holder)


@mark.unit_testing
def test_secret_string_value_object_redacts_inside_list_value_object_display_paths() -> None:
    """
    Test SecretStringValueObject redacts when nested inside ListValueObject display paths.
    """
    raw_value = 'hidden-value'
    sequence = SecretListValueObject(value=[SecretStringValueObject(value=raw_value)])

    assert sequence.to_primitives() == ['********']
    assert raw_value not in str(sequence)
    assert raw_value not in repr(sequence)
    assert '********' in str(sequence)
    assert '********' in repr(sequence)


@mark.unit_testing
def test_secret_string_value_object_redacts_at_any_list_position() -> None:
    """
    Test SecretStringValueObject redacts regardless of list position.
    """
    first_value = 'first-hidden-value'
    second_value = 'second-hidden-value'
    sequence = AnyListValueObject(
        value=[
            SecretStringValueObject(value=first_value),
            'visible',
            SecretStringValueObject(value=second_value),
        ]
    )

    assert first_value not in str(sequence)
    assert second_value not in str(sequence)
    assert first_value not in repr(sequence)
    assert second_value not in repr(sequence)
    assert str(sequence).count('********') == 2
    assert repr(sequence).count('********') == 2


@mark.unit_testing
def test_secret_string_value_object_redacts_with_mixed_string_base_orders() -> None:
    """
    Test SecretStringValueObject redacts with different string value object base orders.
    """
    raw_value = 'hidden-password'

    for value_object_type in (
        NotEmptyTrimmedSecretStringValueObject,
        SecretNotEmptyTrimmedStringValueObject,
        TrimmedSecretNotEmptyStringValueObject,
    ):
        secret = value_object_type(value=raw_value)

        assert secret.value == raw_value
        assert str(secret) == '********'
        assert repr(secret) == f"{value_object_type.__name__}(value='********')"
        assert raw_value not in str(secret)
        assert raw_value not in repr(secret)


@mark.unit_testing
def test_secret_string_value_object_mixed_with_trimmed_still_rejects_untrimmed_value() -> None:
    """
    Test SecretStringValueObject does not bypass sibling string value object validation.
    """
    for value_object_type in (
        NotEmptyTrimmedSecretStringValueObject,
        SecretNotEmptyTrimmedStringValueObject,
        TrimmedSecretNotEmptyStringValueObject,
    ):
        try:
            value_object_type(value='  hidden-password  ')

        except ValueError:
            continue

        raise AssertionError(f'{value_object_type.__name__} accepted an untrimmed value.')
