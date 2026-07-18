"""
Test DomainOrLocalhostValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import DomainOrLocalhostValueObject


@mark.unit_testing
def test_domain_or_localhost_value_object_accepts_domain() -> None:
    """
    Test DomainOrLocalhostValueObject accepts domain values.
    """
    assert DomainOrLocalhostValueObject(value='Example.COM.').value == 'example.com'


@mark.unit_testing
def test_domain_or_localhost_value_object_accepts_localhost() -> None:
    """
    Test DomainOrLocalhostValueObject accepts and normalizes localhost.
    """
    assert DomainOrLocalhostValueObject(value='LOCALHOST.').value == 'localhost'


@mark.unit_testing
def test_domain_or_localhost_value_object_rejects_other_single_label_hostnames() -> None:
    """
    Test DomainOrLocalhostValueObject rejects other single-label hostnames.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainOrLocalhostValueObject value <<<database>>> has not a valid top level domain.',
    ):
        DomainOrLocalhostValueObject(value='database')
