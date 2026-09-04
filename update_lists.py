"""
Update the lists used in the Object Mother Pattern package.
"""

from datetime import UTC, date, datetime
from pathlib import Path
from re import DOTALL, findall, fullmatch
from urllib.request import urlopen
from xml.etree import ElementTree


def write_if_changed(path: str, lines: tuple[str, ...]) -> None:
    """
    Write list content to a file only when the body has changed to avoid noisy commits. Preserves the existing file
    when no changes are detected.

    Args:
        path (str): The file path to update.
        lines (tuple[str, ...]): The lines to write to the file.
    """
    header_prefix = '# This file was automatically updated using "update_lists.py" on '
    new_body = '\n'.join(lines) + '\n'
    file_path = Path(path)

    if file_path.exists():
        current_text = file_path.read_text(encoding='utf-8')
        _, _, existing_body = current_text.partition('\n')
        if existing_body == f'\n{new_body}':
            return

    now = datetime.now(tz=UTC).isoformat()
    new_text = f'{header_prefix}{now}\n\n{new_body}'
    file_path.write_text(new_text, encoding='utf-8')


def update_bcp47_registry() -> None:  # noqa: C901
    """
    Retrieve the IANA Language Subtag Registry and update the local BCP 47 catalogs.

    Raises:
        RuntimeError: When the source cannot be retrieved, parsed, or validated.

    References:
        IANA Language Subtag Registry: https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry
    """
    url = 'https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry'
    paths = {
        'language': 'value_object_pattern/usables/identifiers/world/utils/bcp47_language_subtags.txt',
        'extlang': 'value_object_pattern/usables/identifiers/world/utils/bcp47_extlang_subtags.txt',
        'script': 'value_object_pattern/usables/identifiers/world/utils/bcp47_script_subtags.txt',
        'region': 'value_object_pattern/usables/identifiers/world/utils/bcp47_region_subtags.txt',
        'variant': 'value_object_pattern/usables/identifiers/world/utils/bcp47_variant_subtags.txt',
        'grandfathered': 'value_object_pattern/usables/identifiers/world/utils/bcp47_grandfathered_tags.txt',
        'redundant': 'value_object_pattern/usables/identifiers/world/utils/bcp47_redundant_tags.txt',
    }
    subtag_patterns = {
        'language': r'[a-z]{2,8}(?:\.\.[a-z]{2,8})?',
        'extlang': r'[a-z]{3}',
        'script': r'[a-z]{4}(?:\.\.[a-z]{4})?',
        'region': r'(?:[a-z]{2}(?:\.\.[a-z]{2})?|[0-9]{3})',
        'variant': r'(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3})',
    }

    def parse_fields(raw_record: str) -> dict[str, list[str]]:
        fields: dict[str, list[str]] = {}
        for line in raw_record.strip().splitlines():
            if line[:1].isspace():
                continue

            name, separator, value = line.partition(':')
            if not separator or not name or not value.strip():
                raise RuntimeError('The IANA Language Subtag Registry contains a malformed field.')

            fields.setdefault(name, []).append(value.strip())

        return fields

    def parse_entry(fields: dict[str, list[str]]) -> tuple[str, str]:
        registry_types = fields.get('Type', [])
        if len(registry_types) != 1 or registry_types[0] not in paths:
            raise RuntimeError('The IANA Language Subtag Registry contains an invalid record type.')

        registry_type = registry_types[0]
        value_field = 'Tag' if registry_type in {'grandfathered', 'redundant'} else 'Subtag'
        values = fields.get(value_field, [])
        if len(values) != 1:
            raise RuntimeError('The IANA Language Subtag Registry contains a record without one identifier.')

        entry = values[0] if value_field == 'Tag' else values[0].lower()
        pattern = subtag_patterns.get(registry_type)
        if pattern is not None and fullmatch(pattern, entry) is None:
            raise RuntimeError('The IANA Language Subtag Registry contains an invalid subtag.')

        if value_field == 'Tag' and fullmatch(r'[A-Za-z0-9]{1,8}(?:-[A-Za-z0-9]{1,8})+', entry) is None:
            raise RuntimeError('The IANA Language Subtag Registry contains an invalid registered tag.')

        if registry_type == 'extlang':
            prefixes = fields.get('Prefix', [])
            if len(prefixes) != 1 or fullmatch(r'[A-Za-z]{2,8}', prefixes[0]) is None:
                raise RuntimeError('The IANA Language Subtag Registry contains an invalid extlang prefix.')

            entry = f'{entry} {prefixes[0].lower()}'

        return registry_type, entry

    def parse_registry(content: str) -> dict[str, tuple[str, ...]]:
        raw_records = tuple(record for record in content.split('%%') if record.strip())
        if not raw_records:
            raise RuntimeError('The IANA Language Subtag Registry is empty.')

        metadata = parse_fields(raw_record=raw_records[0])
        file_dates = metadata.get('File-Date', [])
        if len(file_dates) != 1 or fullmatch(r'\d{4}-\d{2}-\d{2}', file_dates[0]) is None:
            raise RuntimeError('The IANA Language Subtag Registry has an invalid file date.')

        try:
            date.fromisoformat(file_dates[0])

        except ValueError as error:
            raise RuntimeError('The IANA Language Subtag Registry has an invalid file date.') from error

        catalogs: dict[str, list[str]] = {registry_type: [] for registry_type in paths}
        seen: dict[str, set[str]] = {registry_type: set() for registry_type in paths}
        for raw_record in raw_records[1:]:
            registry_type, entry = parse_entry(fields=parse_fields(raw_record=raw_record))
            lowercase_entry = entry.lower()
            if lowercase_entry in seen[registry_type]:
                raise RuntimeError('The IANA Language Subtag Registry contains a duplicate identifier.')

            seen[registry_type].add(lowercase_entry)
            catalogs[registry_type].append(entry)

        if any(not entries for entries in catalogs.values()):
            raise RuntimeError('The IANA Language Subtag Registry is missing a required record type.')

        return {registry_type: tuple(sorted(entries, key=str.lower)) for registry_type, entries in catalogs.items()}

    try:
        with urlopen(url=url) as response:  # noqa: S310
            content = response.read().decode('utf-8')

    except (OSError, UnicodeError) as error:
        raise RuntimeError('Failed to retrieve the IANA Language Subtag Registry.') from error

    catalogs = parse_registry(content=content)
    for registry_type, path in paths.items():
        write_if_changed(path=path, lines=catalogs[registry_type])


