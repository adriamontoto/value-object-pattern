"""
EnumerationValueObject module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from inspect import isclass
from typing import Any, Generic, NoReturn, TypeVar, get_args, get_origin

from value_object_pattern.decorators import process, validation

from .value_object import ValueObject

E = TypeVar('E', bound=Enum)


class EnumerationValueObject(ValueObject[Any | E], Generic[E]):  # noqa: UP046
    """
    EnumerationValueObject is a value object that ensures the provided value is from an enumeration.

    ***This class is abstract and should not be instantiated directly***.

    Example:
    ```python
    from enum import Enum, unique

    from value_object_pattern import EnumerationValueObject


    @unique
    class ColorEnumeration(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3


    class ColorValueObject(EnumerationValueObject[ColorEnumeration]):
        pass


    red = ColorValueObject(value=ColorEnumeration.RED)
    green = ColorValueObject(value='GREEN')
    print(repr(red), repr(green))
    # >>> ColorValueObject(value=ColorEnumeration.RED) ColorValueObject(value=ColorEnumeration.GREEN)
    ```
    """

    _enumeration: type[E]

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initializes the class.

        Args:
            **kwargs (Any): Keyword arguments.

        Raises:
            TypeError: If the class parameter is not an Enum subclass.
            TypeError: If the class is not parameterized.
        """
        super().__init_subclass__(**kwargs)

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(tp=base) is EnumerationValueObject:
                enumeration, *_ = get_args(tp=base)

                if not (isclass(object=enumeration) and issubclass(enumeration, Enum)):
                    raise TypeError(f'EnumerationValueObject[...] <<<{enumeration}>>> must be an Enum subclass. Got <<<{type(enumeration).__name__}>>> type.')  # noqa: E501  # fmt: skip

                cls._enumeration = enumeration  # type: ignore[assignment]
                return

        raise TypeError('EnumerationValueObject must be parameterized, e.g. "class ColorValueObject(EnumerationValueObject[ColorEnumeration])".')  # noqa: E501  # fmt: skip

    @process(order=0)
    def _ensure_value_is_stored_as_enumeration(self, value: Any | E) -> E:
        """
        Ensures the value object `value` is stored as an enumeration.

        Args:
            value (Any | E): The provided value. It can be the name of the member or the member itself.

        Raises:
            TypeError: If the `value` is not from the enumeration.

        Returns:
            E: The processed value.
        """
        if isinstance(value, self._enumeration):
            return value

        for member in self._enumeration:
            if member.value == value:
                return member

        self._raise_value_is_not_from_enumeration(value=value)

    @validation(order=0)
    def _ensure_value_is_from_enumeration(self, value: Any | E) -> None:
        """
        Ensures the value object `value` is from the enumeration.

        Args:
            value (Any | E): The provided value. It can be the name of the member or the member itself.

        Raises:
            TypeError: If the `value` is not from the enumeration.
        """
        if isinstance(value, self._enumeration):
            return

        if any(value == member.value for member in self._enumeration):
            return

        self._raise_value_is_not_from_enumeration(value=value)

    def _raise_value_is_not_from_enumeration(self, value: Any) -> NoReturn:
        """
        Raises a TypeError exception if the value is not from the enumeration.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the value is not from the enumeration.
        """
        raise TypeError(f'EnumerationValueObject value <<<{value}>>> must be from the enumeration <<<{self._enumeration.__name__}>>>. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @override
    @property
    def value(self) -> E:
        """
        Returns the value object value.

        Returns:
            E: The value object value.

        Example:
        ```python
        from enum import Enum, unique

        from value_object_pattern import EnumerationValueObject


        @unique
        class ColorEnumeration(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3


        class ColorValueObject(EnumerationValueObject[ColorEnumeration]):
            pass


        red = ColorValueObject(value=ColorEnumeration.RED)
        print(red.value)
        # >>> ColorEnumeration.RED
        ```
        """
        return self._value
