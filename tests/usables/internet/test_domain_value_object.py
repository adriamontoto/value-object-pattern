"""
Test DomainValueObject value object.
"""

from pytest import mark, raises as assert_raises

from value_object_pattern.usables.internet import DomainValueObject


@mark.unit_testing
def test_domain_value_object_happy_path() -> None:
    """
    Test DomainValueObject value object happy path.
    """
    domain = DomainValueObject(value='Example.COM.')

    assert type(domain.value) is str
    assert domain.value == 'example.com'


@mark.unit_testing
def test_domain_value_object_accepts_idna_label() -> None:
    """
    Test DomainValueObject value object accepts IDNA labels.
    """
    assert DomainValueObject(value='xn--bcher-kva.com').value == 'xn--bcher-kva.com'


@mark.unit_testing
def test_domain_value_object_invalid_top_level_domain() -> None:
    """
    Test DomainValueObject value object raises ValueError when top-level domain is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<localhost>>> has not a valid top level domain.',
    ):
        DomainValueObject(value='localhost')


@mark.unit_testing
def test_domain_value_object_invalid_domain_length() -> None:
    """
    Test DomainValueObject value object raises ValueError when domain length is invalid.
    """
    invalid_domain = f'{"a" * 250}.com'

    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<.*>>> length is longer than <<<253>>> characters.',
    ):
        DomainValueObject(value=invalid_domain)


@mark.unit_testing
def test_domain_value_object_invalid_empty_label() -> None:
    """
    Test DomainValueObject value object raises ValueError when a domain label is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<example..com>>> has a label <<<>>> shorter than <<<1>>> characters.',
    ):
        DomainValueObject(value='example..com')


@mark.unit_testing
def test_domain_value_object_invalid_long_label() -> None:
    """
    Test DomainValueObject value object raises ValueError when a domain label is too long.
    """
    invalid_label = 'a' * 64

    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<.*>>> has a label <<<.*>>> longer than <<<63>>> characters.',
    ):
        DomainValueObject(value=f'{invalid_label}.com')


@mark.unit_testing
def test_domain_value_object_invalid_leading_hyphen() -> None:
    """
    Test DomainValueObject value object raises ValueError when a domain label starts with a hyphen.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<-example.com>>> has a label <<<-example>>> with invalid format',
    ):
        DomainValueObject(value='-example.com')


@mark.unit_testing
def test_domain_value_object_invalid_trailing_hyphen() -> None:
    """
    Test DomainValueObject value object raises ValueError when a domain label ends with a hyphen.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<example-.com>>> has a label <<<example->>> with invalid format',
    ):
        DomainValueObject(value='example-.com')


@mark.unit_testing
def test_domain_value_object_invalid_characters() -> None:
    """
    Test DomainValueObject value object raises ValueError when a domain label contains invalid characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'DomainValueObject value <<<exa_mple.com>>> has a label <<<exa_mple>>> with invalid format',
    ):
        DomainValueObject(value='exa_mple.com')
