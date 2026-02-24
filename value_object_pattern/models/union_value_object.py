"""
UnionValueObject module.
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
from typing import Any, Generic, NoReturn, Self, TypeVar, Union, get_args, get_origin

from value_object_pattern.decorators import process, validation

from .base_model import BaseModel
from .primitive_conversion import from_primitive
from .type_matching import matches_expected_type
from .value_object import ValueObject

T = TypeVar('T', bound=Any)


class UnionValueObject(ValueObject[T], Generic[T]):  # noqa: UP046
    """
    UnionValueObject validates and stores the value as one of the allowed union candidates.

    It supports primitives, ValueObject subclasses, BaseModel subclasses, Enum subclasses,
    and combinations of all of them.

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

    @override
    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initializes the class.

        Args:
            **kwargs (Any): Keyword arguments.

        Raises:
            TypeError: If the class parameter is not a type.
            TypeError: If the class is not parameterized.
        """
        super().__init_subclass__(**kwargs)

        for base in getattr(cls, '__orig_bases__', ()):
            if get_origin(tp=base) is UnionValueObject:
                _type, *_ = get_args(tp=base)

                if isinstance(_type, TypeVar):
                    cls._type = _type  # type: ignore[assignment]
                    return

                if type(_type) is not type and not isclass(object=_type) and get_origin(tp=_type) is None:
                    raise TypeError(f'UnionValueObject[...] <<<{_type}>>> must be a type. Got <<<{type(_type).__name__}>>> type.')  # noqa: E501  # fmt: skip

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
