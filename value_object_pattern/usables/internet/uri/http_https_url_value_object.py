"""
HttpHttpsUrlValueObject value object.
"""

from value_object_pattern import validation

from .url_value_object import UrlValueObject, split_url


class HttpHttpsUrlValueObject(UrlValueObject):
    """
    HttpHttpsUrlValueObject value object.
    """

    @validation(order=0)
    def _validate_url_is_http_https(self, value: str) -> None:
        """
        Validate url scheme is HTTP or HTTPS.

        Args:
            value (str): The url value.

        Raises:
            ValueError: If the url scheme is not HTTP or HTTPS.
        """
        scheme, *_ = split_url(value=value)

        if scheme not in ('http', 'https'):
            raise ValueError(f'HttpHttpsUrlValueObject value <<<{value}>>> scheme is not HTTP or HTTPS')
