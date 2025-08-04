"""
Iso3166Alpha2CodeValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import get_iso3166_alpha2_codes


class Iso3166Alpha2CodeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Iso3166Alpha2CodeValueObject value object ensures the provided value is a valid ISO 3166-1 alpha-2 country code. An
    ISO 3166-1 alpha-2 country code is a string with 2 uppercase letters representing a country or territory.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries import Iso3166Alpha2CodeValueObject

    country_code = Iso3166Alpha2CodeValueObject(value='ES')

    print(repr(country_code))
    # >>> Iso3166Alpha2CodeValueObject(value=ES)
    ```
    """

    @process(order=0)
    def _ensure_value_is_upper(self, value: str) -> str:
        """
        Ensures the value object `value` is an upper string.

        Args:
            value (str): The provided value.

        Returns:
            str: Upper case value.
        """
        return value.upper()

    @validation(order=0)
    def _ensure_value_is_iso3166_alpha2(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid ISO 3166-1 alpha-2 country code.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid ISO 3166-1 alpha-2 country code.
        """
        if value.upper() not in get_iso3166_alpha2_codes():
            self._raise_value_is_not_iso3166_alpha2(value=value)

    def _raise_value_is_not_iso3166_alpha2(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid ISO 3166-1 alpha-2 country code.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid ISO 3166-1 alpha-2 country code.
        """
        raise ValueError(f'Iso3166Alpha2CodeValueObject value <<<{value}>>> is not a valid ISO 3166-1 alpha-2 country code.')  # noqa: E501  # fmt: skip
