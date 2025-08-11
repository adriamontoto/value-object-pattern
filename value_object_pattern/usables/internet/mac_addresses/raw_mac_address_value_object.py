"""
RawMacAddressValueObject value object.
"""

from __future__ import annotations

from re import Pattern, compile as re_compile
from typing import TYPE_CHECKING, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

if TYPE_CHECKING:
    from .cisco_mac_address_value_object import CiscoMacAddressValueObject
    from .space_mac_address_value_object import SpaceMacAddressValueObject
    from .universal_mac_address_value_object import UniversalMacAddressValueObject
    from .windows_mac_address_value_object import WindowsMacAddressValueObject


class RawMacAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    RawMacAddressValueObject value object ensures the provided value is a valid MAC address in raw format
    (D5B9EB4DC2CC).

    Example:
    ```python
    from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject

    mac = RawMacAddressValueObject(value='D5B9EB4DC2CC')
    print(repr(mac))
    # >>> RawMacAddressValueObject(value=D5B9EB4DC2CC)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'[0-9A-F]{12}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'[0-9a-fA-F]{12}')

    @process(order=0)
    def _ensure_value_is_uppercase(self, value: str) -> str:
        """
        Ensures the value object value is uppercase.

        Args:
            value (str): The provided value.

        Returns:
            str: Uppercase value.
        """
        return value.upper()

    @validation(order=0)
    def _ensure_value_is_raw_mac_address(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid raw MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid raw MAC address.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_raw_mac_address(value=value)

    @validation(order=1, early_process=True)
    def _ensure_value_follows_validation_regex(self, value: str, processed_value: str) -> None:
        """
        Ensures the value object `value` follows the validation regex.

        Args:
            value (str): The provided value.
            processed_value (str): The early processed value.

        Raises:
            ValueError: If the `value` does not follow the validation regex.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=processed_value):
            self._raise_value_is_not_raw_mac_address(value=value)

    def _raise_value_is_not_raw_mac_address(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid raw MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid raw MAC address.
        """
        raise ValueError(f'RawMacAddressValueObject value <<<{value}>>> is not a valid raw MAC address.')

    def to_universal(self) -> UniversalMacAddressValueObject:
        """
        Converts the raw MAC address to universal format (D5:B9:EB:4D:C2:CC).

        Returns:
            UniversalMacAddressValueObject: MAC address in universal format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject

        mac = RawMacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_universal()))
        # >>> UniversalMacAddressValueObject(value=D5:B9:EB:4D:C2:CC)
        ```
        """
        from .universal_mac_address_value_object import UniversalMacAddressValueObject

        universal_value = ':'.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return UniversalMacAddressValueObject(value=universal_value)

    def to_windows(self) -> WindowsMacAddressValueObject:
        """
        Converts the raw MAC address to Windows format (D5-B9-EB-4D-C2-CC).

        Returns:
            WindowsMacAddressValueObject: MAC address in Windows format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject

        mac = RawMacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_windows()))
        # >>> WindowsMacAddressValueObject(value=D5-B9-EB-4D-C2-CC)
        ```
        """
        from .windows_mac_address_value_object import WindowsMacAddressValueObject

        windows_value = '-'.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return WindowsMacAddressValueObject(value=windows_value)

    def to_cisco(self) -> CiscoMacAddressValueObject:
        """
        Converts the raw MAC address to Cisco format (D5B9.EB4D.C2CC).

        Returns:
            CiscoMacAddressValueObject: MAC address in Cisco format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject

        mac = RawMacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_cisco()))
        # >>> CiscoMacAddressValueObject(value=D5B9.EB4D.C2CC)
        ```
        """
        from .cisco_mac_address_value_object import CiscoMacAddressValueObject

        cisco_value = f'{self.value[:4]}.{self.value[4:8]}.{self.value[8:]}'

        return CiscoMacAddressValueObject(value=cisco_value)

    def to_space(self) -> SpaceMacAddressValueObject:
        """
        Converts the raw MAC address to space format (D5 B9 EB 4D C2 CC).

        Returns:
            SpaceMacAddressValueObject: MAC address in space format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import RawMacAddressValueObject

        mac = RawMacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_space()))
        # >>> SpaceMacAddressValueObject(value=D5 B9 EB 4D C2 CC)
        ```
        """
        from .space_mac_address_value_object import SpaceMacAddressValueObject

        space_value = ' '.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return SpaceMacAddressValueObject(value=space_value)

    @classmethod
    def identification_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for identification.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._IDENTIFICATION_REGEX

    @classmethod
    def validation_regex(cls) -> Pattern[str]:
        """
        Returns the regex pattern used for validation.

        Returns:
            Pattern[str]: Regex pattern.
        """
        return cls._VALIDATION_REGEX
