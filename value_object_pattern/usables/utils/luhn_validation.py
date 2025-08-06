"""
Luhn algorithm validation module.
"""


def validate_luhn_checksum(value: str) -> bool:
    """
    Performs Luhn algorithm validation on the provided `value`.

    Args:
        value (str): The value to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    digits = [int(digit) for digit in value]

    odd_digits = digits[-1::-2]
    checksum = sum(odd_digits)

    even_digits = digits[-2::-2]
    for digit in even_digits:
        checksum += sum(divmod(digit * 2, 10))

    return checksum % 10 == 0
