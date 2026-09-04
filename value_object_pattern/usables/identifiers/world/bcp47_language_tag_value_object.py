"""
Bcp47LanguageTagValueObject value object.
"""

from re import Match, Pattern, compile as re_compile
from typing import NoReturn, cast

from value_object_pattern.decorators import process, validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .utils import (
    get_bcp47_extlang_to_prefix_mapping,
    get_bcp47_grandfathered_tag_mapping,
    get_bcp47_language_subtags,
    get_bcp47_redundant_tag_mapping,
    get_bcp47_region_subtags,
    get_bcp47_script_subtags,
    get_bcp47_variant_subtags,
)


class Bcp47LanguageTagValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate and normalize an IETF BCP 47 language tag.

    Core language, extended-language, script, region, and variant subtags are checked against the packaged IANA Language
    Subtag Registry catalogs. Extension and private-use sequences are syntax-checked as permitted by
    RFC 5646. Input is case-insensitive and stored using the recommended language, script, and region casing. BCP 47
    requires hyphen separators, so underscore-separated locale identifiers such as `en_US` are rejected.

    References:
        RFC 5646: https://www.rfc-editor.org/rfc/rfc5646.html
        IANA registry: https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world import Bcp47LanguageTagValueObject

    language_tag = Bcp47LanguageTagValueObject(value='ZH-hant-tw')
    print(repr(language_tag))
    # >>> Bcp47LanguageTagValueObject(value='zh-Hant-TW')
    ```
    """

    _LANGUAGE_TAG_REGEX: Pattern[str] = re_compile(pattern=r'(?P<language>[a-z]{2,8})(?P<extlangs>(?:-[a-z]{3}){0,3})(?:-(?P<script>[a-z]{4}))?(?:-(?P<region>[a-z]{2}|[0-9]{3}))?(?P<variants>(?:-(?:[a-z0-9]{5,8}|[0-9][a-z0-9]{3}))*)(?P<extensions>(?:-[0-9a-wy-z](?:-[a-z0-9]{2,8})+)*)(?P<private_use>(?:-x(?:-[a-z0-9]{1,8})+)?)')  # noqa: E501  # fmt: skip
    _PRIVATE_USE_REGEX: Pattern[str] = re_compile(pattern=r'x(?:-[a-z0-9]{1,8})+')

    @classmethod
    def _is_registered_or_private_use_tag(cls, value: str) -> bool:
        """
        Return whether a complete tag is registered or reserved for private use.

        Args:
            value (str): Language tag to check.

        Returns:
            bool: True if the tag is registered or reserved for private use, False otherwise.
        """
        return (
            value in get_bcp47_grandfathered_tag_mapping()
            or value in get_bcp47_redundant_tag_mapping()
            or cls._PRIVATE_USE_REGEX.fullmatch(string=value) is not None
        )

    @staticmethod
    def _is_registered_subtag(subtag: str, registered_subtags: tuple[str, ...]) -> bool:
        """
        Return whether a subtag is registered directly or through an inclusive range.

        Args:
            subtag (str): Subtag to check.
            registered_subtags (tuple[str, ...]): Registered subtags in lowercase.

        Returns:
            bool: True if the subtag is registered, False otherwise.
        """
        for registered_subtag in registered_subtags:
            if subtag == registered_subtag:
                return True

            if '..' in registered_subtag:
                start, end = registered_subtag.split(sep='..', maxsplit=1)
                if start <= subtag <= end:
                    return True

        return False

    @process(order=0)
    def _normalize_case(self, value: str) -> str:
        """
        Normalize the language tag using BCP 47 casing conventions.

        Args:
            value (str): Language tag to normalize.

        Returns:
            str: Language tag with normalized casing.
        """
        lowercase_value = value.lower()
        registered_tag = get_bcp47_grandfathered_tag_mapping().get(
            lowercase_value
        ) or get_bcp47_redundant_tag_mapping().get(lowercase_value)
        if registered_tag is not None:
            return registered_tag

        subtags = lowercase_value.split('-')
        normalized_subtags = [subtags[0]]
        index = 1

        if subtags[0] == 'x':
            return '-'.join(subtags)

        extlang_count = 0
        while (
            index < len(subtags)
            and extlang_count < 3
            and len(subtags[index]) == 3
            and subtags[index].isascii()
            and subtags[index].isalpha()
        ):
            normalized_subtags.append(subtags[index])
            index += 1
            extlang_count += 1

        if index < len(subtags) and len(subtags[index]) == 4 and subtags[index].isascii() and subtags[index].isalpha():
            normalized_subtags.append(subtags[index].title())
            index += 1

        if index < len(subtags) and (
            (len(subtags[index]) == 2 and subtags[index].isascii() and subtags[index].isalpha())
            or (len(subtags[index]) == 3 and subtags[index].isascii() and subtags[index].isdigit())
        ):
            normalized_subtags.append(subtags[index].upper())
            index += 1

        normalized_subtags.extend(subtags[index:])

        return '-'.join(normalized_subtags)

    @validation(order=0, early_process=True)
    def _validate_language_tag_structure(self, value: str, processed_value: str) -> None:
        """
        Validate the overall BCP 47 language-tag structure.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If the value is not a well-formed BCP 47 language tag.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        if not self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value):
            self._raise_value_is_not_well_formed_bcp47_language_tag(value=value)

    def _raise_value_is_not_well_formed_bcp47_language_tag(self, value: str) -> NoReturn:
        """
        Raise an error for a language tag with invalid structure.

        Args:
            value (str): Invalid language tag.

        Raises:
            ValueError: Always raised with the invalid value.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> is not a well-formed BCP 47 language tag.')

    @validation(order=1, early_process=True)
    def _validate_language_subtag(self, value: str, processed_value: str) -> None:
        """
        Validate the primary language subtag.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If the language subtag is not registered.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        language = match.group('language')
        if not self._is_registered_subtag(subtag=language, registered_subtags=get_bcp47_language_subtags()):
            self._raise_value_has_invalid_language_subtag(value=value, language=language)

    def _raise_value_has_invalid_language_subtag(self, value: str, language: str) -> NoReturn:
        """
        Raise an error for an unregistered language subtag.

        Args:
            value (str): Invalid language tag.
            language (str): Unregistered language subtag.

        Raises:
            ValueError: Always raised with the invalid language subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has an invalid language subtag <<<{language}>>>.')  # noqa: E501  # fmt: skip

    @validation(order=2, early_process=True)
    def _validate_extended_language_subtags(self, value: str, processed_value: str) -> None:
        """
        Validate extended-language subtags against their primary language.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If an extended-language subtag is not valid for the primary language.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        language = match.group('language')
        for extlang in match.group('extlangs').split('-')[1:]:
            if get_bcp47_extlang_to_prefix_mapping().get(extlang) != language:
                self._raise_value_has_invalid_extended_language_subtag(value=value, language=language, extlang=extlang)

    def _raise_value_has_invalid_extended_language_subtag(self, value: str, language: str, extlang: str) -> NoReturn:
        """
        Raise an error for an extended-language subtag with an invalid prefix.

        Args:
            value (str): Invalid language tag.
            language (str): Primary language subtag.
            extlang (str): Invalid extended-language subtag.

        Raises:
            ValueError: Always raised with the invalid extended-language subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has an invalid extended language subtag <<<{extlang}>>> for language <<<{language}>>>.')  # noqa: E501  # fmt: skip

    @validation(order=3, early_process=True)
    def _validate_script_subtag(self, value: str, processed_value: str) -> None:
        """
        Validate the script subtag.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If the script subtag is not registered.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        script = match.group('script')
        if script is not None and not self._is_registered_subtag(
            subtag=script,
            registered_subtags=get_bcp47_script_subtags(),
        ):
            self._raise_value_has_invalid_script_subtag(value=value, script=script.title())

    def _raise_value_has_invalid_script_subtag(self, value: str, script: str) -> NoReturn:
        """
        Raise an error for an unregistered script subtag.

        Args:
            value (str): Invalid language tag.
            script (str): Unregistered script subtag.

        Raises:
            ValueError: Always raised with the invalid script subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has an invalid script subtag <<<{script}>>>.')  # noqa: E501  # fmt: skip

    @validation(order=4, early_process=True)
    def _validate_region_subtag(self, value: str, processed_value: str) -> None:
        """
        Validate the region subtag.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If the region subtag is not registered.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        region = match.group('region')
        if region is not None and not self._is_registered_subtag(
            subtag=region,
            registered_subtags=get_bcp47_region_subtags(),
        ):
            self._raise_value_has_invalid_region_subtag(value=value, region=region.upper())

    def _raise_value_has_invalid_region_subtag(self, value: str, region: str) -> NoReturn:
        """
        Raise an error for an unregistered region subtag.

        Args:
            value (str): Invalid language tag.
            region (str): Unregistered region subtag.

        Raises:
            ValueError: Always raised with the invalid region subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has an invalid region subtag <<<{region}>>>.')  # noqa: E501  # fmt: skip

    @validation(order=5, early_process=True)
    def _validate_variant_subtags(self, value: str, processed_value: str) -> None:
        """
        Validate registered and non-duplicated variant subtags.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If a variant is unregistered or duplicated.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        variants: set[str] = set()
        for variant in match.group('variants').split('-')[1:]:
            if variant in variants:
                self._raise_value_has_duplicated_variant_subtag(value=value, variant=variant)

            if variant not in get_bcp47_variant_subtags():
                self._raise_value_has_invalid_variant_subtag(value=value, variant=variant)

            variants.add(variant)

    def _raise_value_has_invalid_variant_subtag(self, value: str, variant: str) -> NoReturn:
        """
        Raise an error for an unregistered variant subtag.

        Args:
            value (str): Invalid language tag.
            variant (str): Unregistered variant subtag.

        Raises:
            ValueError: Always raised with the invalid variant subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has an invalid variant subtag <<<{variant}>>>.')  # noqa: E501  # fmt: skip

    def _raise_value_has_duplicated_variant_subtag(self, value: str, variant: str) -> NoReturn:
        """
        Raise an error for a duplicated variant subtag.

        Args:
            value (str): Invalid language tag.
            variant (str): Duplicated variant subtag.

        Raises:
            ValueError: Always raised with the duplicated variant subtag.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has a duplicated variant subtag <<<{variant}>>>.')  # noqa: E501  # fmt: skip

    @validation(order=6, early_process=True)
    def _validate_extension_singletons(self, value: str, processed_value: str) -> None:
        """
        Validate that extension singletons do not repeat.

        Args:
            value (str): Original language tag.
            processed_value (str): Language tag with normalized casing.

        Raises:
            ValueError: If an extension singleton is duplicated.
        """
        lowercase_value = processed_value.lower()
        if self._is_registered_or_private_use_tag(value=lowercase_value):
            return

        match = cast(Match[str], self._LANGUAGE_TAG_REGEX.fullmatch(string=lowercase_value))
        extension_singletons: set[str] = set()
        for singleton in (subtag for subtag in match.group('extensions').split('-')[1:] if len(subtag) == 1):
            if singleton in extension_singletons:
                self._raise_value_has_duplicated_extension_singleton(value=value, singleton=singleton)

            extension_singletons.add(singleton)

    def _raise_value_has_duplicated_extension_singleton(self, value: str, singleton: str) -> NoReturn:
        """
        Raise an error for a duplicated extension singleton.

        Args:
            value (str): Invalid language tag.
            singleton (str): Duplicated extension singleton.

        Raises:
            ValueError: Always raised with the duplicated singleton.
        """
        raise ValueError(f'Bcp47LanguageTagValueObject value <<<{value}>>> has a duplicated extension singleton <<<{singleton}>>>.')  # noqa: E501  # fmt: skip
