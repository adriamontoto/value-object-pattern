# ruff: noqa: N802
"""
Provide a value object for supported HTTP request methods.
"""

from __future__ import annotations

from typing import NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class HttpMethodValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and store a supported HTTP request method.

    Values are case-sensitive and must be one of `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`, `POST`, `PUT`,
    `QUERY`, or `TRACE`. The value is stored without normalization. Instances can be created directly with `value` or
    through a named constructor such as `GET()`.

    References:
        IANA HTTP Method Registry: https://www.iana.org/assignments/http-methods/http-methods.xhtml

    Example:
    ```python
    from value_object_pattern.usables.internet import HttpMethodValueObject

    post = HttpMethodValueObject(value='POST')
    print(repr(post))
    # >>> HttpMethodValueObject(value='POST')
    ```
    """

    _HTTP_METHODS: frozenset[str] = frozenset({'CONNECT', 'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PATCH', 'POST', 'PUT', 'QUERY', 'TRACE'})  # noqa: E501  # fmt: skip

    @validation(order=1)
    def _ensure_value_is_http_method(self, value: str) -> None:
        """
        Ensure the value is a supported HTTP request method.

        Args:
            value (str): The HTTP method to validate.

        Raises:
            ValueError: If the value is not a supported HTTP method.
        """
        if value not in self._HTTP_METHODS:
            self._raise_value_is_not_http_method(value=value)

    def _raise_value_is_not_http_method(self, value: str) -> NoReturn:
        """
        Raise an error for an unsupported HTTP method.

        Args:
            value (str): The unsupported HTTP method.

        Raises:
            ValueError: Always raised with the unsupported value.
        """
        raise ValueError(f'HttpMethodValueObject value <<<{value}>>> is not a supported HTTP method.')

    @classmethod
    def CONNECT(cls) -> HttpMethodValueObject:
        """
        Create a value object for the CONNECT HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `CONNECT`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        connect = HttpMethodValueObject.CONNECT()
        print(repr(connect))
        # >>> HttpMethodValueObject(value='CONNECT')
        ```
        """
        return cls(value='CONNECT')

    @classmethod
    def DELETE(cls) -> HttpMethodValueObject:
        """
        Create a value object for the DELETE HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `DELETE`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        delete = HttpMethodValueObject.DELETE()
        print(repr(delete))
        # >>> HttpMethodValueObject(value='DELETE')
        ```
        """
        return cls(value='DELETE')

    @classmethod
    def GET(cls) -> HttpMethodValueObject:
        """
        Create a value object for the GET HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `GET`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        get = HttpMethodValueObject.GET()
        print(repr(get))
        # >>> HttpMethodValueObject(value='GET')
        ```
        """
        return cls(value='GET')

    @classmethod
    def HEAD(cls) -> HttpMethodValueObject:
        """
        Create a value object for the HEAD HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `HEAD`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        head = HttpMethodValueObject.HEAD()
        print(repr(head))
        # >>> HttpMethodValueObject(value='HEAD')
        ```
        """
        return cls(value='HEAD')

    @classmethod
    def OPTIONS(cls) -> HttpMethodValueObject:
        """
        Create a value object for the OPTIONS HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `OPTIONS`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        options = HttpMethodValueObject.OPTIONS()
        print(repr(options))
        # >>> HttpMethodValueObject(value='OPTIONS')
        ```
        """
        return cls(value='OPTIONS')

    @classmethod
    def PATCH(cls) -> HttpMethodValueObject:
        """
        Create a value object for the PATCH HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `PATCH`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        patch = HttpMethodValueObject.PATCH()
        print(repr(patch))
        # >>> HttpMethodValueObject(value='PATCH')
        ```
        """
        return cls(value='PATCH')

    @classmethod
    def POST(cls) -> HttpMethodValueObject:
        """
        Create a value object for the POST HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `POST`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        post = HttpMethodValueObject.POST()
        print(repr(post))
        # >>> HttpMethodValueObject(value='POST')
        ```
        """
        return cls(value='POST')

    @classmethod
    def PUT(cls) -> HttpMethodValueObject:
        """
        Create a value object for the PUT HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `PUT`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        put = HttpMethodValueObject.PUT()
        print(repr(put))
        # >>> HttpMethodValueObject(value='PUT')
        ```
        """
        return cls(value='PUT')

    @classmethod
    def QUERY(cls) -> HttpMethodValueObject:
        """
        Create a value object for the QUERY HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `QUERY`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        query = HttpMethodValueObject.QUERY()
        print(repr(query))
        # >>> HttpMethodValueObject(value='QUERY')
        ```
        """
        return cls(value='QUERY')

    @classmethod
    def TRACE(cls) -> HttpMethodValueObject:
        """
        Create a value object for the TRACE HTTP method.

        Returns:
            HttpMethodValueObject: A value object containing `TRACE`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpMethodValueObject

        trace = HttpMethodValueObject.TRACE()
        print(repr(trace))
        # >>> HttpMethodValueObject(value='TRACE')
        ```
        """
        return cls(value='TRACE')
