"""
HttpUrlValueObject value object.
"""

from value_object_pattern import validation

from .url_value_object import UrlValueObject, split_url


class HttpUrlValueObject(UrlValueObject):
    """
    HttpUrlValueObject value object ensures the provided value is a valid HTTP URL.

    Example:
    ```python
    from value_object_pattern.usables.internet import HttpUrlValueObject

    url = HttpUrlValueObject(value='http://github.com/adriamontoto/value-object-pattern')

    print(repr(url))
    # >>> HttpUrlValueObject(value=http://github.com/adriamontoto/value-object-pattern)
    ```
    """

    @validation(order=0)
    def _validate_url_is_http(self, value: str) -> None:
        """
        Validate url scheme is HTTP.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If the url scheme is not HTTP.
        """
        scheme, *_ = split_url(value=value)

        if scheme != 'http':
            raise ValueError(f'HttpUrlValueObject value <<<{value}>>> scheme is not HTTP')
