# ruff: noqa: N802
"""
MacAddressValueObject value object.
"""

from __future__ import annotations

from re import fullmatch

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class MacAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    MacAddressValueObject value object.
    """

    __MAC_ADDRESS_VALUE_OBJECT_RAW_FORMAT_SEPARATOR: str = ''
    __MAC_ADDRESS_VALUE_OBJECT_RAW_REGEX: str = r'^[0-9A-F]{12}$'
    __MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR: str = ':'
    __MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_REGEX: str = r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$'
    __MAC_ADDRESS_VALUE_OBJECT_WINDOWS_FORMAT_SEPARATOR: str = '-'
    __MAC_ADDRESS_VALUE_OBJECT_WINDOWS_REGEX: str = r'^([0-9A-F]{2}-){5}[0-9A-F]{2}$'
    __MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR: str = '.'
    __MAC_ADDRESS_VALUE_OBJECT_CISCO_REGEX: str = r'^([0-9A-F]{4}\.){2}[0-9A-F]{4}$'
    __MAC_ADDRESS_VALUE_OBJECT_SPACE_FORMAT_SEPARATOR: str = ' '
    __MAC_ADDRESS_VALUE_OBJECT_SPACE_REGEX: str = r'^([0-9A-F]{2} ){5}[0-9A-F]{2}$'

    @process(order=0)
    def _ensure_value_is_uppercase(self, value: str) -> str:
        """
        Ensures the value object value is uppercase.

        Args:
            value (str): Value.

        Returns:
            str: Uppercase value.
        """
        return value.upper()

    @process(order=1)
    def _ensure_value_is_normalized(self, value: str) -> str:
        """
        Ensures the value object value is normalized (universally formatted).

        Args:
            value (str): Value.

        Returns:
            str: Value with the normalized format (universally formatted).
        """
        if self.is_raw_format(value=value):
            return ':'.join(value[i : i + 2] for i in range(0, len(value), 2))

        if self.is_windows_format(value=value):
            return value.replace(
                self.__MAC_ADDRESS_VALUE_OBJECT_WINDOWS_FORMAT_SEPARATOR,
                self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            )

        if self.is_cisco_format(value=value):
            raw_mac = value.replace(self.__MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR, '')
            return ':'.join(raw_mac[i : i + 2] for i in range(0, len(raw_mac), 2))

        if self.is_space_format(value=value):
            return value.replace(
                self.__MAC_ADDRESS_VALUE_OBJECT_SPACE_FORMAT_SEPARATOR,
                self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            )

        return value

    @validation(order=0)
    def _ensure_value_is_valid_mac_address(self, value: str) -> None:
        """
        Ensures the value object value is a valid MAC address.

        Args:
            value (str): Value.

        Raises:
            ValueError: If the value is not a valid MAC address.
        """
        if (
            not self.is_raw_format(value=value)
            and not self.is_universal_format(value=value)
            and not self.is_windows_format(value=value)
            and not self.is_cisco_format(value=value)
            and not self.is_space_format(value=value)
        ):
            raise ValueError(f'MacAddressValueObject value <<<{value}>>> is not a valid MAC address.')

    @property
    def raw_format(self) -> str:
        """
        Returns the MAC address in raw format.

        Returns:
            str: MAC address in raw format.
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_RAW_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_raw_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in raw format.

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in raw format.
        """
        if type(value) is not str:
            return False

        return bool(fullmatch(pattern=cls.__MAC_ADDRESS_VALUE_OBJECT_RAW_REGEX, string=value.upper()))

    @property
    def universal_format(self) -> str:
        """
        Returns the MAC address in universal format.

        Returns:
            str: MAC address in universal format.
        """
        return self.value

    @classmethod
    def is_universal_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in universal format.

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in universal format.
        """
        if type(value) is not str:
            return False

        return bool(fullmatch(pattern=cls.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_REGEX, string=value.upper()))

    @property
    def windows_format(self) -> str:
        """
        Returns the MAC address in Windows format.

        Returns:
            str: MAC address in Windows format.
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_WINDOWS_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_windows_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in Windows format.

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in Windows format.
        """
        if type(value) is not str:
            return False

        return bool(fullmatch(pattern=cls.__MAC_ADDRESS_VALUE_OBJECT_WINDOWS_REGEX, string=value.upper()))

    @property
    def cisco_format(self) -> str:
        """
        Returns the MAC address in Cisco format.

        Returns:
            str: MAC address in Cisco format.
        """
        raw_mac = self.raw_format
        return f'{raw_mac[:4]}{self.__MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR}{raw_mac[4:8]}{self.__MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR}{raw_mac[8:]}'  # noqa: E501

    @classmethod
    def is_cisco_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in Cisco format.

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in Cisco format.
        """
        if type(value) is not str:
            return False

        return bool(fullmatch(pattern=cls.__MAC_ADDRESS_VALUE_OBJECT_CISCO_REGEX, string=value.upper()))

    @property
    def space_format(self) -> str:
        """
        Returns the MAC address in space format.

        Returns:
            str: MAC address in space format.
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_SPACE_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_space_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in space format.

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in space format.
        """
        if type(value) is not str:
            return False

        return bool(fullmatch(pattern=cls.__MAC_ADDRESS_VALUE_OBJECT_SPACE_REGEX, string=value.upper()))

    @classmethod
    def NULL(cls) -> MacAddressValueObject:
        """
        Returns the null MAC address.

        Returns:
            MacAddressValueObject: Null MAC address.
        """
        return cls(value='00:00:00:00:00:00')

    @classmethod
    def BROADCAST(cls) -> MacAddressValueObject:
        """
        Returns the broadcast MAC address.

        Returns:
            MacAddressValueObject: Broadcast MAC address.
        """
        return cls(value='FF:FF:FF:FF:FF:FF')
