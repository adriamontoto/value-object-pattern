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

    current_text = file_path.read_text(encoding='utf-8')
    _, _, existing_body = current_text.partition('\n')
    if existing_body[1:] == new_body:
        return

    now = datetime.now(tz=UTC).isoformat()
    new_text = f'{header_prefix}{now}\n\n{new_body}'
    file_path.write_text(new_text, encoding='utf-8')


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
