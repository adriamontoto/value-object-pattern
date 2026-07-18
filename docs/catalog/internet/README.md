# Internet Value Objects

Internet value objects validate web, network, and protocol-shaped strings. They are useful for accepting structured
configuration and user-facing input before the value reaches lower-level networking code.

## Imports

```python
from value_object_pattern.usables.internet import (
    DomainOrLocalhostValueObject,
    DomainValueObject,
    EmailAddressValueObject,
    PortValueObject,
)
from value_object_pattern.usables.internet.uri import HttpsUrlValueObject, UrlValueObject
```

## URLs, Hosts, And Domains

| Value Object | Rule |
| --- | --- |
| `UrlValueObject` | Validates URL syntax and stores the normalized URL form. |
| `HttpUrlValueObject` | Accepts only HTTP URLs. |
| `HttpsUrlValueObject` | Accepts only HTTPS URLs. |
| `HttpHttpsUrlValueObject` | Accepts HTTP or HTTPS URLs. |
| `HostValueObject` | Accepts host values. |
| `DomainOrLocalhostValueObject` | Accepts domain values or `localhost`. |
| `DomainValueObject` | Validates domain labels and top-level domains. |

## Addresses, Networks, And Ports

| Value Object | Rule |
| --- | --- |
| `IpAddressValueObject` | Accepts IPv4 or IPv6 address values. |
| `Ipv4AddressValueObject` | Accepts IPv4 address values. |
| `Ipv6AddressValueObject` | Accepts IPv6 address values. |
| `Ipv4NetworkValueObject` | Accepts IPv4 network values. |
| `Ipv6NetworkValueObject` | Accepts IPv6 network values. |
| `MacAddressValueObject` | Accepts supported MAC address formats. |
| `PortValueObject` | Accepts valid TCP/UDP port numbers. |

## Keys, Slugs, And Metadata

| Value Object | Rule |
| --- | --- |
| `SnakeCaseKeyValueObject` | Accepts snake_case key strings. |
| `KebabCaseKeyValueObject` | Accepts kebab-case key strings. |
| `SlugValueObject` | Accepts slug strings. |
| `EmailAddressValueObject` | Accepts email address strings. |
| `AwsCloudRegionValueObject` | Accepts AWS cloud region identifiers from the package catalog. |
| `UserAgentValueObject` | Accepts user-agent strings. |
