"""
PhoneCodeValueObject value object.
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
    from .country_tld_value_object import CountryTldValueObject
    from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject
    from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject
    from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject


class PhoneCodeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    PhoneCodeValueObject value object ensures the provided value is a valid phone code. A phone code is a string that
    starts with '+' followed by digits representing a country's phone code.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject

    phone_code = PhoneCodeValueObject(value='+34')

    print(repr(phone_code))
    # >>> PhoneCodeValueObject(value=34)
    ```
    """

    @process(order=0)
    def _ensure_value_starts_without_plus(self, value: str) -> str:
        """
        Ensures the phone code starts without a '+' sign.

        Args:
            value (str): The provided value.

        Returns:
            str: The phone code value with a leading '+' if not present.
        """
        return value.lstrip('+')

    @validation(order=0)
    def _ensure_value_is_valid_phone_code(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid phone code.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid phone code.
        """
        phone_codes = get_iso3166_alpha2_to_phone_code_mapping()[1]

        if value.lstrip('+') not in phone_codes:
            self._raise_value_is_not_valid_phone_code(value=value)

    def _raise_value_is_not_valid_phone_code(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid phone code.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid phone code.
        """
        raise ValueError(f'PhoneCodeValueObject value <<<{value}>>> is not a valid phone code.')  # noqa: E501  # fmt: skip

    def to_alpha2(self) -> Iso3166Alpha2CodeValueObject:
        """
        Converts the phone code to its corresponding ISO 3166-1 alpha-2 code.

        Returns:
            Iso3166Alpha2CodeValueObject: The corresponding ISO 3166-1 alpha-2 code.

        Raises:
            ValueError: If the phone code has no conversion to ISO 3166-1 alpha-2 code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject

        phone_code = PhoneCodeValueObject(value='+34')
        alpha2_code = phone_code.to_alpha2()
        print(repr(alpha2_code))
        # >>> Iso3166Alpha2CodeValueObject(value=ES)
        ```
        """
        from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject

        _, phone_code_to_alpha2 = get_iso3166_alpha2_to_phone_code_mapping()

        try:
            return Iso3166Alpha2CodeValueObject(value=phone_code_to_alpha2[self.value])

        except KeyError:
            self._raise_phone_code_has_no_conversion(value=self.value)

    def to_alpha3(self) -> Iso3166Alpha3CodeValueObject:
        """
        Converts the phone code to its corresponding ISO 3166-1 alpha-3 code.

        Raises:
            ValueError: If the phone code has no conversion to ISO 3166-1 alpha-3 code.

        Returns:
            Iso3166Alpha3CodeValueObject: The corresponding ISO 3166-1 alpha-3 code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject

        phone_code = PhoneCodeValueObject(value='+34')
        alpha3_code = phone_code.to_alpha3()
        print(repr(alpha3_code))
        # >>> Iso3166Alpha3CodeValueObject(value=ESP)
        ```
        """
        from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject

        _, phone_code_to_alpha2 = get_iso3166_alpha2_to_phone_code_mapping()
        alpha2_to_alpha3, _ = get_iso3166_alpha2_to_alpha3_mapping()

        try:
            return Iso3166Alpha3CodeValueObject(value=alpha2_to_alpha3[phone_code_to_alpha2[self.value]])

        except KeyError:
            self._raise_phone_code_has_no_conversion(value=self.value)

    def to_numeric(self) -> Iso3166NumericCodeValueObject:
        """
        Converts the phone code to its corresponding ISO 3166-1 numeric code.

        Raises:
            ValueError: If the phone code has no conversion to ISO 3166-1 numeric code.

        Returns:
            Iso3166NumericCodeValueObject: The corresponding ISO 3166-1 numeric code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject

        phone_code = PhoneCodeValueObject(value='+34')
        numeric_code = phone_code.to_numeric()
        print(repr(numeric_code))
        # >>> Iso3166NumericCodeValueObject(value=724)
        ```
        """
        from .iso3166_numeric_code_value_object import Iso3166NumericCodeValueObject

        _, phone_code_to_alpha2 = get_iso3166_alpha2_to_phone_code_mapping()
        alpha2_to_numeric, _ = get_iso3166_alpha2_to_numeric_mapping()

        try:
            return Iso3166NumericCodeValueObject(value=alpha2_to_numeric[phone_code_to_alpha2[self.value]])

        except KeyError:
            self._raise_phone_code_has_no_conversion(value=self.value)

    def to_tld(self) -> CountryTldValueObject:
        """
        Converts the phone code to its corresponding country TLD.

        Raises:
            ValueError: If the phone code has no conversion to a country TLD.

        Returns:
            CountryTldValueObject: The corresponding country TLD.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import PhoneCodeValueObject

        phone_code = PhoneCodeValueObject(value='+34')
        tld = phone_code.to_tld()
        print(repr(tld))
        # >>> CountryTldValueObject(value=es)
        ```
        """
        from .country_tld_value_object import CountryTldValueObject

        _, phone_code_to_alpha2 = get_iso3166_alpha2_to_phone_code_mapping()
        alpha2_to_tld, _ = get_iso3166_alpha2_to_tld_mapping()

        try:
            return CountryTldValueObject(value=alpha2_to_tld[phone_code_to_alpha2[self.value]])

        except KeyError:
            self._raise_phone_code_has_no_conversion(value=self.value)

    def _raise_phone_code_has_no_conversion(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the phone code has no conversion to ISO 3166-1 alpha-2 code.

        Args:
            value (str): The provided phone code value.

        Raises:
            ValueError: If the phone code has no conversion.
        """
        raise ValueError(f'PhoneCodeValueObject value <<<{value}>>> has no conversion to ISO 3166-1 alpha-2 code.')
