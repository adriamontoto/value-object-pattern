# ruff: noqa: N802
"""
Provide a value object for HTTP response status codes.
"""

from __future__ import annotations

from typing import ClassVar, NoReturn

from value_object_pattern.decorators import validation
from value_object_pattern.usables import IntegerValueObject


class HttpStatusCodeValueObject(IntegerValueObject):
    """
    Validate and store an HTTP response status code.

    Valid values are integers from `100` through `599`, including unassigned codes reserved for future extensions within
    the five HTTP response classes. Instances can be created directly with `value` or through a named constructor for
    known codes, such as `OK()` or `NOT_FOUND()`. The `reason_phrase` property exposes known IANA or legacy text and
    returns `None` for unassigned codes.

    References:
        RFC 9110, Status Codes: https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes
        IANA HTTP Status Code Registry: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

    Example:
    ```python
    from value_object_pattern.usables.internet import HttpStatusCodeValueObject

    ok = HttpStatusCodeValueObject.OK()
    print(repr(ok))
    # >>> HttpStatusCodeValueObject(value=200)
    print(ok.reason_phrase)
    # >>> OK
    ```
    """

    _MIN_STATUS_CODE: int = 100
    _MAX_STATUS_CODE: int = 599
    _REASON_PHRASES: ClassVar[dict[int, str]] = {
        100: 'Continue',
        101: 'Switching Protocols',
        102: 'Processing',
        103: 'Early Hints',
        104: 'Upload Resumption Supported',
        200: 'OK',
        201: 'Created',
        202: 'Accepted',
        203: 'Non-Authoritative Information',
        204: 'No Content',
        205: 'Reset Content',
        206: 'Partial Content',
        207: 'Multi-Status',
        208: 'Already Reported',
        226: 'IM Used',
        300: 'Multiple Choices',
        301: 'Moved Permanently',
        302: 'Found',
        303: 'See Other',
        304: 'Not Modified',
        305: 'Use Proxy',
        306: 'Unused',
        307: 'Temporary Redirect',
        308: 'Permanent Redirect',
        400: 'Bad Request',
        401: 'Unauthorized',
        402: 'Payment Required',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        406: 'Not Acceptable',
        407: 'Proxy Authentication Required',
        408: 'Request Timeout',
        409: 'Conflict',
        410: 'Gone',
        411: 'Length Required',
        412: 'Precondition Failed',
        413: 'Content Too Large',
        414: 'URI Too Long',
        415: 'Unsupported Media Type',
        416: 'Range Not Satisfiable',
        417: 'Expectation Failed',
        418: "I'm a Teapot",
        421: 'Misdirected Request',
        422: 'Unprocessable Content',
        423: 'Locked',
        424: 'Failed Dependency',
        425: 'Too Early',
        426: 'Upgrade Required',
        428: 'Precondition Required',
        429: 'Too Many Requests',
        431: 'Request Header Fields Too Large',
        451: 'Unavailable For Legal Reasons',
        500: 'Internal Server Error',
        501: 'Not Implemented',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
        504: 'Gateway Timeout',
        505: 'HTTP Version Not Supported',
        506: 'Variant Also Negotiates',
        507: 'Insufficient Storage',
        508: 'Loop Detected',
        510: 'Not Extended',
        511: 'Network Authentication Required',
    }

    @validation(order=1)
    def _ensure_value_is_http_status_code(self, value: int) -> None:
        """
        Ensure the value is within the valid HTTP status-code range.

        Args:
            value (int): The HTTP status code to validate.

        Raises:
            ValueError: If the value is outside the HTTP status-code range.
        """
        if value < self._MIN_STATUS_CODE or value > self._MAX_STATUS_CODE:
            self._raise_value_is_not_http_status_code(value=value)

    def _raise_value_is_not_http_status_code(self, value: int) -> NoReturn:
        """
        Raise an error for a value outside the HTTP status-code range.

        Args:
            value (int): The out-of-range HTTP status code.

        Raises:
            ValueError: Always raised with the invalid value and valid range.
        """
        raise ValueError(f'HttpStatusCodeValueObject value <<<{value}>>> must be between {self._MIN_STATUS_CODE} and {self._MAX_STATUS_CODE}.')  # noqa: E501  # fmt: skip

    @property
    def reason_phrase(self) -> str | None:
        """
        Return the known reason phrase for the status code.

        Returns:
            str | None: The IANA or legacy reason phrase, or `None` when the status code is unassigned.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        print(HttpStatusCodeValueObject.NOT_FOUND().reason_phrase)
        # >>> Not Found
        ```
        """
        return self._REASON_PHRASES.get(self.value)

    @classmethod
    def CONTINUE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 100 Continue HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `100`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        continue = HttpStatusCodeValueObject.CONTINUE()
        print(repr(continue))
        # >>> HttpStatusCodeValueObject(value=100)
        ```
        """
        return cls(value=100)

    @classmethod
    def SWITCHING_PROTOCOLS(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 101 Switching Protocols HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `101`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        switching_protocols = HttpStatusCodeValueObject.SWITCHING_PROTOCOLS()
        print(repr(switching_protocols))
        # >>> HttpStatusCodeValueObject(value=101)
        ```
        """
        return cls(value=101)

    @classmethod
    def PROCESSING(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 102 Processing HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `102`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        processing = HttpStatusCodeValueObject.PROCESSING()
        print(repr(processing))
        # >>> HttpStatusCodeValueObject(value=102)
        ```
        """
        return cls(value=102)

    @classmethod
    def EARLY_HINTS(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 103 Early Hints HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `103`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        early_hints = HttpStatusCodeValueObject.EARLY_HINTS()
        print(repr(early_hints))
        # >>> HttpStatusCodeValueObject(value=103)
        ```
        """
        return cls(value=103)

    @classmethod
    def UPLOAD_RESUMPTION_SUPPORTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the temporary 104 Upload Resumption Supported HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `104`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        upload_resumption_supported = HttpStatusCodeValueObject.UPLOAD_RESUMPTION_SUPPORTED()
        print(repr(upload_resumption_supported))
        # >>> HttpStatusCodeValueObject(value=104)
        ```
        """
        return cls(value=104)

    @classmethod
    def OK(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 200 OK HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `200`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        ok = HttpStatusCodeValueObject.OK()
        print(repr(ok))
        # >>> HttpStatusCodeValueObject(value=200)
        ```
        """
        return cls(value=200)

    @classmethod
    def CREATED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 201 Created HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `201`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        created = HttpStatusCodeValueObject.CREATED()
        print(repr(created))
        # >>> HttpStatusCodeValueObject(value=201)
        ```
        """
        return cls(value=201)

    @classmethod
    def ACCEPTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 202 Accepted HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `202`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        accepted = HttpStatusCodeValueObject.ACCEPTED()
        print(repr(accepted))
        # >>> HttpStatusCodeValueObject(value=202)
        ```
        """
        return cls(value=202)

    @classmethod
    def NON_AUTHORITATIVE_INFORMATION(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 203 Non-Authoritative Information HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `203`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        non_authoritative_information = HttpStatusCodeValueObject.NON_AUTHORITATIVE_INFORMATION()
        print(repr(non_authoritative_information))
        # >>> HttpStatusCodeValueObject(value=203)
        ```
        """
        return cls(value=203)

    @classmethod
    def NO_CONTENT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 204 No Content HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `204`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        no_content = HttpStatusCodeValueObject.NO_CONTENT()
        print(repr(no_content))
        # >>> HttpStatusCodeValueObject(value=204)
        ```
        """
        return cls(value=204)

    @classmethod
    def RESET_CONTENT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 205 Reset Content HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `205`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        reset_content = HttpStatusCodeValueObject.RESET_CONTENT()
        print(repr(reset_content))
        # >>> HttpStatusCodeValueObject(value=205)
        ```
        """
        return cls(value=205)

    @classmethod
    def PARTIAL_CONTENT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 206 Partial Content HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `206`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        partial_content = HttpStatusCodeValueObject.PARTIAL_CONTENT()
        print(repr(partial_content))
        # >>> HttpStatusCodeValueObject(value=206)
        ```
        """
        return cls(value=206)

    @classmethod
    def MULTI_STATUS(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 207 Multi-Status HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `207`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        multi_status = HttpStatusCodeValueObject.MULTI_STATUS()
        print(repr(multi_status))
        # >>> HttpStatusCodeValueObject(value=207)
        ```
        """
        return cls(value=207)

    @classmethod
    def ALREADY_REPORTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 208 Already Reported HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `208`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        already_reported = HttpStatusCodeValueObject.ALREADY_REPORTED()
        print(repr(already_reported))
        # >>> HttpStatusCodeValueObject(value=208)
        ```
        """
        return cls(value=208)

    @classmethod
    def IM_USED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 226 IM Used HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `226`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        im_used = HttpStatusCodeValueObject.IM_USED()
        print(repr(im_used))
        # >>> HttpStatusCodeValueObject(value=226)
        ```
        """
        return cls(value=226)

    @classmethod
    def MULTIPLE_CHOICES(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 300 Multiple Choices HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `300`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        multiple_choices = HttpStatusCodeValueObject.MULTIPLE_CHOICES()
        print(repr(multiple_choices))
        # >>> HttpStatusCodeValueObject(value=300)
        ```
        """
        return cls(value=300)

    @classmethod
    def MOVED_PERMANENTLY(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 301 Moved Permanently HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `301`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        moved_permanently = HttpStatusCodeValueObject.MOVED_PERMANENTLY()
        print(repr(moved_permanently))
        # >>> HttpStatusCodeValueObject(value=301)
        ```
        """
        return cls(value=301)

    @classmethod
    def FOUND(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 302 Found HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `302`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        found = HttpStatusCodeValueObject.FOUND()
        print(repr(found))
        # >>> HttpStatusCodeValueObject(value=302)
        ```
        """
        return cls(value=302)

    @classmethod
    def SEE_OTHER(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 303 See Other HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `303`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        see_other = HttpStatusCodeValueObject.SEE_OTHER()
        print(repr(see_other))
        # >>> HttpStatusCodeValueObject(value=303)
        ```
        """
        return cls(value=303)

    @classmethod
    def NOT_MODIFIED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 304 Not Modified HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `304`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        not_modified = HttpStatusCodeValueObject.NOT_MODIFIED()
        print(repr(not_modified))
        # >>> HttpStatusCodeValueObject(value=304)
        ```
        """
        return cls(value=304)

    @classmethod
    def USE_PROXY(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 305 Use Proxy HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `305`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        use_proxy = HttpStatusCodeValueObject.USE_PROXY()
        print(repr(use_proxy))
        # >>> HttpStatusCodeValueObject(value=305)
        ```
        """
        return cls(value=305)

    @classmethod
    def UNUSED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the unused 306 HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `306`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        unused = HttpStatusCodeValueObject.UNUSED()
        print(repr(unused))
        # >>> HttpStatusCodeValueObject(value=306)
        ```
        """
        return cls(value=306)

    @classmethod
    def TEMPORARY_REDIRECT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 307 Temporary Redirect HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `307`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        temporary_redirect = HttpStatusCodeValueObject.TEMPORARY_REDIRECT()
        print(repr(temporary_redirect))
        # >>> HttpStatusCodeValueObject(value=307)
        ```
        """
        return cls(value=307)

    @classmethod
    def PERMANENT_REDIRECT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 308 Permanent Redirect HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `308`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        permanent_redirect = HttpStatusCodeValueObject.PERMANENT_REDIRECT()
        print(repr(permanent_redirect))
        # >>> HttpStatusCodeValueObject(value=308)
        ```
        """
        return cls(value=308)

    @classmethod
    def BAD_REQUEST(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 400 Bad Request HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `400`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        bad_request = HttpStatusCodeValueObject.BAD_REQUEST()
        print(repr(bad_request))
        # >>> HttpStatusCodeValueObject(value=400)
        ```
        """
        return cls(value=400)

    @classmethod
    def UNAUTHORIZED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 401 Unauthorized HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `401`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        unauthorized = HttpStatusCodeValueObject.UNAUTHORIZED()
        print(repr(unauthorized))
        # >>> HttpStatusCodeValueObject(value=401)
        ```
        """
        return cls(value=401)

    @classmethod
    def PAYMENT_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 402 Payment Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `402`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        payment_required = HttpStatusCodeValueObject.PAYMENT_REQUIRED()
        print(repr(payment_required))
        # >>> HttpStatusCodeValueObject(value=402)
        ```
        """
        return cls(value=402)

    @classmethod
    def FORBIDDEN(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 403 Forbidden HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `403`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        forbidden = HttpStatusCodeValueObject.FORBIDDEN()
        print(repr(forbidden))
        # >>> HttpStatusCodeValueObject(value=403)
        ```
        """
        return cls(value=403)

    @classmethod
    def NOT_FOUND(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 404 Not Found HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `404`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        not_found = HttpStatusCodeValueObject.NOT_FOUND()
        print(repr(not_found))
        # >>> HttpStatusCodeValueObject(value=404)
        ```
        """
        return cls(value=404)

    @classmethod
    def METHOD_NOT_ALLOWED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 405 Method Not Allowed HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `405`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        method_not_allowed = HttpStatusCodeValueObject.METHOD_NOT_ALLOWED()
        print(repr(method_not_allowed))
        # >>> HttpStatusCodeValueObject(value=405)
        ```
        """
        return cls(value=405)

    @classmethod
    def NOT_ACCEPTABLE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 406 Not Acceptable HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `406`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        not_acceptable = HttpStatusCodeValueObject.NOT_ACCEPTABLE()
        print(repr(not_acceptable))
        # >>> HttpStatusCodeValueObject(value=406)
        ```
        """
        return cls(value=406)

    @classmethod
    def PROXY_AUTHENTICATION_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 407 Proxy Authentication Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `407`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        proxy_authentication_required = HttpStatusCodeValueObject.PROXY_AUTHENTICATION_REQUIRED()
        print(repr(proxy_authentication_required))
        # >>> HttpStatusCodeValueObject(value=407)
        ```
        """
        return cls(value=407)

    @classmethod
    def REQUEST_TIMEOUT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 408 Request Timeout HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `408`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        request_timeout = HttpStatusCodeValueObject.REQUEST_TIMEOUT()
        print(repr(request_timeout))
        # >>> HttpStatusCodeValueObject(value=408)
        ```
        """
        return cls(value=408)

    @classmethod
    def CONFLICT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 409 Conflict HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `409`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        conflict = HttpStatusCodeValueObject.CONFLICT()
        print(repr(conflict))
        # >>> HttpStatusCodeValueObject(value=409)
        ```
        """
        return cls(value=409)

    @classmethod
    def GONE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 410 Gone HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `410`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        gone = HttpStatusCodeValueObject.GONE()
        print(repr(gone))
        # >>> HttpStatusCodeValueObject(value=410)
        ```
        """
        return cls(value=410)

    @classmethod
    def LENGTH_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 411 Length Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `411`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        length_required = HttpStatusCodeValueObject.LENGTH_REQUIRED()
        print(repr(length_required))
        # >>> HttpStatusCodeValueObject(value=411)
        ```
        """
        return cls(value=411)

    @classmethod
    def PRECONDITION_FAILED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 412 Precondition Failed HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `412`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        precondition_failed = HttpStatusCodeValueObject.PRECONDITION_FAILED()
        print(repr(precondition_failed))
        # >>> HttpStatusCodeValueObject(value=412)
        ```
        """
        return cls(value=412)

    @classmethod
    def CONTENT_TOO_LARGE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 413 Content Too Large HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `413`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        content_too_large = HttpStatusCodeValueObject.CONTENT_TOO_LARGE()
        print(repr(content_too_large))
        # >>> HttpStatusCodeValueObject(value=413)
        ```
        """
        return cls(value=413)

    @classmethod
    def URI_TOO_LONG(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 414 URI Too Long HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `414`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        uri_too_long = HttpStatusCodeValueObject.URI_TOO_LONG()
        print(repr(uri_too_long))
        # >>> HttpStatusCodeValueObject(value=414)
        ```
        """
        return cls(value=414)

    @classmethod
    def UNSUPPORTED_MEDIA_TYPE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 415 Unsupported Media Type HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `415`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        unsupported_media_type = HttpStatusCodeValueObject.UNSUPPORTED_MEDIA_TYPE()
        print(repr(unsupported_media_type))
        # >>> HttpStatusCodeValueObject(value=415)
        ```
        """
        return cls(value=415)

    @classmethod
    def RANGE_NOT_SATISFIABLE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 416 Range Not Satisfiable HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `416`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        range_not_satisfiable = HttpStatusCodeValueObject.RANGE_NOT_SATISFIABLE()
        print(repr(range_not_satisfiable))
        # >>> HttpStatusCodeValueObject(value=416)
        ```
        """
        return cls(value=416)

    @classmethod
    def EXPECTATION_FAILED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 417 Expectation Failed HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `417`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        expectation_failed = HttpStatusCodeValueObject.EXPECTATION_FAILED()
        print(repr(expectation_failed))
        # >>> HttpStatusCodeValueObject(value=417)
        ```
        """
        return cls(value=417)

    @classmethod
    def IM_A_TEAPOT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the legacy 418 I'm a Teapot HTTP status code.

        IANA currently marks code 418 as unused; this constructor preserves the widely used legacy phrase.

        Returns:
            HttpStatusCodeValueObject: A value object containing `418`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        im_a_teapot = HttpStatusCodeValueObject.IM_A_TEAPOT()
        print(repr(im_a_teapot))
        # >>> HttpStatusCodeValueObject(value=418)
        ```
        """
        return cls(value=418)

    @classmethod
    def MISDIRECTED_REQUEST(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 421 Misdirected Request HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `421`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        misdirected_request = HttpStatusCodeValueObject.MISDIRECTED_REQUEST()
        print(repr(misdirected_request))
        # >>> HttpStatusCodeValueObject(value=421)
        ```
        """
        return cls(value=421)

    @classmethod
    def UNPROCESSABLE_CONTENT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 422 Unprocessable Content HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `422`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        unprocessable_content = HttpStatusCodeValueObject.UNPROCESSABLE_CONTENT()
        print(repr(unprocessable_content))
        # >>> HttpStatusCodeValueObject(value=422)
        ```
        """
        return cls(value=422)

    @classmethod
    def LOCKED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 423 Locked HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `423`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        locked = HttpStatusCodeValueObject.LOCKED()
        print(repr(locked))
        # >>> HttpStatusCodeValueObject(value=423)
        ```
        """
        return cls(value=423)

    @classmethod
    def FAILED_DEPENDENCY(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 424 Failed Dependency HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `424`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        failed_dependency = HttpStatusCodeValueObject.FAILED_DEPENDENCY()
        print(repr(failed_dependency))
        # >>> HttpStatusCodeValueObject(value=424)
        ```
        """
        return cls(value=424)

    @classmethod
    def TOO_EARLY(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 425 Too Early HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `425`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        too_early = HttpStatusCodeValueObject.TOO_EARLY()
        print(repr(too_early))
        # >>> HttpStatusCodeValueObject(value=425)
        ```
        """
        return cls(value=425)

    @classmethod
    def UPGRADE_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 426 Upgrade Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `426`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        upgrade_required = HttpStatusCodeValueObject.UPGRADE_REQUIRED()
        print(repr(upgrade_required))
        # >>> HttpStatusCodeValueObject(value=426)
        ```
        """
        return cls(value=426)

    @classmethod
    def PRECONDITION_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 428 Precondition Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `428`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        precondition_required = HttpStatusCodeValueObject.PRECONDITION_REQUIRED()
        print(repr(precondition_required))
        # >>> HttpStatusCodeValueObject(value=428)
        ```
        """
        return cls(value=428)

    @classmethod
    def TOO_MANY_REQUESTS(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 429 Too Many Requests HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `429`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        too_many_requests = HttpStatusCodeValueObject.TOO_MANY_REQUESTS()
        print(repr(too_many_requests))
        # >>> HttpStatusCodeValueObject(value=429)
        ```
        """
        return cls(value=429)

    @classmethod
    def REQUEST_HEADER_FIELDS_TOO_LARGE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 431 Request Header Fields Too Large HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `431`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        request_header_fields_too_large = HttpStatusCodeValueObject.REQUEST_HEADER_FIELDS_TOO_LARGE()
        print(repr(request_header_fields_too_large))
        # >>> HttpStatusCodeValueObject(value=431)
        ```
        """
        return cls(value=431)

    @classmethod
    def UNAVAILABLE_FOR_LEGAL_REASONS(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 451 Unavailable For Legal Reasons HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `451`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        unavailable_for_legal_reasons = HttpStatusCodeValueObject.UNAVAILABLE_FOR_LEGAL_REASONS()
        print(repr(unavailable_for_legal_reasons))
        # >>> HttpStatusCodeValueObject(value=451)
        ```
        """
        return cls(value=451)

    @classmethod
    def INTERNAL_SERVER_ERROR(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 500 Internal Server Error HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `500`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        internal_server_error = HttpStatusCodeValueObject.INTERNAL_SERVER_ERROR()
        print(repr(internal_server_error))
        # >>> HttpStatusCodeValueObject(value=500)
        ```
        """
        return cls(value=500)

    @classmethod
    def NOT_IMPLEMENTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 501 Not Implemented HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `501`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        not_implemented = HttpStatusCodeValueObject.NOT_IMPLEMENTED()
        print(repr(not_implemented))
        # >>> HttpStatusCodeValueObject(value=501)
        ```
        """
        return cls(value=501)

    @classmethod
    def BAD_GATEWAY(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 502 Bad Gateway HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `502`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        bad_gateway = HttpStatusCodeValueObject.BAD_GATEWAY()
        print(repr(bad_gateway))
        # >>> HttpStatusCodeValueObject(value=502)
        ```
        """
        return cls(value=502)

    @classmethod
    def SERVICE_UNAVAILABLE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 503 Service Unavailable HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `503`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        service_unavailable = HttpStatusCodeValueObject.SERVICE_UNAVAILABLE()
        print(repr(service_unavailable))
        # >>> HttpStatusCodeValueObject(value=503)
        ```
        """
        return cls(value=503)

    @classmethod
    def GATEWAY_TIMEOUT(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 504 Gateway Timeout HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `504`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        gateway_timeout = HttpStatusCodeValueObject.GATEWAY_TIMEOUT()
        print(repr(gateway_timeout))
        # >>> HttpStatusCodeValueObject(value=504)
        ```
        """
        return cls(value=504)

    @classmethod
    def HTTP_VERSION_NOT_SUPPORTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 505 HTTP Version Not Supported HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `505`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        http_version_not_supported = HttpStatusCodeValueObject.HTTP_VERSION_NOT_SUPPORTED()
        print(repr(http_version_not_supported))
        # >>> HttpStatusCodeValueObject(value=505)
        ```
        """
        return cls(value=505)

    @classmethod
    def VARIANT_ALSO_NEGOTIATES(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 506 Variant Also Negotiates HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `506`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        variant_also_negotiates = HttpStatusCodeValueObject.VARIANT_ALSO_NEGOTIATES()
        print(repr(variant_also_negotiates))
        # >>> HttpStatusCodeValueObject(value=506)
        ```
        """
        return cls(value=506)

    @classmethod
    def INSUFFICIENT_STORAGE(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 507 Insufficient Storage HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `507`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        insufficient_storage = HttpStatusCodeValueObject.INSUFFICIENT_STORAGE()
        print(repr(insufficient_storage))
        # >>> HttpStatusCodeValueObject(value=507)
        ```
        """
        return cls(value=507)

    @classmethod
    def LOOP_DETECTED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 508 Loop Detected HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `508`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        loop_detected = HttpStatusCodeValueObject.LOOP_DETECTED()
        print(repr(loop_detected))
        # >>> HttpStatusCodeValueObject(value=508)
        ```
        """
        return cls(value=508)

    @classmethod
    def NOT_EXTENDED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the obsolete 510 Not Extended HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `510`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        not_extended = HttpStatusCodeValueObject.NOT_EXTENDED()
        print(repr(not_extended))
        # >>> HttpStatusCodeValueObject(value=510)
        ```
        """
        return cls(value=510)

    @classmethod
    def NETWORK_AUTHENTICATION_REQUIRED(cls) -> HttpStatusCodeValueObject:
        """
        Create a value object for the 511 Network Authentication Required HTTP status code.

        Returns:
            HttpStatusCodeValueObject: A value object containing `511`.

        Example:
        ```python
        from value_object_pattern.usables.internet import HttpStatusCodeValueObject

        network_authentication_required = HttpStatusCodeValueObject.NETWORK_AUTHENTICATION_REQUIRED()
        print(repr(network_authentication_required))
        # >>> HttpStatusCodeValueObject(value=511)
        ```
        """
        return cls(value=511)
