"""
HttpUrlValueObject value object.
"""

from value_object_pattern import validation

from .url_value_object import UrlValueObject, split_url


class HttpUrlValueObject(UrlValueObject):
    """
    HttpUrlValueObject value object.
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