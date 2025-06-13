# ruff: noqa: N802
"""
MacAddressValueObject value object.
"""

from __future__ import annotations

from re import Pattern, compile as re_compile

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class MacAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    MacAddressValueObject value object ensures the provided value is a valid MAC address.

    Formats:
        - Raw: D5B9EB4DC2CC
        - Universal: D5:B9:EB:4D:C2:CC
        - Windows: D5-B9-EB-4D-C2-CC
        - Cisco: D5B9.EB4D.C2CC
        - Space: D5 B9 EB 4D C2 CC

    Example:
    ```python
    from value_object_pattern.usables.internet import MacAddressValueObject

    mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC')

    print(repr(mac))
    # >>> MacAddressValueObject(value=D5:B9:EB:4D:C2:CC)
    ```
    """

    __MAC_ADDRESS_VALUE_OBJECT_RAW_FORMAT_SEPARATOR: str = ''
    __MAC_ADDRESS_VALUE_OBJECT_RAW_REGEX: Pattern[str] = re_compile(pattern=r'^[A-F0-9]{12}$')
    __MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR: str = ':'
    __MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_REGEX: Pattern[str] = re_compile(pattern=r'^([A-F0-9]{2}:){5}[A-F0-9]{2}$')
    __MAC_ADDRESS_VALUE_OBJECT_WINDOWS_FORMAT_SEPARATOR: str = '-'
    __MAC_ADDRESS_VALUE_OBJECT_WINDOWS_REGEX: Pattern[str] = re_compile(pattern=r'^([A-F0-9]{2}-){5}[A-F0-9]{2}$')
    __MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR: str = '.'
    __MAC_ADDRESS_VALUE_OBJECT_CISCO_REGEX: Pattern[str] = re_compile(pattern=r'^([A-F0-9]{4}\.){2}[0-9A-F]{4}$')
    __MAC_ADDRESS_VALUE_OBJECT_SPACE_FORMAT_SEPARATOR: str = ' '
    __MAC_ADDRESS_VALUE_OBJECT_SPACE_REGEX: Pattern[str] = re_compile(pattern=r'^([A-F0-9]{2} ){5}[A-F0-9]{2}$')

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
        Returns the MAC address in raw format (D5B9EB4DC2CC).

        Returns:
            str: MAC address in raw format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC').raw_format

        print(mac)
        # >>> D5B9EB4DC2CC
        ```
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_RAW_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_raw_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in raw format (D5B9EB4DC2CC).

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in raw format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        is_raw = MacAddressValueObject.is_raw_format(value='D5B9EB4DC2CC')

        print(is_raw)
        # >>> True
        ```
        """
        if type(value) is not str:
            return False

        return bool(cls.__MAC_ADDRESS_VALUE_OBJECT_RAW_REGEX.fullmatch(string=value.upper()))

    @property
    def universal_format(self) -> str:
        """
        Returns the MAC address in universal format (D5:B9:EB:4D:C2:CC).

        Returns:
            str: MAC address in universal format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC').universal_format

        print(mac)
        # >>> D5:B9:EB:4D:C2:CC
        ```
        """
        return self.value

    @classmethod
    def is_universal_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in universal format (D5:B9:EB:4D:C2:CC).

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in universal format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        is_universal = MacAddressValueObject.is_universal_format(value='D5:B9:EB:4D:C2:CC')

        print(is_universal)
        # >>> True
        ```
        """
        if type(value) is not str:
            return False

        return bool(cls.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_REGEX.fullmatch(string=value.upper()))

    @property
    def windows_format(self) -> str:
        """
        Returns the MAC address in Windows format (D5-B9-EB-4D-C2-CC).

        Returns:
            str: MAC address in Windows format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC').windows_format

        print(mac)
        # >>> D5-B9-EB-4D-C2-CC
        ```
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_WINDOWS_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_windows_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in Windows format (D5-B9-EB-4D-C2-CC).

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in Windows format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        is_windows = MacAddressValueObject.is_windows_format(value='D5-B9-EB-4D-C2-CC')

        print(is_windows)
        # >>> True
        ```
        """
        if type(value) is not str:
            return False

        return bool(cls.__MAC_ADDRESS_VALUE_OBJECT_WINDOWS_REGEX.fullmatch(string=value.upper()))

    @property
    def cisco_format(self) -> str:
        """
        Returns the MAC address in Cisco format (D5B9.EB4D.C2CC).

        Returns:
            str: MAC address in Cisco format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC').cisco_format

        print(mac)
        # >>> D5B9.EB4D.C2CC
        ```
        """
        raw_mac = self.raw_format
        return f'{raw_mac[:4]}{self.__MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR}{raw_mac[4:8]}{self.__MAC_ADDRESS_VALUE_OBJECT_CISCO_FORMAT_SEPARATOR}{raw_mac[8:]}'  # noqa: E501

    @classmethod
    def is_cisco_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in Cisco format (D5B9.EB4D.C2CC).

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in Cisco format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        is_cisco = MacAddressValueObject.is_cisco_format(value='D5B9.EB4D.C2CC')

        print(is_cisco)
        # >>> True
        ```
        """
        if type(value) is not str:
            return False

        return bool(cls.__MAC_ADDRESS_VALUE_OBJECT_CISCO_REGEX.fullmatch(string=value.upper()))

    @property
    def space_format(self) -> str:
        """
        Returns the MAC address in space format (D5 B9 EB 4D C2 CC).

        Returns:
            str: MAC address in space format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC').space_format

        print(mac)
        # >>> D5 B9 EB 4D C2 CC
        ```
        """
        return self.value.replace(
            self.__MAC_ADDRESS_VALUE_OBJECT_UNIVERSAL_SEPARATOR,
            self.__MAC_ADDRESS_VALUE_OBJECT_SPACE_FORMAT_SEPARATOR,
        )

    @classmethod
    def is_space_format(cls, *, value: str) -> bool:
        """
        Returns whether the value is a MAC address in space format (D5 B9 EB 4D C2 CC).

        Args:
            value (str): Value.

        Returns:
            bool: Whether the value is a MAC address in space format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        is_space = MacAddressValueObject.is_space_format(value='D5 B9 EB 4D C2 CC')

        print(is_space)
        # >>> True
        ```
        """
        if type(value) is not str:
            return False

        return bool(cls.__MAC_ADDRESS_VALUE_OBJECT_SPACE_REGEX.fullmatch(string=value.upper()))

    @classmethod
    def NULL(cls) -> MacAddressValueObject:
        """
        Returns the null MAC address.

        Returns:
            MacAddressValueObject: Null MAC address.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject.NULL()

        print(repr(mac))
        # >>> MacAddressValueObject(value=00:00:00:00:00:00')
        ```
        """
        return cls(value='00:00:00:00:00:00')

    @classmethod
    def BROADCAST(cls) -> MacAddressValueObject:
        """
        Returns the broadcast MAC address.

        Returns:
            MacAddressValueObject: Broadcast MAC address.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject.BROADCAST()

        print(repr(mac))
        # >>> MacAddressValueObject(value=FF:FF:FF:FF:FF:FF')
        ```
        """
        return cls(value='FF:FF:FF:FF:FF:FF')
