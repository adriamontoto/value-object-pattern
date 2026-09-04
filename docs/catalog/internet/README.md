# Internet Value Objects

Internet value objects validate web, network, and protocol-shaped strings. They are useful for accepting structured
configuration and user-facing input before the value reaches lower-level networking code.

## Imports

```python
from value_object_pattern.usables.internet import (
    DomainOrLocalhostValueObject,
    DomainValueObject,
    EmailAddressValueObject,
    HttpMethodValueObject,
    HttpStatusCodeValueObject,
    IpAddressValueObject,
    IpNetworkValueObject,
    MediaTypeValueObject,
    PortValueObject,
)
from value_object_pattern.usables.internet.uri import HttpsUrlValueObject, UrlValueObject
```

## URLs, Hosts, And Domains

| Value Object                   | Rule                                                     |
| ------------------------------ | -------------------------------------------------------- |
| `UrlValueObject`               | Validates URL syntax and stores the normalized URL form. |
| `HttpUrlValueObject`           | Accepts only HTTP URLs.                                  |
| `HttpsUrlValueObject`          | Accepts only HTTPS URLs.                                 |
| `HttpHttpsUrlValueObject`      | Accepts HTTP or HTTPS URLs.                              |
| `HostValueObject`              | Accepts host values.                                     |
| `DomainOrLocalhostValueObject` | Accepts domain values or `localhost`.                    |
| `DomainValueObject`            | Validates domain labels and top-level domains.           |

## Addresses, Networks, And Ports

| Value Object             | Rule                                   |
| ------------------------ | -------------------------------------- |
| `IpAddressValueObject`   | Accepts IPv4 or IPv6 address values.   |
| `IpNetworkValueObject`   | Accepts IPv4 or IPv6 network values.   |
| `Ipv4AddressValueObject` | Accepts IPv4 address values.           |
| `Ipv6AddressValueObject` | Accepts IPv6 address values.           |
| `Ipv4NetworkValueObject` | Accepts IPv4 network values.           |
| `Ipv6NetworkValueObject` | Accepts IPv6 network values.           |
| `MacAddressValueObject`  | Accepts supported MAC address formats. |
| `PortValueObject`        | Accepts valid TCP/UDP port numbers.    |

Format-specific MAC classes are exported from `value_object_pattern.usables.internet.mac_addresses`.

## HTTP Methods And Status Codes

`HttpMethodValueObject` accepts the case-sensitive methods `CONNECT`, `DELETE`, `GET`, `HEAD`, `OPTIONS`, `PATCH`,
`POST`, `PUT`, `QUERY`, and `TRACE`. Each method is also available as a named constructor.

`HttpStatusCodeValueObject` accepts integer status codes from `100` through `599`. Named constructors cover known
codes, and `.reason_phrase` returns the known phrase or `None` for an unassigned code.

```python
from value_object_pattern.usables.internet import HttpMethodValueObject, HttpStatusCodeValueObject


method = HttpMethodValueObject.GET()
not_found = HttpStatusCodeValueObject.NOT_FOUND()
unassigned = HttpStatusCodeValueObject(value=599)

assert method.value == "GET"
assert not_found.value == 404
assert not_found.reason_phrase == "Not Found"
assert unassigned.reason_phrase is None
```

## Media Types

`MediaTypeValueObject` validates HTTP media-type syntax, normalizes type and subtype casing, and exposes parsed
parameters. Named constructors cover common media types:

```python
from value_object_pattern.usables.internet import MediaTypeValueObject


json_type = MediaTypeValueObject.JSON()
plain_text = MediaTypeValueObject.TEXT_PLAIN()
upload = MediaTypeValueObject.MULTIPART_FORM_DATA()
pdf = MediaTypeValueObject.APPLICATION_PDF()

assert json_type.value == 'application/json'
assert plain_text.value == 'text/plain'
assert upload.value == 'multipart/form-data'
assert pdf.value == 'application/pdf'
```

Use direct construction when a parameterized or less common media type is needed:

```python
html = MediaTypeValueObject(value='text/html; charset="UTF-8"')

assert html.top_level_type == 'text'
assert html.subtype == 'html'
assert html.parameters == {'charset': 'UTF-8'}
```

## Keys, Slugs, And Metadata

| Value Object                | Rule                                                           |
| --------------------------- | -------------------------------------------------------------- |
| `SnakeCaseKeyValueObject`   | Accepts snake_case key strings.                                |
| `KebabCaseKeyValueObject`   | Accepts kebab-case key strings.                                |
| `SlugValueObject`           | Accepts slug strings.                                          |
| `EmailAddressValueObject`   | Accepts email address strings.                                 |
| `AwsCloudRegionValueObject` | Accepts AWS cloud region identifiers from the package catalog. |
| `UserAgentValueObject`      | Accepts user-agent strings.                                    |

`ImeiValueObject` is available from `value_object_pattern.usables.internet.mobile` for IMEI values.
