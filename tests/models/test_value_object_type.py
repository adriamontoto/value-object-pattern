"""
Test ValueObject type resolution.
"""

from sys import version_info
from typing import Generic, TypeVar

if version_info >= (3, 12):
    pass  # pragma: no cover
else:
    pass  # pragma: no cover

from pytest import MonkeyPatch, mark

from value_object_pattern import ValueObject

TItem = TypeVar('TItem')


class GenericFirstValueObject(Generic[TItem], ValueObject[int]):  # noqa: UP046
    """
    Value object with Generic in original bases before ValueObject.
    """


class OriginSkippingValueObject(ValueObject[int]):
    """
    Value object used to exercise non-ValueObject original base skipping.
    """


class NotValueObjectOrigin:
    """
    Fake original base with an origin that is not a ValueObject.
    """

    __origin__ = str


@mark.unit_testing
def test_value_object_type_skips_plain_generic_orig_base() -> None:
    """
    Test ValueObject.type skips Generic bases before resolving the ValueObject type.
    """
    assert GenericFirstValueObject.type() is int


@mark.unit_testing
def test_value_object_type_skips_non_value_object_orig_base(monkeypatch: MonkeyPatch) -> None:
    """
    Test ValueObject.type skips original bases whose origin is not ValueObject.
    """
    monkeypatch.setattr(
        OriginSkippingValueObject,
        '__orig_bases__',
        (NotValueObjectOrigin(), *OriginSkippingValueObject.__orig_bases__),  # type: ignore[attr-defined]
    )

    assert OriginSkippingValueObject.type() is int
