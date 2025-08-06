"""
CountryTldValueObject value object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import (
    get_iso3166_alpha2_to_alpha3_mapping,
    get_iso3166_alpha2_to_numeric_mapping,
    get_iso3166_alpha2_to_phone_code_mapping,
    get_iso3166_alpha2_to_tld_mapping,
)

if TYPE_CHECKING:
    from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject
    from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject
    from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject
    from .phone_code_value_object import PhoneCodeValueObject


class CountryTldValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CountryTldValueObject value object ensures the provided value is a valid country TLD. A country TLD is a string
    that starts with '.' followed by a two-letter country code.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world import CountryTldValueObject

    tld = CountryTldValueObject(value='.es')

    print(repr(tld))
    # >>> CountryTldValueObject(value=.es)
    ```
    """

    @process(order=0)
    def _ensure_value_is_lower(self, value: str) -> str:
        """
        Ensures the value object `value` is stored in lower case.

        Args:
            value (str): The provided value.

        Returns:
            str: Lower case value.
        """
        return value.lower()

    @process(order=1)
    def _ensure_value_starts_without_dot(self, value: str) -> str:
        """
        Ensures the value object `value` starts without a '.'.

        Args:
            value (str): The provided value.

        Returns:
            str: Value without leading '.'.
        """
        return value.lstrip('.')

    @validation(order=0)
    def _ensure_value_is_valid_tld(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid country TLD.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid country TLD.
        """
        tlds = get_iso3166_alpha2_to_tld_mapping()[1]

        if value.lstrip('.').lower() not in tlds:
            self._raise_value_is_not_valid_tld(value=value)

    def _raise_value_is_not_valid_tld(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid country TLD.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid country TLD.
        """
        raise ValueError(f'CountryTldValueObject value <<<{value}>>> is not a valid country TLD.')  # noqa: E501  # fmt: skip

    def to_alpha2(self) -> Iso3166Alpha2CodeValueObject:
        """
        Converts the country TLD to its corresponding ISO 3166-1 alpha-2 code.

        Returns:
            Iso3166Alpha2CodeValueObject: The corresponding ISO 3166-1 alpha-2 code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import CountryTldValueObject

        tld = CountryTldValueObject(value='.es')
        alpha2_code = tld.to_alpha2()
        print(repr(alpha2_code))
        # >>> Iso3166Alpha2CodeValueObject(value=ES)
        ```
        """
        from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject

        _, tld_to_alpha2 = get_iso3166_alpha2_to_tld_mapping()

        return Iso3166Alpha2CodeValueObject(value=tld_to_alpha2[self.value])

    def to_alpha3(self) -> Iso3166Alpha3CodeValueObject:
        """
        Converts the country TLD to its corresponding ISO 3166-1 alpha-3 code.

        Returns:
            Iso3166Alpha3CodeValueObject: The corresponding ISO 3166-1 alpha-3 code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import CountryTldValueObject

        tld = CountryTldValueObject(value='.es')
        alpha3_code = tld.to_alpha3()
        print(repr(alpha3_code))
        # >>> Iso3166Alpha3CodeValueObject(value=ESP)
        ```
        """
        from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject

        _, tld_to_alpha2 = get_iso3166_alpha2_to_tld_mapping()
        alpha2_to_alpha3, _ = get_iso3166_alpha2_to_alpha3_mapping()

        return Iso3166Alpha3CodeValueObject(value=alpha2_to_alpha3[tld_to_alpha2[self.value]])

    def to_numeric(self) -> Iso3166NumericCodeValueObject:
        """
        Converts the country TLD to its corresponding ISO 3166-1 numeric code.

        Returns:
            Iso3166NumericCodeValueObject: The corresponding ISO 3166-1 numeric code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import CountryTldValueObject

        tld = CountryTldValueObject(value='.es')
        numeric_code = tld.to_numeric()
        print(repr(numeric_code))
        # >>> Iso3166NumericCodeValueObject(value=724)
        ```
        """
        from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject

        _, tld_to_alpha2 = get_iso3166_alpha2_to_tld_mapping()
        alpha2_to_numeric, _ = get_iso3166_alpha2_to_numeric_mapping()

        return Iso3166NumericCodeValueObject(value=alpha2_to_numeric[tld_to_alpha2[self.value]])

    def to_phone_code(self) -> PhoneCodeValueObject:
        """
        Converts the country TLD to its corresponding phone code.

        Returns:
            PhoneCodeValueObject: The corresponding phone code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import CountryTldValueObject

        tld = CountryTldValueObject(value='.es')
        phone_code = tld.to_phone_code()
        print(repr(phone_code))
        # >>> PhoneCodeValueObject(value=+34)
        ```
        """
        from .phone_code_value_object import PhoneCodeValueObject

        _, tld_to_alpha2 = get_iso3166_alpha2_to_tld_mapping()
        alpha2_to_phone_code, _ = get_iso3166_alpha2_to_phone_code_mapping()

        try:
            return PhoneCodeValueObject(value=alpha2_to_phone_code[tld_to_alpha2[self.value]])

        except KeyError:
            self._raise_tld_has_no_conversion_to_phone_code(value=self.value)

    def _raise_tld_has_no_conversion_to_phone_code(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the country TLD has no conversion to a phone code.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the country TLD has no conversion to a phone code.
        """
        raise ValueError(f'CountryTldValueObject value <<<{value}>>> has no conversion to a phone code.')
