"""
UrlValueObject value object.
"""

from functools import lru_cache
from re import Pattern, compile as re_compile
from typing import NoReturn
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
    if ':' in host and not host.startswith('['):
        host = f'[{host}]'

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

    if host_port.startswith('['):
        host, _, port_string = host_port[1:].partition(']')
        if port_string:
            port = int(port_string.removeprefix(':'))

        return user_information, host, port

    if host_port.count(':') > 1:
        raise ValueError('IPv6 URL hosts must be enclosed in brackets.')

    host = host_port
    if ':' in host_port:
        host, port_string = host_port.rsplit(sep=':', maxsplit=1)
        port = int(port_string)

    return user_information, host, port


class UrlValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Ensure the provided value is a syntactically valid URL.

    The validator checks URL shape, host, optional user information, optional port, path, query, and fragment.
    Processing lowercases the scheme and host while preserving the rest of the URL. This class validates syntax; it does
    not verify ownership, reachability, or safety of the target URL.

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

    _URL_SCHEME_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z][a-zA-Z0-9\+\-\.]+$')
    _URL_USER_INFORMATION_REGEX: Pattern[str] = re_compile(pattern=r'^[a-zA-Z0-9\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]+$')  # noqa: E501  # fmt: skip
    _URL_PATH_REGEX: Pattern[str] = re_compile(pattern=r'^\/(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip
    _URL_QUERY_REGEX: Pattern[str] = re_compile(pattern=r'^(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip
    _URL_FRAGMENT_REGEX: Pattern[str] = re_compile(pattern=r'^(?:[a-zA-Z0-9\/\-\.\_\~\!\$\&\'\(\)\*\+\,\;\=\:\@]|%[a-fA-F0-9]{2})*$')  # noqa: E501  # fmt: skip

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

        except ValueError:
            self._raise_value_is_not_valid_url(value=value)

        if not scheme and not netloc and not path and not query and not fragment:
            self._raise_value_is_not_valid_url(value=value)

    def _raise_value_is_not_valid_url(self, value: str) -> NoReturn:
        """
        Raise an error if the value is not a valid URL.

        Args:
            value (str): The invalid URL value.

        Raises:
            ValueError: If the value is not a valid URL.
        """
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
        if not self._URL_SCHEME_REGEX.match(string=scheme):
            self._raise_value_has_not_valid_scheme(value=value, scheme=scheme)

    def _raise_value_has_not_valid_scheme(self, value: str, scheme: str) -> NoReturn:
        """
        Raise an error if the URL scheme is invalid.

        Args:
            value (str): The URL value.
            scheme (str): The invalid scheme.

        Raises:
            ValueError: If the URL scheme is invalid.
        """
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
        try:
            user_information, host, port = split_netloc(value=netloc)

        except ValueError:
            if netloc.count(':') > 1 and not netloc.startswith('['):
                self._raise_value_is_not_valid_url(value=value)

            invalid_port = netloc.rsplit(sep=':', maxsplit=1)[-1]
            self._raise_value_has_not_valid_port(value=value, port=invalid_port)

        if user_information is not None and not self._URL_USER_INFORMATION_REGEX.match(string=user_information):  # noqa: E501  # fmt: skip
            self._raise_value_has_not_valid_user_information(value=value, user_information=user_information)

        try:
            HostValueObject(value=host)

        except (TypeError, ValueError):
            self._raise_value_has_not_valid_host(value=value, host=host)

        if port is not None:
            try:
                PortValueObject(value=port)

            except (TypeError, ValueError):
                self._raise_value_has_not_valid_port(value=value, port=port)

    def _raise_value_has_not_valid_user_information(self, value: str, user_information: str) -> NoReturn:
        """
        Raise an error if the URL user information is invalid.

        Args:
            value (str): The URL value.
            user_information (str): The invalid user information.

        Raises:
            ValueError: If the URL user information is invalid.
        """
        raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid user information <<<{user_information}>>>.')  # noqa: E501  # fmt: skip

    def _raise_value_has_not_valid_host(self, value: str, host: str) -> NoReturn:
        """
        Raise an error if the URL host is invalid.

        Args:
            value (str): The URL value.
            host (str): The invalid host.

        Raises:
            ValueError: If the URL host is invalid.
        """
        raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid host <<<{host}>>>.')

    def _raise_value_has_not_valid_port(self, value: str, port: int | str) -> NoReturn:
        """
        Raise an error if the URL port is invalid.

        Args:
            value (str): The URL value.
            port (int | str): The invalid port.

        Raises:
            ValueError: If the URL port is invalid.
        """
        raise ValueError(f'UrlValueObject value <<<{value}>>> has not a valid port <<<{port}>>>.')

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

        if not self._URL_PATH_REGEX.match(string=path):
            self._raise_value_has_not_valid_path(value=value, path=path)

    def _raise_value_has_not_valid_path(self, value: str, path: str) -> NoReturn:
        """
        Raise an error if the URL path is invalid.

        Args:
            value (str): The URL value.
            path (str): The invalid path.

        Raises:
            ValueError: If the URL path is invalid.
        """
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

        except ValueError:
            self._raise_value_has_not_valid_query(value=value, query=query)

        if not self._URL_QUERY_REGEX.match(string=query):
            self._raise_value_has_not_valid_query(value=value, query=query)

    def _raise_value_has_not_valid_query(self, value: str, query: str) -> NoReturn:
        """
        Raise an error if the URL query is invalid.

        Args:
            value (str): The URL value.
            query (str): The invalid query.

        Raises:
            ValueError: If the URL query is invalid.
        """
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

        if not self._URL_FRAGMENT_REGEX.match(string=fragment):
            self._raise_value_has_not_valid_fragment(value=value, fragment=fragment)

    def _raise_value_has_not_valid_fragment(self, value: str, fragment: str) -> NoReturn:
        """
        Raise an error if the URL fragment is invalid.

        Args:
            value (str): The URL value.
            fragment (str): The invalid fragment.

        Raises:
            ValueError: If the URL fragment is invalid.
        """
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
