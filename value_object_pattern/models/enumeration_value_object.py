"""
EnumerationValueObject module.
"""

from enum import Enum
from inspect import isclass
from sys import version_info
from typing import Any, Generic, TypeVar, get_args, get_origin

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject

E = TypeVar('E', bound=Enum)


class EnumerationValueObject(ValueObject[str | E], Generic[E]):  # noqa: UP046
    """
    EnumerationValueObject is a value object that ensures the provided value is from an enumeration.

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

                cls._enumeration = enumeration
                return

        raise TypeError('EnumerationValueObject must be parameterized, e.g. "class ColorValueObject(EnumerationValueObject[ColorEnumeration])".')  # noqa: E501  # fmt: skip

    @override
    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the value object.

        Returns:
            str: A string representation of the value object in the format 'ClassName(value=value)'.

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
        print(repr(red))
        # >>> ColorValueObject(value=ColorEnumeration.RED)
        ```
        """
        return f'{self.__class__.__name__}(value={self.value.__class__.__name__}.{self.value.name})'

    @process(order=0)
    def _ensure_value_is_stored_as_enumeration(self, value: str | E) -> E:
        """
        Ensures the value object `value` is stored as an enumeration.

        Args:
            value (str | E): The provided value. It can be the name of the member or the member itself.

        Returns:
            E: The processed value.
        """
        if type(value) is str:
            return self._enumeration[value.upper()]

        return value  # type: ignore[return-value]

    @validation(order=0)
    def _ensure_value_is_from_enumeration(self, value: str | E) -> None:
        """
        Ensures the value object `value` is from the enumeration.

        Args:
            value (str | E): The provided value. It can be the name of the member or the member itself.

        Raises:
            TypeError: If the `value` is not from the enumeration.
        """
        if isinstance(value, self._enumeration):
            return

        if isinstance(value, str) and value in self._enumeration.__members__:
            return

        raise TypeError(f'EnumerationValueObject value <<<{value}>>> must be from the enumeration <<<{self._title}>>>.')  # noqa: E501  # fmt: skip

    @override
    @property
    def value(self) -> E:
        """
        Returns the value object value.

        Returns:
            E: The value object value.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer.value)
        # >>> 10
        ```
        """
        return self._value  # type: ignore[return-value]
