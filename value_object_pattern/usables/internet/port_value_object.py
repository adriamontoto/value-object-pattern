# ruff: noqa: N802
"""
PortValueObject value object.
"""

from __future__ import annotations

from value_object_pattern.decorators import validation
from value_object_pattern.usables import IntegerValueObject


class PortValueObject(IntegerValueObject):
    """
    PortValueObject value object ensures the provided value is a valid port.

    Example:
    ```python
    from value_object_pattern.usables.internet import PortValueObject

    port = PortValueObject(value=443)

    print(repr(port))
    # >>> PortValueObject(value=443)
    ```
    """

    __PORT_VALUE_OBJECT_MIN_PORT: int = 0
    __PORT_VALUE_OBJECT_MAX_PORT: int = 65535

    @validation(order=0)
    def _ensure_value_is_valid_port(self, value: int) -> None:
        """
        Ensures the value object value is a valid port.

        Args:
            value (int): Value.

        Raises:
            ValueError: If the value is not a valid port.
        """
        if value < self.__PORT_VALUE_OBJECT_MIN_PORT or value > self.__PORT_VALUE_OBJECT_MAX_PORT:
            raise ValueError(f'PortValueObject value <<<{value}>>> must be between {self.__PORT_VALUE_OBJECT_MIN_PORT} and {self.__PORT_VALUE_OBJECT_MAX_PORT}.')  # noqa: E501  # fmt: skip

    @classmethod
    def FTP_DATA(cls) -> PortValueObject:
        """
        Returns FTP data port value object.

        Returns:
            PortValueObject: FTP data port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.FTP_DATA()

        print(repr(port))
        # >>> PortValueObject(value=20)
        ```
        """
        return cls(value=20)

    @classmethod
    def FTP_CONTROL(cls) -> PortValueObject:
        """
        Returns FTP control port value object.

        Returns:
            PortValueObject: FTP control port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.FTP_DATA()

        print(repr(port))
        # >>> PortValueObject(value=21)
        ```
        """
        return cls(value=21)

    @classmethod
    def SSH(cls) -> PortValueObject:
        """
        Returns SSH port value object.

        Returns:
            PortValueObject: SSH port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.SSH()

        print(repr(port))
        # >>> PortValueObject(value=22)
        ```
        """
        return cls(value=22)

    @classmethod
    def TELNET(cls) -> PortValueObject:
        """
        Returns Telnet port value object.

        Returns:
            PortValueObject: Telnet port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.TELNET()

        print(repr(port))
        # >>> PortValueObject(value=23)
        ```
        """
        return cls(value=23)

    @classmethod
    def SMTP(cls) -> PortValueObject:
        """
        Returns SMTP port value object.

        Returns:
            PortValueObject: SMTP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.SMTP()

        print(repr(port))
        # >>> PortValueObject(value=25)
        ```
        """
        return cls(value=25)

    @classmethod
    def DNS(cls) -> PortValueObject:
        """
        Returns DNS port value object.

        Returns:
            PortValueObject: DNS port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.DNS()

        print(repr(port))
        # >>> PortValueObject(value=53)
        ```
        """
        return cls(value=53)

    @classmethod
    def DHCP_SERVER(cls) -> PortValueObject:
        """
        Returns DHCP server port value object.

        Returns:
            PortValueObject: DHCP server port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.DHCP_SERVER()

        print(repr(port))
        # >>> PortValueObject(value=67)
        ```
        """
        return cls(value=67)

    @classmethod
    def DHCP_CLIENT(cls) -> PortValueObject:
        """
        Returns DHCP client port value object.

        Returns:
            PortValueObject: DHCP client port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.DHCP_CLIENT()

        print(repr(port))
        # >>> PortValueObject(value=68)
        ```
        """
        return cls(value=68)

    @classmethod
    def HTTP(cls) -> PortValueObject:
        """
        Returns HTTP port value object.

        Returns:
            PortValueObject: HTTP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.HTTP()

        print(repr(port))
        # >>> PortValueObject(value=80)
        ```
        """
        return cls(value=80)

    @classmethod
    def POP3(cls) -> PortValueObject:
        """
        Returns POP3 port value object.

        Returns:
            PortValueObject: POP3 port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.POP3()

        print(repr(port))
        # >>> PortValueObject(value=110)
        ```
        """
        return cls(value=110)

    @classmethod
    def NTP(cls) -> PortValueObject:
        """
        Returns NTP port value object.

        Returns:
            PortValueObject: NTP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.NTP()

        print(repr(port))
        # >>> PortValueObject(value=123)
        ```
        """
        return cls(value=123)

    @classmethod
    def IMAP(cls) -> PortValueObject:
        """
        Returns IMAP port value object.

        Returns:
            PortValueObject: IMAP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.IMAP()

        print(repr(port))
        # >>> PortValueObject(value=143)
        ```
        """
        return cls(value=143)

    @classmethod
    def SNMP_MONITOR(cls) -> PortValueObject:
        """
        Returns SNMP monitor port value object.

        Returns:
            PortValueObject: SNMP monitor port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.SNMP_MONITOR()

        print(repr(port))
        # >>> PortValueObject(value=161)
        ```
        """
        return cls(value=161)

    @classmethod
    def SNMP_TRAP(cls) -> PortValueObject:
        """
        Returns SNMP trap port value object.

        Returns:
            PortValueObject: SNMP trap port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.SNMP_TRAP()

        print(repr(port))
        # >>> PortValueObject(value=162)
        ```
        """
        return cls(value=162)

    @classmethod
    def LDAP(cls) -> PortValueObject:
        """
        Returns LDAP port value object.

        Returns:
            PortValueObject: LDAP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.LDAP()

        print(repr(port))
        # >>> PortValueObject(value=389)
        ```
        """
        return cls(value=389)

    @classmethod
    def HTTPS(cls) -> PortValueObject:
        """
        Returns HTTPS port value object.

        Returns:
            PortValueObject: HTTPS port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.HTTPS()

        print(repr(port))
        # >>> PortValueObject(value=443)
        ```
        """
        return cls(value=443)

    @classmethod
    def DoH(cls) -> PortValueObject:
        """
        Returns DoH port value object.

        Returns:
            PortValueObject: DoH port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.DoH()

        print(repr(port))
        # >>> PortValueObject(value=443)
        ```
        """
        return cls(value=443)

    @classmethod
    def SMTPS(cls) -> PortValueObject:
        """
        Returns SMTPS port value object.

        Returns:
            PortValueObject: SMTPS port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.SMTPS()

        print(repr(port))
        # >>> PortValueObject(value=465)
        ```
        """
        return cls(value=465)

    @classmethod
    def DoT(cls) -> PortValueObject:
        """
        Returns DoT port value object.

        Returns:
            PortValueObject: DoT port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.DoT()

        print(repr(port))
        # >>> PortValueObject(value=853)
        ```
        """
        return cls(value=853)

    @classmethod
    def IMAPS(cls) -> PortValueObject:
        """
        Returns IMAPS port value object.

        Returns:
            PortValueObject: IMAPS port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.IMAPS()

        print(repr(port))
        # >>> PortValueObject(value=993)
        ```
        """
        return cls(value=993)

    @classmethod
    def POP3S(cls) -> PortValueObject:
        """
        Returns POP3S port value object.

        Returns:
            PortValueObject: POP3S port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.POP3S()

        print(repr(port))
        # >>> PortValueObject(value=995)
        ```
        """
        return cls(value=995)

    @classmethod
    def OPENVPN(cls) -> PortValueObject:
        """
        Returns OpenVPN port value object.

        Returns:
            PortValueObject: OpenVPN port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.OPENVPN()

        print(repr(port))
        # >>> PortValueObject(value=1194)
        ```
        """
        return cls(value=1194)

    @classmethod
    def MICROSOFT_SQL_SERVER(cls) -> PortValueObject:
        """
        Returns Microsoft SQL Server port value object.

        Returns:
            PortValueObject: Microsoft SQL Server port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.MICROSOFT_SQL_SERVER()

        print(repr(port))
        # >>> PortValueObject(value=1433)
        ```
        """
        return cls(value=1433)

    @classmethod
    def ORACLE(cls) -> PortValueObject:
        """
        Returns Oracle port value object.

        Returns:
            PortValueObject: Oracle port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.ORACLE()

        print(repr(port))
        # >>> PortValueObject(value=1521)
        ```
        """
        return cls(value=1521)

    @classmethod
    def MYSQL(cls) -> PortValueObject:
        """
        Returns MySQL port value object.

        Returns:
            PortValueObject: MySQL port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.MYSQL()

        print(repr(port))
        # >>> PortValueObject(value=3306)
        ```
        """
        return cls(value=3306)

    @classmethod
    def MARIADB(cls) -> PortValueObject:
        """
        Returns MariaDB port value object.

        Returns:
            PortValueObject: MariaDB port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.MARIADB()

        print(repr(port))
        # >>> PortValueObject(value=3306)
        ```
        """
        return cls(value=3306)

    @classmethod
    def RDP(cls) -> PortValueObject:
        """
        Returns RDP port value object.

        Returns:
            PortValueObject: RDP port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.RDP()

        print(repr(port))
        # >>> PortValueObject(value=3389)
        ```
        """
        return cls(value=3389)

    @classmethod
    def POSTGRESQL(cls) -> PortValueObject:
        """
        Returns PostgreSQL port value object.

        Returns:
            PortValueObject: PostgreSQL port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.POSTGRESQL()

        print(repr(port))
        # >>> PortValueObject(value=5432)
        ```
        """
        return cls(value=5432)

    @classmethod
    def REDIS(cls) -> PortValueObject:
        """
        Returns Redis port value object.

        Returns:
            PortValueObject: Redis port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.REDIS()

        print(repr(port))
        # >>> PortValueObject(value=6379)
        ```
        """
        return cls(value=6379)

    @classmethod
    def MINECRAFT(cls) -> PortValueObject:
        """
        Returns Minecraft port value object.

        Returns:
            PortValueObject: Minecraft port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.MINECRAFT()

        print(repr(port))
        # >>> PortValueObject(value=25565)
        ```
        """
        return cls(value=25565)

    @classmethod
    def MONGODB(cls) -> PortValueObject:
        """
        Returns MongoDB port value object.

        Returns:
            PortValueObject: MongoDB port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.MONGODB()

        print(repr(port))
        # >>> PortValueObject(value=27017)
        ```
        """
        return cls(value=27017)

    @classmethod
    def WIREGUARD(cls) -> PortValueObject:
        """
        Returns WireGuard port value object.

        Returns:
            PortValueObject: WireGuard port value object.

        Example:
        ```python
        from value_object_pattern.usables.internet import PortValueObject

        port = PortValueObject.WIREGUARD()

        print(repr(port))
        # >>> PortValueObject(value=51820)
        ```
        """
        return cls(value=51820)
