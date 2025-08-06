"""
Iso3166Alpha2CodeValueObject value object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import (
    get_iso3166_alpha2_codes,
    get_iso3166_alpha2_to_alpha3_mapping,
    get_iso3166_alpha2_to_numeric_mapping,
    get_iso3166_alpha2_to_phone_code_mapping,
    get_iso3166_alpha2_to_tld_mapping,
)

if TYPE_CHECKING:
    from .country_tld_value_object import CountryTldValueObject
    from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject
    from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject
    from .phone_code_value_object import PhoneCodeValueObject


class Iso3166Alpha2CodeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Iso3166Alpha2CodeValueObject value object ensures the provided value is a valid ISO 3166-1 alpha-2 country code. An
    ISO 3166-1 alpha-2 country code is a string with 2 uppercase letters representing a country or territory.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject

    country_code = Iso3166Alpha2CodeValueObject(value='ES')

    print(repr(country_code))
    # >>> Iso3166Alpha2CodeValueObject(value=ES)
    ```
    """

    @process(order=0)
    def _ensure_value_is_upper(self, value: str) -> str:
        """
        Ensures the value object `value` is stored in upper case.

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

    def to_alpha3(self) -> Iso3166Alpha3CodeValueObject:
        """
        Converts the ISO 3166-1 alpha-2 code to its corresponding ISO 3166-1 alpha-3 code.

        Returns:
            Iso3166Alpha3CodeValueObject: The corresponding ISO 3166-1 alpha-3 code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject

        country_code = Iso3166Alpha2CodeValueObject(value='ES')
        alpha3_code = country_code.to_alpha3()
        print(repr(alpha3_code))
        # >>> Iso3166Alpha3CodeValueObject(value=ESP)
        ```
        """
        from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject

        alpha2_to_alpha3, _ = get_iso3166_alpha2_to_alpha3_mapping()

        return Iso3166Alpha3CodeValueObject(value=alpha2_to_alpha3[self.value])

    def to_numeric(self) -> Iso3166NumericCodeValueObject:
        """
        Converts the ISO 3166-1 alpha-2 code to its corresponding ISO 3166-1 numeric code.

        Returns:
            Iso3166NumericCodeValueObject: The corresponding ISO 3166-1 numeric code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject

        country_code = Iso3166Alpha2CodeValueObject(value='ES')
        numeric_code = country_code.to_numeric()
        print(repr(numeric_code))
        # >>> Iso3166NumericCodeValueObject(value=724)
        ```
        """
        from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject

        alpha2_to_numeric, _ = get_iso3166_alpha2_to_numeric_mapping()

        return Iso3166NumericCodeValueObject(value=alpha2_to_numeric[self.value])

    def to_phone_code(self) -> PhoneCodeValueObject:
        """
        Converts the ISO 3166-1 alpha-2 code to its corresponding phone code.

        Returns:
            PhoneCodeValueObject: The corresponding phone code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject

        country_code = Iso3166Alpha2CodeValueObject(value='ES')
        phone_code = country_code.to_phone_code()
        print(repr(phone_code))
        # >>> PhoneCodeValueObject(value=+34)
        ```
        """
        from .phone_code_value_object import PhoneCodeValueObject

        alpha2_to_phone_code, _ = get_iso3166_alpha2_to_phone_code_mapping()

        try:
            return PhoneCodeValueObject(value=alpha2_to_phone_code[self.value])

        except KeyError:
            self._raise_alpha2_has_no_conversion_to_phone_code(value=self.value)

    def _raise_alpha2_has_no_conversion_to_phone_code(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the ISO 3166-1 alpha-2 code has no conversion to a phone code.

        Args:
            value (str): The provided ISO 3166-1 alpha-2 code.

        Raises:
            ValueError: If the `value` has no conversion to a phone code.
        """
        raise ValueError(f'Iso3166Alpha2CodeValueObject value <<<{value}>>> has no conversion to a phone code.')

    def to_tld(self) -> CountryTldValueObject:
        """
        Converts the ISO 3166-1 alpha-2 code to its corresponding country TLD.

        Returns:
            CountryTldValueObject: The corresponding country TLD.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166Alpha2CodeValueObject

        country_code = Iso3166Alpha2CodeValueObject(value='ES')
        tld = country_code.to_tld()
        print(repr(tld))
        # >>> CountryTldValueObject(value=.es)
        ```
        """
        from .country_tld_value_object import CountryTldValueObject

        alpha2_to_tld, _ = get_iso3166_alpha2_to_tld_mapping()

        return CountryTldValueObject(value=alpha2_to_tld[self.value])
