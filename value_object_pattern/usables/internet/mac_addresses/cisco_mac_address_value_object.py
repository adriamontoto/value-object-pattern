"""
CiscoMacAddressValueObject value object.
"""

from __future__ import annotations

from re import Pattern, compile as re_compile
from typing import TYPE_CHECKING, NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

if TYPE_CHECKING:
    from .raw_mac_address_value_object import RawMacAddressValueObject
    from .space_mac_address_value_object import SpaceMacAddressValueObject
    from .universal_mac_address_value_object import UniversalMacAddressValueObject
    from .windows_mac_address_value_object import WindowsMacAddressValueObject


class CiscoMacAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CiscoMacAddressValueObject value object ensures the provided value is a valid MAC address in Cisco format
    (D5B9.EB4D.C2CC).

    Example:
    ```python
    from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject

    mac = CiscoMacAddressValueObject(value='D5B9.EB4D.C2CC')
    print(repr(mac))
    # >>> CiscoMacAddressValueObject(value=D5B9.EB4D.C2CC)
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9A-F]{4}\.){2}[0-9A-F]{4}')
    _IDENTIFICATION_REGEX: Pattern[str] = re_compile(pattern=r'([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}')

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
    def _ensure_value_is_cisco_mac_address(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Cisco MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Cisco MAC address.
        """
        if not self._IDENTIFICATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_cisco_mac_address(value=value)

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
            self._raise_value_is_not_cisco_mac_address(value=value)

    def _raise_value_is_not_cisco_mac_address(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Cisco MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Cisco MAC address.
        """
        raise ValueError(f'CiscoMacAddressValueObject value <<<{value}>>> is not a valid Cisco MAC address.')

    def to_raw(self) -> RawMacAddressValueObject:
        """
        Converts the Cisco MAC address to raw format (D5B9EB4DC2CC).

        Returns:
            RawMacAddressValueObject: MAC address in raw format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject

        mac = CiscoMacAddressValueObject(value='D5B9.EB4D.C2CC')
        print(repr(mac.to_raw()))
        # >>> RawMacAddressValueObject(value=D5B9EB4DC2CC)
        ```
        """
        from .raw_mac_address_value_object import RawMacAddressValueObject

        raw_value = self.value.replace('.', '')

        return RawMacAddressValueObject(value=raw_value)

    def to_universal(self) -> UniversalMacAddressValueObject:
        """
        Converts the Cisco MAC address to universal format (D5:B9:EB:4D:C2:CC).

        Returns:
            UniversalMacAddressValueObject: MAC address in universal format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject

        mac = CiscoMacAddressValueObject(value='D5B9.EB4D.C2CC')
        print(repr(mac.to_universal()))
        # >>> UniversalMacAddressValueObject(value=D5:B9:EB:4D:C2:CC)
        ```
        """
        from .universal_mac_address_value_object import UniversalMacAddressValueObject

        raw_value = self.value.replace('.', '')
        universal_value = ':'.join(raw_value[i : i + 2] for i in range(0, len(raw_value), 2))

        return UniversalMacAddressValueObject(value=universal_value)

    def to_windows(self) -> WindowsMacAddressValueObject:
        """
        Converts the Cisco MAC address to Windows format (D5-B9-EB-4D-C2-CC).

        Returns:
            WindowsMacAddressValueObject: MAC address in Windows format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject

        mac = CiscoMacAddressValueObject(value='D5B9.EB4D.C2CC')
        print(repr(mac.to_windows()))
        # >>> WindowsMacAddressValueObject(value=D5-B9-EB-4D-C2-CC)
        ```
        """
        from .windows_mac_address_value_object import WindowsMacAddressValueObject

        raw_value = self.value.replace('.', '')
        windows_value = '-'.join(raw_value[i : i + 2] for i in range(0, len(raw_value), 2))

        return WindowsMacAddressValueObject(value=windows_value)

    def to_space(self) -> SpaceMacAddressValueObject:
        """
        Converts the Cisco MAC address to space format (D5 B9 EB 4D C2 CC).

        Returns:
            SpaceMacAddressValueObject: MAC address in space format.

        Example:
        ```python
        from value_object_pattern.usables.internet.mac_addresses import CiscoMacAddressValueObject

        mac = CiscoMacAddressValueObject(value='D5B9.EB4D.C2CC')
        print(repr(mac.to_space()))
        # >>> SpaceMacAddressValueObject(value=D5 B9 EB 4D C2 CC)
        ```
        """
        from .space_mac_address_value_object import SpaceMacAddressValueObject

        raw_value = self.value.replace('.', '')
        space_value = ' '.join(raw_value[i : i + 2] for i in range(0, len(raw_value), 2))

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
