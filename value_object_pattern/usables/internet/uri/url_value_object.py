"""
UrlValueObject value object.
"""

from functools import lru_cache
from re import Pattern, compile as re_compile
from urllib.parse import parse_qs, urlsplit

from value_object_pattern import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject
from value_object_pattern.usables.internet.host_value_object import HostValueObject
from value_object_pattern.usables.internet.port_value_object import PortValueObject


@lru_cache(maxsize=16)
def join_url(
    scheme: str,
    host: str,
    port: int | None = None,
    user_information: str | None = None,
    path: str | None = None,
    query: str | None = None,
    fragment: str | None = None,
) -> str:
    """
    Join the URL parts.

    Args:
        scheme (str): The URL scheme.
        host (str): The URL host.
        port (int | None, optional): The URL port. Defaults to None.
        user_information (str | None, optional): The URL user information. Defaults to None.
        path (str | None, optional): The URL path. Defaults to None.
        query (str | None, optional): The URL query. Defaults to None.
        fragment (str | None, optional): The URL fragment. Defaults to None.

    Returns:
        str: The URL joined.
    """
    netloc = host
    if user_information:
        netloc = f'{user_information}@{netloc}'

    if port is not None:
        netloc = f'{netloc}:{port}'

    if path and not path.startswith('/'):
        path = f'/{path}'

    if query:
        query = f'?{query}'

    if fragment:
        fragment = f'#{fragment}'

    return f'{scheme}://{netloc}{path}{query}{fragment}'


@lru_cache(maxsize=16)
def split_url(value: str) -> tuple[str, str, str, str, str]:
    """
    Split the URL in scheme, netloc, path, query and fragment.

    Args:
        value (str): The URL value.

    Returns:
        tuple[str, str, str, str, str]: The URL splitted in scheme, netloc, path, query and fragment.
    """
    return urlsplit(url=value)


@lru_cache(maxsize=16)
def split_netloc(value: str) -> tuple[str | None, str, int | None]:
    """
    Split the netloc in user_information, host and port.

    Args:
        value (str): The netloc value.

    Returns:
        tuple[str | None, str, int | None]: The netloc splitted in user_information, host and port.
    """
    user_information, port = None, None

    host_port = value
    if '@' in value:
        # prevent splitting passwords with @
        user_information, host_port = value.rsplit(sep='@', maxsplit=1)

    host = host_port
    if ':' in host_port and host_port.count(':') == 1:
        # prevent splitting IPv6 addresses
        host, port_string = host_port.rsplit(sep=':', maxsplit=1)
        port = int(port_string)

    return user_information, host, port


class UrlValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    UrlValueObject value object ensures the provided value is a valid URL.

    References:
        https://www.rfc-editor.org/rfc/rfc3986

    Example:
    ```python
    from value_object_pattern.usables.internet import UrlValueObject

    url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

    print(repr(url))
    # >>> UrlValueObject(value=https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents)
    ```
    """

    __URL_VALUE_OBJECT_SCHEME_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z][a-zA-Z0-9\+\-\.]+$')
    __URL_VALUE_OBJECT_USER_INFORMATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z0-9\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]+$')  # noqa: E501  # fmt: skip
    __URL_VALUE_OBJECT_PATH_REGEX: Pattern[str] = re_compile(pattern=r'^\/(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip
    __URL_VALUE_OBJECT_QUERY_REGEX: Pattern[str] = re_compile(pattern=r'^(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip
    __URL_VALUE_OBJECT_FRAGMENT_REGEX: Pattern[str] = re_compile(pattern=r'^(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip

    @process(order=0)
    def _ensure_url_is_lower(self, value: str) -> str:
        """
        Ensure scheme and domain are in lower case.

        Args:
            value (str): The url value.

        Returns:
            str: The url value with scheme and domain in lower case.
        """
        scheme, netloc, path, query, fragment = split_url(value=value)
        user_information, host, port = split_netloc(value=netloc)

        return join_url(
            scheme=scheme.lower(),
            user_information=user_information,
            host=host.lower(),
            port=port,
            path=path,
            query=query,
            fragment=fragment,
        )

    @validation(order=0)
    def _validate_url(self, value: str) -> None:
        """
        Validate url.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If value is not a valid url.

        References:
            https://www.rfc-editor.org/rfc/rfc3986
        """
        try:
            scheme, netloc, path, query, fragment = split_url(value=value)

        except ValueError as error:
            raise ValueError(f'UrlValueObject value <<<{value}>>> is not a valid url.') from error

        if not scheme and not netloc and not path and not query and not fragment:
            raise ValueError(f'UrlValueObject value <<<{value}>>> is not a valid url.')

    @validation(order=1)
    def _validate_url_scheme(self, value: str) -> None:
        """
        Validate url scheme.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If the url value has not a valid scheme.

        References:
            https://www.rfc-editor.org/rfc/rfc3986#section-3.1
        """
        scheme, *_ = split_url(value=value)
        if not self.__URL_VALUE_OBJECT_SCHEME_REGEX.match(string=scheme):
            raise ValueError(f'UrlValueObject value <<<{value}>>> contains an invalid scheme <<<{scheme}>>>.')

    @validation(order=2)
    def _validate_url_netloc(self, value: str) -> None:
        """
        Validate url netloc.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If url value has not a valid netloc.

        References:
            https://www.rfc-editor.org/rfc/rfc3986#section-3.2.1
            https://www.rfc-editor.org/rfc/rfc3986#section-3.2.2
            https://www.rfc-editor.org/rfc/rfc3986#section-3.2.3
        """
        _, netloc, *_ = split_url(value=value)
        user_information, host, port = split_netloc(value=netloc)

        if user_information is not None and not self.__URL_VALUE_OBJECT_USER_INFORMATION_REGEX.match(string=user_information):  # noqa: E501  # fmt: skip
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid user information <<<{user_information}>>>.')  # noqa: E501  # fmt: skip

        try:
            HostValueObject(value=host)

        except ValueError as error:
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid host <<<{host}>>>.') from error

        try:
            if port is not None:
                PortValueObject(value=port)

        except ValueError as error:
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid port <<<{port}>>>.') from error

    @validation(order=3)
    def _validate_url_path(self, value: str) -> None:
        """
        Validate url path.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If url value has not a valid path.

        References:
            https://www.rfc-editor.org/rfc/rfc3986#section-3.3
        """
        _, _, path, *_ = split_url(value=value)
        if not path:
            return

        if not self.__URL_VALUE_OBJECT_PATH_REGEX.match(string=path):
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid path <<<{path}>>>.')

    @validation(order=4)
    def _validate_url_query(self, value: str) -> None:
        """
        Validate url query.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If url value has not a valid query.

        References:
            https://www.rfc-editor.org/rfc/rfc3986#section-3.4
        """
        _, _, _, query, *_ = split_url(value=value)
        if not query:
            return

        try:
            parse_qs(qs=query)

        except ValueError as error:
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid query <<<{query}>>>.') from error

        if not self.__URL_VALUE_OBJECT_QUERY_REGEX.match(string=query):
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid query <<<{query}>>>.')

    @validation(order=5)
    def _validate_url_fragment(self, value: str) -> None:
        """
        Validate url fragment.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If url value has not a valid fragment.

        References:
            https://www.rfc-editor.org/rfc/rfc3986#section-3.5
        """
        _, _, _, _, fragment = split_url(value=value)
        if not fragment:
            return

        if not self.__URL_VALUE_OBJECT_FRAGMENT_REGEX.match(string=fragment):
            raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid fragment <<<{fragment}>>>.')

    @property
    def scheme(self) -> str:
        """
        Get the URL scheme.

        Returns:
            str: The URL scheme.

        Example:
        ```python
        from value_object_pattern.usables.internet import UrlValueObject

        url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

        print(url.scheme)
        # >>> https
        ```
        """
        scheme, *_ = split_url(value=self.value)
        return scheme

    @property
    def netloc(self) -> str:
        """
        Get the URL netloc.

        Returns:
            str: The URL netloc.

        Example:
        ```python
        from value_object_pattern.usables.internet import UrlValueObject

        url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

        print(url.netloc)
        # >>> github.com
        ```
        """
        _, netloc, *_ = split_url(value=self.value)
        return netloc

    @property
    def path(self) -> str | None:
        """
        Get the URL path.

        Returns:
            str | None: The URL path if exists, otherwise None.

        Example:
        ```python
        from value_object_pattern.usables.internet import UrlValueObject

        url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

        print(url.path)
        # >>> /adriamontoto/value-object-pattern
        ```
        """
        _, _, path, *_ = split_url(value=self.value)
        return path if path else None

    @property
    def query(self) -> str | None:
        """
        Get the URL query.

        Returns:
            str | None: The URL query if exists, otherwise None.

        Example:
        ```python
        from value_object_pattern.usables.internet import UrlValueObject

        url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

        print(url.query)
        # >>> tab=readme-ov-file
        ```
        """
        _, _, _, query, *_ = split_url(value=self.value)
        return query if query else None

    @property
    def fragment(self) -> str | None:
        """
        Get the URL fragment.

        Returns:
            str | None: The URL fragment if exists, otherwise None.

        Example:
        ```python
        from value_object_pattern.usables.internet import UrlValueObject

        url = UrlValueObject(value='https://github.com/adriamontoto/value-object-pattern?tab=readme-ov-file#table-of-contents')

        print(url.fragment)
        # >>> table-of-contents
        ```
        """
        _, _, _, _, fragment = split_url(value=self.value)
        return fragment if fragment else None