def update_aws_cloud_regions() -> None:
    """
    Retrieve AWS cloud regions from the official AWS documentation and update the local AWS regions file..

    Raise:
        RuntimeError: When unable to retrieve AWS regions from the official documentation.

    References:
        AWS Cloud Regions: https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions
    """
    url = 'https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html#available-regions'
    with urlopen(url=url) as response:  # noqa: S310
        content = response.read().decode('utf-8')

    pattern = r'<tr>\s*<td[^>]*tabindex="-1">(.*?)</td>\s*<td[^>]*tabindex="-1">.*?</td>\s*<td[^>]*tabindex="-1">.*?</td>\s*</tr>'  # noqa: E501
    aws_regions = tuple(region_code.lower() for region_code in findall(pattern=pattern, string=content, flags=DOTALL))
    if not aws_regions:
        raise RuntimeError('Failed to retrieve AWS regions from the official documentation.')

    path = 'value_object_pattern/usables/internet/utils/aws_regions.txt'
    write_if_changed(path=path, lines=aws_regions)


def update_tld_domains() -> None:
    """
    Retrieve top-level domains from IANA and update the local TLD file.

    Raise:
        RuntimeError: When unable to retrieve TLD domains from IANA.

    References:
        TLD Domains: https://data.iana.org/TLD/tlds-alpha-by-domain.txt
    """
    url = 'https://data.iana.org/TLD/tlds-alpha-by-domain.txt'
    with urlopen(url=url) as response:  # noqa: S310
        lines = response.read().decode('utf-8').splitlines()

    tld_domains = tuple(line.strip().lower() for line in lines if line and not line.startswith('#'))
    if not tld_domains:
        raise RuntimeError('Failed to retrieve TLD domains from IANA.')

    path = 'value_object_pattern/usables/internet/utils/tld_domains.txt'
    write_if_changed(path=path, lines=tld_domains)


def update_iso4217_alpha3_codes() -> None:
    """
    Retrieve current ISO 4217 alphabetic codes from SIX List One and update the local catalog.

    Raises:
        RuntimeError: When the source cannot be retrieved, parsed, or validated.

    References:
        ISO 4217: https://www.iso.org/iso-4217-currency-codes.html
        SIX List One: https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml
    """
    url = 'https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml'
    with urlopen(url=url) as response:
        content = response.read()

    if b'<!DOCTYPE' in content.upper() or b'<!ENTITY' in content.upper():
        raise RuntimeError('The official ISO 4217 List One catalog contains unsupported XML declarations.')

    try:
        root = ElementTree.fromstring(content)  # noqa: S314

    except ElementTree.ParseError as error:
        raise RuntimeError('Failed to parse the official ISO 4217 List One catalog.') from error

    if root.tag != 'ISO_4217':
        raise RuntimeError('The official ISO 4217 List One catalog has an unexpected root element.')

    published = root.attrib.get('Pblshd')
    if published is None or fullmatch(r'\d{4}-\d{2}-\d{2}', published) is None:
        raise RuntimeError('The official ISO 4217 List One catalog has an invalid publication date.')

    try:
        date.fromisoformat(published)

    except ValueError as error:
        raise RuntimeError('The official ISO 4217 List One catalog has an invalid publication date.') from error

    raw_codes = tuple(element.text for element in root.iter('Ccy'))
    if not raw_codes:
        raise RuntimeError('The official ISO 4217 List One catalog contains no currency codes.')

    codes: list[str] = []
    for raw_code in raw_codes:
        code = raw_code.strip().upper() if raw_code is not None else ''
        if fullmatch(r'[A-Z]{3}', code) is None:
            raise RuntimeError('The official ISO 4217 List One catalog contains an invalid currency code.')

        codes.append(code)

    write_if_changed(
        path='value_object_pattern/usables/money/utils/iso4217_alpha3_codes.txt',
        lines=tuple(sorted(set(codes))),
    )


if __name__ == '__main__':
    update_aws_cloud_regions()
    update_tld_domains()
    update_iso4217_alpha3_codes()
    update_bcp47_registry()
