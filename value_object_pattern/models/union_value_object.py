"""
Value object for values constrained by a union annotation.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from enum import Enum
from inspect import isclass
from types import UnionType
from typing import Any, ClassVar, Generic, NoReturn, Self, TypeVar, Union, get_args, get_origin

from value_object_pattern.decorators import process, validation

from .base_model import BaseModel
from .primitive_conversion import from_primitive
from .type_matching import matches_expected_type
from .value_object import ValueObject

T = TypeVar('T', bound=Any)


def _validate_union_type_argument(*, type_argument: Any) -> None:
    """
    Validate a type argument used by UnionValueObject.

    Args:
        type_argument: The type argument to validate.

    Raises:
        TypeError: If the type argument is not a type-like annotation.
    """
    if isinstance(type_argument, TypeVar):
        return

    if type(type_argument) is not type and not isclass(object=type_argument) and get_origin(tp=type_argument) is None:
        raise TypeError(f'UnionValueObject[...] <<<{type_argument}>>> must be a type. Got <<<{type(type_argument).__name__}>>> type.')  # noqa: E501  # fmt: skip


class _UnionValueObjectAlias:
    """
    Runtime alias returned by `UnionValueObject[T]`.

    Python assigns `__orig_class__` only after `__init__` completes, but union conversion needs the type parameter
    during `ValueObject.__init__`. This alias keeps subclass declarations working through `__mro_entries__` and supports
    direct inline construction by creating a parameterized runtime subclass before validation starts.
    """

    _runtime_classes: ClassVar[dict[Any, type[UnionValueObject[Any]]]] = {}

    def __init__(self, *, origin: type[UnionValueObject[Any]], type_argument: Any) -> None:
        """
        Create a runtime alias for a parameterized UnionValueObject.

        Args:
            origin: The original UnionValueObject class.
            type_argument: The type argument used in `UnionValueObject[T]`.
        """
        self.__origin__ = origin
        self.__args__ = (type_argument,)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Construct an inline parameterized UnionValueObject instance.

        Args:
            *args: Positional arguments passed to the generated value object subclass.
            **kwargs: Keyword arguments passed to the generated value object subclass.

        Returns:
            Any: The constructed value object.
        """
        return self._runtime_class()(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """
        Delegate class attribute access to the generated runtime subclass.

        Args:
            name: The attribute name to retrieve.

        Returns:
            Any: The resolved attribute.
        """
        return getattr(self._runtime_class(), name)

    def __mro_entries__(self, bases: tuple[type, ...]) -> tuple[type[UnionValueObject[Any]], ...]:
        """
        Return the origin class when the alias is used as a base class.

        Args:
            bases: The original class bases supplied by Python.

        Returns:
            tuple[type[UnionValueObject[Any]], ...]: The base classes to use for MRO construction.
        """
        _ = bases

        return (self.__origin__,)

    def _runtime_class(self) -> type[UnionValueObject[Any]]:
        """
        Return the generated runtime subclass for this alias.

        Returns:
            type[UnionValueObject[Any]]: The runtime subclass.
        """
        type_argument, *_ = self.__args__
        _validate_union_type_argument(type_argument=type_argument)
        key = (self.__origin__, type_argument)
        if key not in self._runtime_classes:
            self._runtime_classes[key] = type(
                f'{self.__origin__.__name__}[{self._format_type_argument(type=type_argument)}]',
                (self.__origin__,),
                {
                    '_is_inline_parameterized_union_value_object': True,
                    '_type': type_argument,
                },
            )

        return self._runtime_classes[key]

    @staticmethod
    def _format_type_argument(*, type: Any) -> str:
        """
        Return a compact type-argument label for generated runtime class names.

        Args:
            type: The type argument to format.

        Returns:
            str: A readable type label.
        """
        origin = get_origin(tp=type)
        if origin in (Union, UnionType):
            return ' | '.join(_UnionValueObjectAlias._format_type_argument(type=allowed) for allowed in get_args(type))

        if hasattr(type, '__name__'):
            return type.__name__  # type: ignore[no-any-return]

        return str(type).replace('typing.', '')


class UnionValueObject(ValueObject[T], Generic[T]):  # noqa: UP046
    """
    Validate and store a value as one of the allowed union candidates.

    It supports primitives, `ValueObject` subclasses, `BaseModel` subclasses, `Enum` subclasses, nested collections,
    and combinations of those types. Input is converted to the first candidate that can represent it safely.

    Example:
    ```python
    from enum import Enum

    from value_object_pattern import BaseModel, UnionValueObject, ValueObject


    class Age(ValueObject[int]):
        pass


    class Tag(BaseModel):
        def __init__(self, name: str) -> None:
            self.name = name


    class Status(Enum):
        ON = 'on'
        OFF = 'off'


    class AgeOrTagOrStatusValueObject(UnionValueObject[Age | Tag | Status]):
        pass


    value = AgeOrTagOrStatusValueObject(value='on')
    print(value.value)
    # >>> Status.ON
    ```
    """

    _type: T

    @classmethod
    def __class_getitem__(cls, item: Any) -> Any:
        """
        Return a runtime alias that supports subclassing and inline construction.

        Args:
            item: The type argument used in `UnionValueObject[item]`.

        Returns:
            Any: A runtime alias for the parameterized UnionValueObject.
        """
        return _UnionValueObjectAlias(origin=cls, type_argument=item)

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Capture and validate the type or union annotation declared by a subclass.

        Args:
            **kwargs: Keyword arguments forwarded to the parent class hook.

        Raises:
            TypeError: If the class parameter is not a type-like annotation.
            TypeError: If the subclass is not parameterized with `UnionValueObject[T]`.
        """
        super().__init_subclass__(**kwargs)

        if getattr(cls, '_is_inline_parameterized_union_value_object', False):
            return

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(tp=base) is UnionValueObject or getattr(base, '__origin__', None) is UnionValueObject:
                _type, *_ = get_args(tp=base) or base.__args__

                _validate_union_type_argument(type_argument=_type)
                cls._type = _type
                return

        raise TypeError('UnionValueObject must be parameterized, e.g. "class IntOrStrValueObject(UnionValueObject[int | str])".')  # noqa: E501  # fmt: skip

    @validation(order=0, early_process=True)
    def _ensure_value_is_of_union_type(self, value: T, processed_value: T) -> None:
        """
        Ensures the value can be converted to one of the allowed union candidates.

        Args:
            value (T): The raw provided value.
            processed_value (T): The processed value that matched one union candidate.
        """
        _ = value
        _ = processed_value

    @process(order=0)
    def _ensure_value_is_stored_as_union_type(self, value: T) -> T:
        """
        Stores the value as the first matching union candidate.

        Args:
            value (T): The provided value.

        Returns:
            T: The processed value.
        """
        if self._type is Any:
            return value

        origin = get_origin(tp=self._type)
        allowed_types = get_args(self._type) if origin in (Union, UnionType) else (self._type,)
        last_error: Exception | None = None

        for allowed_type in allowed_types:
            try:
                return self._coerce_value_to_type(value=value, expected_type=allowed_type)  # type: ignore[no-any-return]

            except Exception as error:
                last_error = error

        if last_error is not None:
            raise TypeError(f'UnionValueObject value <<<{value}>>> must be of type <<<{self._type_label()}>>> type. Got <<<{type(value).__name__}>>> type.') from last_error  # noqa: E501  # fmt: skip

        self._raise_value_is_not_of_type(value=value)

    def _unwrap_candidate_value(self, *, value: Any, unwrap_enum: bool = True) -> Any:
        """
        Unwraps known wrapper values before candidate matching.

        Args:
            value (Any): Value to unwrap.
            unwrap_enum (bool, optional): Whether to unwrap Enum to `Enum.value`. Defaults to True.

        Returns:
            Any: Unwrapped value.
        """
        unwrapped = value

        while isinstance(unwrapped, ValueObject):
            unwrapped = unwrapped.value

        if unwrap_enum and isinstance(unwrapped, Enum):
            return unwrapped.value

        return unwrapped

    def _coerce_value_to_type(self, *, value: Any, expected_type: Any) -> Any:  # noqa: C901
        """
        Attempts to coerce a value into the provided expected type.

        Args:
            value (Any): The provided value.
            expected_type (Any): The target type annotation.

        Raises:
            TypeError: If the value cannot be coerced to the expected type.

        Returns:
            Any: The coerced value.
        """
        if expected_type is Any:
            return value

        origin = get_origin(tp=expected_type)
        if origin in (Union, UnionType):
            last_error: Exception | None = None
            for allowed in get_args(expected_type):
                try:
                    return self._coerce_value_to_type(value=value, expected_type=allowed)

                except Exception as error:
                    last_error = error

            raise TypeError(f'UnionValueObject value <<<{value}>>> must be of type <<<{self._format_single_type(type=expected_type)}>>> type. Got <<<{type(value).__name__}>>> type.') from last_error  # noqa: E501  # fmt: skip

        expected = origin or expected_type

        if expected is type(None):
            if self._unwrap_candidate_value(value=value) is None:
                return None

            raise TypeError(f'UnionValueObject value <<<{value}>>> must be of type <<<None>>> type. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

        candidate_value = self._unwrap_candidate_value(value=value, unwrap_enum=False)

        if not isclass(object=expected):
            if matches_expected_type(value=candidate_value, expected_type=expected):
                return candidate_value

            raise TypeError(f'UnionValueObject value <<<{candidate_value}>>> must be of type <<<{self._format_single_type(type=expected_type)}>>> type. Got <<<{type(candidate_value).__name__}>>> type.')  # noqa: E501  # fmt: skip

        if issubclass(expected, ValueObject):
            converted_value = from_primitive(
                value=self._unwrap_candidate_value(value=candidate_value, unwrap_enum=False),
                expected_type=expected,
            )
            if isinstance(converted_value, expected):
                return converted_value

            raise TypeError(f'UnionValueObject value <<<{converted_value}>>> must be of type <<<{expected.__name__}>>> type. Got <<<{type(converted_value).__name__}>>> type.')  # noqa: E501  # fmt: skip

        if issubclass(expected, BaseModel):
            model_source = self._unwrap_candidate_value(value=candidate_value, unwrap_enum=False)
            converted_value = from_primitive(value=model_source, expected_type=expected)
            if isinstance(converted_value, expected):
                return converted_value

            raise TypeError(f'UnionValueObject value <<<{model_source}>>> must be of type <<<{expected.__name__}>>> type. Got <<<{type(model_source).__name__}>>> type.')  # noqa: E501  # fmt: skip

        if issubclass(expected, Enum):
            enum_source = self._unwrap_candidate_value(value=candidate_value, unwrap_enum=False)
            converted_value = from_primitive(value=enum_source, expected_type=expected)
            if isinstance(converted_value, expected):
                return converted_value

            raise TypeError(f'UnionValueObject value <<<{enum_source}>>> must be of type <<<{expected.__name__}>>> type. Got <<<{type(enum_source).__name__}>>> type.')  # noqa: E501  # fmt: skip

        primitive_source = self._unwrap_candidate_value(value=candidate_value)
        if matches_expected_type(value=primitive_source, expected_type=expected):
            return primitive_source

        raise TypeError(f'UnionValueObject value <<<{primitive_source}>>> must be of type <<<{expected.__name__}>>> type. Got <<<{type(primitive_source).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def _raise_value_is_not_of_type(self, value: Any) -> NoReturn:
        """
        Raises TypeError when the value does not match any allowed union candidate.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the value does not match any allowed union candidate.
        """
        raise TypeError(f'UnionValueObject value <<<{value}>>> must be of type <<<{self._type_label()}>>> type. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    def _type_label(self) -> str:
        """
        Returns a readable label for the configured type, including unions.

        Returns:
            str: The type label.
        """
        origin = get_origin(tp=self._type)
        if origin in (Union, UnionType):
            parts = [self._format_single_type(type=allowed) for allowed in get_args(self._type)]
            return ' | '.join(parts)

        return self._format_single_type(type=self._type)

    def _format_single_type(self, *, type: Any) -> str:
        """
        Formats a single type for error messages.

        Args:
            type (Any): The type to format.

        Returns:
            str: The formatted type.
        """
        if type is Any:
            return 'Any'

        if hasattr(type, '__name__'):
            return type.__name__  # type: ignore[no-any-return]

        return str(type).replace('typing.', '')

    @classmethod
    def from_primitives(cls, value: Any) -> Self:
        """
        Creates the value object from primitives.

        Args:
            value (Any): Primitive value.

        Returns:
            Self: The created value object.
        """
        return cls(value=from_primitive(value=value, expected_type=cls._type))
