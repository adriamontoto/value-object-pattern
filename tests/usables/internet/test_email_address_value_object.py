"""
Test EmailAddressValueObject value object.
"""

from pytest import CaptureFixture, mark, raises as assert_raises

from value_object_pattern.usables.internet import EmailAddressValueObject


@mark.unit_testing
def test_email_address_value_object_happy_path() -> None:
    """
    Test EmailAddressValueObject value object happy path.
    """
    email = EmailAddressValueObject(value='User.Name+Tag@Example.COM')

    assert type(email.value) is str
    assert email.value == 'user.name+tag@example.com'


@mark.unit_testing
def test_email_address_value_object_too_short() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when value is too short.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<a@b.c>>> must be at least <<<6>>> characters long.',
    ):
        EmailAddressValueObject(value='a@b.c')


@mark.unit_testing
def test_email_address_value_object_long_local_part() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when local part is too long.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<.*>>> local part <<<.*>>> must be at most <<<64>>> characters long.',
    ):
        EmailAddressValueObject(value=f'{"a" * 65}@example.com')


@mark.unit_testing
def test_email_address_value_object_missing_at_symbol() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when value does not contain an at symbol.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<without-at-symbol.example.com>>> must contain a single "@" symbol.',
    ):
        EmailAddressValueObject(value='without-at-symbol.example.com')


@mark.unit_testing
def test_email_address_value_object_empty_local_part() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when local part is empty.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<@example.com>>> local part <<<>>> must be at least <<<1>>> characters long.',  # noqa: E501
    ):
        EmailAddressValueObject(value='@example.com')


@mark.unit_testing
def test_email_address_value_object_invalid_local_part() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when local part contains invalid characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<bad space@example.com>>> local part <<<bad space>>> contains invalid characters.',  # noqa: E501
    ):
        EmailAddressValueObject(value='bad space@example.com')


@mark.unit_testing
def test_email_address_value_object_invalid_domain_characters() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when domain part contains invalid characters.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<user@exa_mple.com>>> domain part <<<exa_mple.com>>> contains invalid characters.',  # noqa: E501
    ):
        EmailAddressValueObject(value='user@exa_mple.com')


@mark.unit_testing
def test_email_address_value_object_invalid_domain(capsys: CaptureFixture[str]) -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when domain is invalid.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<user@example.invalidtldunlikely>>> has an invalid domain <<<example.invalidtldunlikely>>>.',  # noqa: E501
    ):
        EmailAddressValueObject(value='user@example.invalidtldunlikely')

    assert capsys.readouterr().out == ''


@mark.unit_testing
def test_email_address_value_object_too_long() -> None:
    """
    Test EmailAddressValueObject value object raises ValueError when value is too long.
    """
    with assert_raises(
        expected_exception=ValueError,
        match=r'EmailAddressValueObject value <<<.*>>> must be at most <<<320>>> characters long.',
    ):
        EmailAddressValueObject(value=f'{"a" * 65}@{"b" * 253}.com')
