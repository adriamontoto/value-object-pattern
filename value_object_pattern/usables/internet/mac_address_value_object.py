# ruff: noqa: N802
"""
MacAddressValueObject value object.
"""

from __future__ import annotations

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .mac_addresses import (
    CiscoMacAddressValueObject,
    RawMacAddressValueObject,
    SpaceMacAddressValueObject,
    UniversalMacAddressValueObject,
    WindowsMacAddressValueObject,
)


class MacAddressValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    MacAddressValueObject value object ensures the provided value is a valid MAC address.

    Accepts any MAC address format and stores it as raw format:
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
    # >>> MacAddressValueObject(value=D5B9EB4DC2CC)
    ```
    """

    _MAC_ADDRESS_VARIATIONS: tuple[type[ValueObject[str]], ...] = (
        RawMacAddressValueObject,
        UniversalMacAddressValueObject,
        WindowsMacAddressValueObject,
        CiscoMacAddressValueObject,
        SpaceMacAddressValueObject,
    )

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:  # type: ignore[return]
        """
        Ensures the value object `value` is stored without separators (Raw format).

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        for variation in self._MAC_ADDRESS_VARIATIONS:
            try:
                mac_address = variation(value=value)
                if hasattr(mac_address, 'to_raw'):
                    return mac_address.to_raw().value  # type: ignore[no-any-return]

                return mac_address.value

            except Exception:  # noqa: S112
                continue

    @validation(order=0)
    def _ensure_value_is_mac_address(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid MAC address.
        """
        for variation in self._MAC_ADDRESS_VARIATIONS:
            try:
                variation(value=value)
                return

            except Exception:  # noqa: S112
                continue

        self._raise_value_is_not_mac_address(value=value)

    def _raise_value_is_not_mac_address(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid MAC address.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid MAC address.
        """
        raise ValueError(f'MacAddressValueObject value <<<{value}>>> is not a valid MAC address.')

    def to_raw(self) -> RawMacAddressValueObject:
        """
        Converts the MAC address to raw format (D5B9EB4DC2CC).

        Returns:
            RawMacAddressValueObject: MAC address in raw format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5:B9:EB:4D:C2:CC')
        print(repr(mac.to_raw()))
        # >>> RawMacAddressValueObject(value=D5B9EB4DC2CC)
        ```
        """
        return RawMacAddressValueObject(value=self.value)

    def to_universal(self) -> UniversalMacAddressValueObject:
        """
        Converts the MAC address to universal format (D5:B9:EB:4D:C2:CC).

        Returns:
            UniversalMacAddressValueObject: MAC address in universal format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_universal()))
        # >>> UniversalMacAddressValueObject(value=D5:B9:EB:4D:C2:CC)
        ```
        """
        universal_value = ':'.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return UniversalMacAddressValueObject(value=universal_value)

    def to_windows(self) -> WindowsMacAddressValueObject:
        """
        Converts the MAC address to Windows format (D5-B9-EB-4D-C2-CC).

        Returns:
            WindowsMacAddressValueObject: MAC address in Windows format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_windows()))
        # >>> WindowsMacAddressValueObject(value=D5-B9-EB-4D-C2-CC)
        ```
        """
        windows_value = '-'.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return WindowsMacAddressValueObject(value=windows_value)

    def to_cisco(self) -> CiscoMacAddressValueObject:
        """
        Converts the MAC address to Cisco format (D5B9.EB4D.C2CC).

        Returns:
            CiscoMacAddressValueObject: MAC address in Cisco format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_cisco()))
        # >>> CiscoMacAddressValueObject(value=D5B9.EB4D.C2CC)
        ```
        """
        cisco_value = f'{self.value[:4]}.{self.value[4:8]}.{self.value[8:]}'

        return CiscoMacAddressValueObject(value=cisco_value)

    def to_space(self) -> SpaceMacAddressValueObject:
        """
        Converts the MAC address to space format (D5 B9 EB 4D C2 CC).

        Returns:
            SpaceMacAddressValueObject: MAC address in space format.

        Example:
        ```python
        from value_object_pattern.usables.internet import MacAddressValueObject

        mac = MacAddressValueObject(value='D5B9EB4DC2CC')
        print(repr(mac.to_space()))
        # >>> SpaceMacAddressValueObject(value=D5 B9 EB 4D C2 CC)
        ```
        """
        space_value = ' '.join(self.value[i : i + 2] for i in range(0, len(self.value), 2))

        return SpaceMacAddressValueObject(value=space_value)

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
        # >>> MacAddressValueObject(value=000000000000)
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
        # >>> MacAddressValueObject(value=FFFFFFFFFFFF)
        ```
        """
        return cls(value='FF:FF:FF:FF:FF:FF')
