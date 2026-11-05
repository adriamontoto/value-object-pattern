"""
Provide a value object for normal semantic versions.
"""

from re import Pattern, compile as re_compile
from typing import NoReturn, Self

from value_object_pattern.decorators import validation
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject


class SemanticVersionValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    Validate a normal semantic version in `major.minor.patch` form. Each component is a non-negative ASCII integer
    without leading zeros. Pre-release identifiers, build metadata, version prefixes, and surrounding whitespace are
    not accepted. The original string is preserved, while `major`, `minor`, and `patch` expose integer components.
    Increment methods return a new instance of the same subclass and preserve error metadata. Increasing minor resets
    patch; increasing major resets both minor and patch.

    References:
        Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html

    Example:
    ```python
    from value_object_pattern.usables.internet import SemanticVersionValueObject

    version = SemanticVersionValueObject(value='1.2.3')
    print(version.major)
    # >>> 1
    print(version.minor)
    # >>> 2
    print(version.patch)
    # >>> 3
    ```
    """

    _VALIDATION_REGEX: Pattern[str] = re_compile(pattern=r'(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)')

    @property
    def major(self) -> int:
        """
        Return the major version component as an integer.

        Returns:
            int: The major version component.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        print(version.major)
        # >>> 1
        ```
        """
        return int(self.value.split('.')[0])

    @property
    def minor(self) -> int:
        """
        Return the minor version component as an integer.

        Returns:
            int: The minor version component.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        print(version.minor)
        # >>> 2
        ```
        """
        return int(self.value.split('.')[1])

    @property
    def patch(self) -> int:
        """
        Return the patch version component as an integer.

        Returns:
            int: The patch version component.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        print(version.patch)
        # >>> 3
        ```
        """
        return int(self.value.split('.')[2])

    def increase_patch(self) -> Self:
        """
        Return a new version with patch increased by one, preserving major and minor.

        Returns:
            Self: A new instance of the same subclass with the patch version increased by one.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        new_version = version.increase_patch()
        print(new_version.value)
        # >>> '1.2.4'
        ```
        """
        return self.__class__(
            value=f'{self.major}.{self.minor}.{self.patch + 1}',
            title=self.title,
            parameter=self.parameter,
        )

    def increase_minor(self) -> Self:
        """
        Return a new version with minor increased by one and patch reset to zero.

        Returns:
            Self: A new instance of the same subclass with the minor version increased by one and patch reset to zero.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        new_version = version.increase_minor()
        print(new_version.value)
        # >>> '1.3.0'
        ```
        """
        return self.__class__(
            value=f'{self.major}.{self.minor + 1}.0',
            title=self.title,
            parameter=self.parameter,
        )

    def increase_major(self) -> Self:
        """
        Return a new version with major increased by one and minor and patch reset to zero.

        Returns:
            Self: A new instance of the same subclass with the major version increased by one and minor and patch reset
            to zero.

        Example:
        ```python
        from value_object_pattern.usables.internet import SemanticVersionValueObject

        version = SemanticVersionValueObject(value='1.2.3')
        new_version = version.increase_major()
        print(new_version.value)
        # >>> '2.0.0'
        ```
        """
        return self.__class__(
            value=f'{self.major + 1}.0.0',
            title=self.title,
            parameter=self.parameter,
        )

    @validation(order=0)
    def _ensure_value_is_semantic_version(self, value: str) -> None:
        """
        Ensure the value is a normal semantic version.

        Args:
            value (str): The provided version string.

        Raises:
            ValueError: If the value does not use the `major.minor.patch` format.
        """
        if not self._VALIDATION_REGEX.fullmatch(string=value):
            self._raise_value_is_not_semantic_version(value=value)

    def _raise_value_is_not_semantic_version(self, value: str) -> NoReturn:
        """
        Raise an error for an invalid normal semantic version.

        Args:
            value (str): The invalid version string.

        Raises:
            ValueError: Always raised because the value is not a normal semantic version.
        """
        raise ValueError(f'SemanticVersionValueObject value <<<{value}>>> must use major.minor.patch format with non-negative ASCII integers and no leading zeros.')  # noqa: E501  # fmt: skip
