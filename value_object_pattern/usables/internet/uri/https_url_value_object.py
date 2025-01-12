"""
HttpsUrlValueObject value object.
"""

from value_object_pattern import validation

from .url_value_object import UrlValueObject, split_url


class HttpsUrlValueObject(UrlValueObject):
    """
    HttpsUrlValueObject value object.
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
