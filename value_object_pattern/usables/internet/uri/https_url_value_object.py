"""
HttpsUrlValueObject value object.
"""

from typing import NoReturn

from value_object_pattern import validation

from .url_value_object import UrlValueObject, split_url


class HttpsUrlValueObject(UrlValueObject):
    """
    HttpsUrlValueObject value object ensures the provided value is a valid HTTPS URL.

    Example:
    ```python
    from value_object_pattern.usables.internet import HttpsUrlValueObject

    url = HttpsUrlValueObject(value='https://github.com/adriamontoto/value-object-pattern')

    print(repr(url))
    # >>> HttpsUrlValueObject(value=https://github.com/adriamontoto/value-object-pattern)
    ```
    """

    @validation(order=0)
    def _validate_url_is_https(self, value: str) -> None:
        """
        Validate url scheme is HTTPS.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If the url scheme is not HTTPS.
        """
        scheme, *_ = split_url(value=value)

        if scheme != 'https':
            self._raise_value_is_not_https_url(value=value, scheme=scheme)

    def _raise_value_is_not_https_url(self, value: str, scheme: str) -> NoReturn:
        """
        Raise an error if the URL scheme is not HTTPS.

        Args:
            value (str): The URL value.
            scheme (str): The invalid scheme.

        Raises:
            ValueError: If the URL scheme is not HTTPS.
        """
        raise ValueError(f'HttpsUrlValueObject value <<<{value}>>> scheme is not HTTPS')
