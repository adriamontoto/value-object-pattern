# ruff: noqa: N802
"""
Provide a value object for HTTP media types.
"""

from __future__ import annotations

from re import Pattern, compile as re_compile, sub as re_sub
from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class MediaTypeValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and normalize an HTTP media type.

    Media types contain a type and subtype followed by optional parameters. The type, subtype, and parameter names are
    case-insensitive and are normalized to lowercase. Parameter values retain their original case. Instances can be
    created directly with `value` or through a named constructor such as `JSON()` or `MULTIPART_FORM_DATA()`.

    References:
        RFC 9110 media types: https://www.rfc-editor.org/rfc/rfc9110.html#name-media-type
        IANA Media Types Registry: https://www.iana.org/assignments/media-types/media-types.xhtml

    Example:
    ```python
    from value_object_pattern.usables.internet import MediaTypeValueObject

    media_type = MediaTypeValueObject(value='Application/JSON; Charset="UTF-8"')
    print(repr(media_type))
    # >>> MediaTypeValueObject(value='application/json; charset="UTF-8"')
    ```
    """

    _HTTP_TCHAR_PATTERN = r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+"
    _QUOTED_STRING_PATTERN = r'"(?:[\t !#-\[\]-~\x80-\xff]|\\[\t -~\x80-\xff])*"'
    _MEDIA_TYPE_REGEX: Pattern[str] = re_compile(pattern=rf'^(?P<type>{_HTTP_TCHAR_PATTERN})/(?P<subtype>{_HTTP_TCHAR_PATTERN})(?P<parameters>(?:[ \t]*;[ \t]*{_HTTP_TCHAR_PATTERN}=(?:{_HTTP_TCHAR_PATTERN}|{_QUOTED_STRING_PATTERN}))*)$')  # noqa: E501  # fmt: skip
    _PARAMETER_REGEX: Pattern[str] = re_compile(pattern=rf'[ \t]*;[ \t]*(?P<name>{_HTTP_TCHAR_PATTERN})=(?P<value>{_HTTP_TCHAR_PATTERN}|{_QUOTED_STRING_PATTERN})')  # noqa: E501  # fmt: skip

    @staticmethod
    def _unquote_parameter_value(value: str) -> str:
        """
        Return the semantic value of a token or quoted parameter value.

        Args:
            value (str): The serialized parameter value.

        Returns:
            str: The token value or unquoted and unescaped quoted-string value.
        """
        if not value.startswith('"'):
            return value

        return re_sub(pattern=r'\\([\t -~\x80-\xff])', repl=r'\1', string=value[1:-1])

    @classmethod
    def _parse_media_type(cls, value: str) -> tuple[str, str, tuple[tuple[str, str, str], ...]] | None:
        """
        Parse a media type into normalized components.

        Args:
            value (str): The media type to parse.

        Returns:
            tuple[str, str, tuple[tuple[str, str, str], ...]] | None: Parsed components, or `None` when the value is
            invalid or repeats a parameter.
        """
        media_type_match = cls._MEDIA_TYPE_REGEX.fullmatch(string=value)
        if media_type_match is None:
            return None

        parameters: list[tuple[str, str, str]] = []
        parameter_names: set[str] = set()
        for parameter_match in cls._PARAMETER_REGEX.finditer(media_type_match.group('parameters')):
            parameter_name = parameter_match.group('name').lower()
            if parameter_name in parameter_names:
                return None

            parameter_names.add(parameter_name)
            serialized_value = parameter_match.group('value')
            parameters.append(
                (
                    parameter_name,
                    cls._unquote_parameter_value(value=serialized_value),
                    serialized_value,
                ),
            )

        return media_type_match.group('type').lower(), media_type_match.group('subtype').lower(), tuple(parameters)

    @process(order=0)
    def _normalize_media_type(self, value: str) -> str:
        """
        Normalize case-insensitive media type components.

        Args:
            value (str): The validated media type.

        Returns:
            str: The normalized media type.
        """
        media_type, subtype, parameters = self._parse_media_type(value=value)

        return f'{media_type}/{subtype}{"".join(f"; {name}={serialized_value}" for name, _, serialized_value in parameters)}'  # noqa: E501

    @validation(order=1)
    def _ensure_value_is_media_type(self, value: str) -> None:
        """
        Ensure the value uses the HTTP media-type grammar.

        Args:
            value (str): The media type to validate.

        Raises:
            ValueError: If the value is not a valid media type.
        """
        if self._parse_media_type(value=value) is None:
            self._raise_value_is_not_media_type(value=value)

    def _raise_value_is_not_media_type(self, value: str) -> NoReturn:
        """
        Raise an error for an invalid media type.

        Args:
            value (str): The invalid media type.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'MediaTypeValueObject value <<<{value}>>> is not a valid HTTP media type.')

    @classmethod
    def APPLICATION_OCTET_STREAM(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/octet-stream media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/octet-stream`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        octet_stream = MediaTypeValueObject.APPLICATION_OCTET_STREAM()
        print(repr(octet_stream))
        # >>> MediaTypeValueObject(value='application/octet-stream')
        ```
        """
        return cls(value='application/octet-stream')

    @classmethod
    def APPLICATION_PDF(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/pdf media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/pdf`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        pdf = MediaTypeValueObject.APPLICATION_PDF()
        print(repr(pdf))
        # >>> MediaTypeValueObject(value='application/pdf')
        ```
        """
        return cls(value='application/pdf')

    @classmethod
    def APPLICATION_XML(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/xml media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/xml`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        xml = MediaTypeValueObject.APPLICATION_XML()
        print(repr(xml))
        # >>> MediaTypeValueObject(value='application/xml')
        ```
        """
        return cls(value='application/xml')

    @classmethod
    def APPLICATION_ZIP(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/zip media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/zip`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        zip_archive = MediaTypeValueObject.APPLICATION_ZIP()
        print(repr(zip_archive))
        # >>> MediaTypeValueObject(value='application/zip')
        ```
        """
        return cls(value='application/zip')

    @classmethod
    def AUDIO_MPEG(cls) -> MediaTypeValueObject:
        """
        Create a value object for the audio/mpeg media type.

        Returns:
            MediaTypeValueObject: A value object containing `audio/mpeg`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        audio = MediaTypeValueObject.AUDIO_MPEG()
        print(repr(audio))
        # >>> MediaTypeValueObject(value='audio/mpeg')
        ```
        """
        return cls(value='audio/mpeg')

    @classmethod
    def FORM_URLENCODED(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/x-www-form-urlencoded media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/x-www-form-urlencoded`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        form = MediaTypeValueObject.FORM_URLENCODED()
        print(repr(form))
        # >>> MediaTypeValueObject(value='application/x-www-form-urlencoded')
        ```
        """
        return cls(value='application/x-www-form-urlencoded')

    @classmethod
    def IMAGE_GIF(cls) -> MediaTypeValueObject:
        """
        Create a value object for the image/gif media type.

        Returns:
            MediaTypeValueObject: A value object containing `image/gif`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        gif = MediaTypeValueObject.IMAGE_GIF()
        print(repr(gif))
        # >>> MediaTypeValueObject(value='image/gif')
        ```
        """
        return cls(value='image/gif')

    @classmethod
    def IMAGE_JPEG(cls) -> MediaTypeValueObject:
        """
        Create a value object for the image/jpeg media type.

        Returns:
            MediaTypeValueObject: A value object containing `image/jpeg`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        jpeg = MediaTypeValueObject.IMAGE_JPEG()
        print(repr(jpeg))
        # >>> MediaTypeValueObject(value='image/jpeg')
        ```
        """
        return cls(value='image/jpeg')

    @classmethod
    def IMAGE_PNG(cls) -> MediaTypeValueObject:
        """
        Create a value object for the image/png media type.

        Returns:
            MediaTypeValueObject: A value object containing `image/png`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        png = MediaTypeValueObject.IMAGE_PNG()
        print(repr(png))
        # >>> MediaTypeValueObject(value='image/png')
        ```
        """
        return cls(value='image/png')

    @classmethod
    def IMAGE_SVG_XML(cls) -> MediaTypeValueObject:
        """
        Create a value object for the image/svg+xml media type.

        Returns:
            MediaTypeValueObject: A value object containing `image/svg+xml`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        svg = MediaTypeValueObject.IMAGE_SVG_XML()
        print(repr(svg))
        # >>> MediaTypeValueObject(value='image/svg+xml')
        ```
        """
        return cls(value='image/svg+xml')

    @classmethod
    def MULTIPART_FORM_DATA(cls) -> MediaTypeValueObject:
        """
        Create a value object for the multipart/form-data media type.

        Returns:
            MediaTypeValueObject: A value object containing `multipart/form-data`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        multipart = MediaTypeValueObject.MULTIPART_FORM_DATA()
        print(repr(multipart))
        # >>> MediaTypeValueObject(value='multipart/form-data')
        ```
        """
        return cls(value='multipart/form-data')

    @classmethod
    def JSON(cls) -> MediaTypeValueObject:
        """
        Create a value object for the application/json media type.

        Returns:
            MediaTypeValueObject: A value object containing `application/json`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        json = MediaTypeValueObject.JSON()
        print(repr(json))
        # >>> MediaTypeValueObject(value='application/json')
        ```
        """
        return cls(value='application/json')

    @classmethod
    def TEXT_CSS(cls) -> MediaTypeValueObject:
        """
        Create a value object for the text/css media type.

        Returns:
            MediaTypeValueObject: A value object containing `text/css`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        css = MediaTypeValueObject.TEXT_CSS()
        print(repr(css))
        # >>> MediaTypeValueObject(value='text/css')
        ```
        """
        return cls(value='text/css')

    @classmethod
    def TEXT_HTML(cls) -> MediaTypeValueObject:
        """
        Create a value object for the text/html media type.

        Returns:
            MediaTypeValueObject: A value object containing `text/html`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        text_html = MediaTypeValueObject.TEXT_HTML()
        print(repr(text_html))
        # >>> MediaTypeValueObject(value='text/html')
        ```
        """
        return cls(value='text/html')

    @classmethod
    def TEXT_JAVASCRIPT(cls) -> MediaTypeValueObject:
        """
        Create a value object for the text/javascript media type.

        Returns:
            MediaTypeValueObject: A value object containing `text/javascript`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        javascript = MediaTypeValueObject.TEXT_JAVASCRIPT()
        print(repr(javascript))
        # >>> MediaTypeValueObject(value='text/javascript')
        ```
        """
        return cls(value='text/javascript')

    @classmethod
    def TEXT_PLAIN(cls) -> MediaTypeValueObject:
        """
        Create a value object for the text/plain media type.

        Returns:
            MediaTypeValueObject: A value object containing `text/plain`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        plain_text = MediaTypeValueObject.TEXT_PLAIN()
        print(repr(plain_text))
        # >>> MediaTypeValueObject(value='text/plain')
        ```
        """
        return cls(value='text/plain')

    @classmethod
    def VIDEO_MP4(cls) -> MediaTypeValueObject:
        """
        Create a value object for the video/mp4 media type.

        Returns:
            MediaTypeValueObject: A value object containing `video/mp4`.

        Example:
        ```python
        from value_object_pattern.usables.internet import MediaTypeValueObject

        video = MediaTypeValueObject.VIDEO_MP4()
        print(repr(video))
        # >>> MediaTypeValueObject(value='video/mp4')
        ```
        """
        return cls(value='video/mp4')
