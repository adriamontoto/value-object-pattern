"""
HttpsUrlValueObject value object.
"""

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
            raise ValueError(f'HttpsUrlValueObject value <<<{value}>>> scheme is not HTTPS')
