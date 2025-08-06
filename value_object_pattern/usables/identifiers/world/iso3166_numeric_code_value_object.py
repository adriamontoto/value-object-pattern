"""
Iso3166NumericCodeValueObject value object.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.usables import PositiveIntegerValueObject

from .utils import (
    get_iso3166_alpha2_to_alpha3_mapping,
    get_iso3166_alpha2_to_numeric_mapping,
    get_iso3166_alpha2_to_phone_code_mapping,
    get_iso3166_alpha2_to_tld_mapping,
    get_iso3166_numeric_codes,
)

if TYPE_CHECKING:
    from .country_tld_value_object import CountryTldValueObject
    from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject
    from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject
    from .phone_code_value_object import PhoneCodeValueObject


class Iso3166NumericCodeValueObject(PositiveIntegerValueObject):
    """
    Iso3166NumericCodeValueObject value object ensures the provided value is a valid ISO 3166-1 numeric country code. An
    ISO 3166-1 numeric country code is a string with 3 digits representing a country or territory.

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world import Iso3166NumericCodeValueObject

    country_code = Iso3166NumericCodeValueObject(value=274)

    print(repr(country_code))
    # >>> Iso3166NumericCodeValueObject(value=274)
    ```
    """

    @validation(order=0)
    def _ensure_value_is_iso3166_numeric(self, value: int) -> None:
        """
        Ensures the value object `value` is a valid ISO 3166-1 numeric country code.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a valid ISO 3166-1 numeric country code.
        """
        if value not in get_iso3166_numeric_codes():
            self._raise_value_is_not_iso3166_numeric(value=value)

    def _raise_value_is_not_iso3166_numeric(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid ISO 3166-1 numeric country code.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the `value` is not a valid ISO 3166-1 numeric country code.
        """
        raise ValueError(f'Iso3166NumericCodeValueObject value <<<{value}>>> is not a valid ISO 3166-1 numeric country code.')  # noqa: E501  # fmt: skip

    def to_alpha2_code(self) -> Iso3166Alpha2CodeValueObject:
        """
        Converts the ISO 3166-1 numeric code to an ISO 3166-1 alpha-2 country code.

        Returns:
            Iso3166Alpha2CodeValueObject: The corresponding ISO 3166-1 alpha-2 code.
        """
        from .iso3166_alpha2_code_value_object import Iso3166Alpha2CodeValueObject

        _, numeric_to_alpha2 = get_iso3166_alpha2_to_numeric_mapping()

        return Iso3166Alpha2CodeValueObject(value=numeric_to_alpha2[self.value])

    def to_alpha3_code(self) -> Iso3166Alpha3CodeValueObject:
        """
        Converts the ISO 3166-1 numeric code to an ISO 3166-1 alpha-3 country code.

        Returns:
            Iso3166Alpha3CodeValueObject: The corresponding ISO 3166-1 alpha-3 code.
        """
        from .iso3166_alpha3_code_value_object import Iso3166Alpha3CodeValueObject

        _, numeric_to_alpha2 = get_iso3166_alpha2_to_numeric_mapping()
        alpha2_to_alpha3, _ = get_iso3166_alpha2_to_alpha3_mapping()

        return Iso3166Alpha3CodeValueObject(value=alpha2_to_alpha3[numeric_to_alpha2[self.value]])

    def to_phone_code(self) -> PhoneCodeValueObject:
        """
        Converts the ISO 3166-1 numeric code to its corresponding phone code.

        Returns:
            PhoneCodeValueObject: The corresponding phone code.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166NumericCodeValueObject

        country_code = Iso3166NumericCodeValueObject(value=724)
        phone_code = country_code.to_phone_code()
        print(repr(phone_code))
        # >>> PhoneCodeValueObject(value=+34)
        ```
        """
        from .phone_code_value_object import PhoneCodeValueObject

        _, numeric_to_alpha2 = get_iso3166_alpha2_to_numeric_mapping()
        alpha2_to_phone_code, _ = get_iso3166_alpha2_to_phone_code_mapping()

        try:
            return PhoneCodeValueObject(value=alpha2_to_phone_code[numeric_to_alpha2[self.value]])

        except KeyError:
            self._raise_numeric_has_no_conversion_to_phone_code(value=self.value)

    def _raise_numeric_has_no_conversion_to_phone_code(self, value: int) -> NoReturn:
        """
        Raises a ValueError if the ISO 3166-1 numeric code has no conversion to a phone code.

        Args:
            value (int): The provided value.

        Raises:
            ValueError: If the ISO 3166-1 numeric code has no conversion to a phone code.
        """
        raise ValueError(f'Iso3166NumericCodeValueObject value <<<{value}>>> has no conversion to a phone code.')

    def to_tld(self) -> CountryTldValueObject:
        """
        Converts the ISO 3166-1 numeric code to its corresponding country TLD.

        Returns:
            CountryTldValueObject: The corresponding country TLD.

        Example:
        ```python
        from value_object_pattern.usables.identifiers.world import Iso3166NumericCodeValueObject

        country_code = Iso3166NumericCodeValueObject(value=724)
        tld = country_code.to_tld()
        print(repr(tld))
        # >>> CountryTldValueObject(value=.es)
        ```
        """
        from .country_tld_value_object import CountryTldValueObject

        _, numeric_to_alpha2 = get_iso3166_alpha2_to_numeric_mapping()
        alpha2_to_tld, _ = get_iso3166_alpha2_to_tld_mapping()

        return CountryTldValueObject(value=alpha2_to_tld[numeric_to_alpha2[self.value]])
