"""
BaseModel module.
"""

from __future__ import annotations

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from abc import ABC, abstractmethod
from copy import deepcopy
from enum import Enum
from inspect import Parameter, _empty, signature
from typing import Any, NoReturn, Self

from .value_object import ValueObject


class BaseModel(ABC):
    """
    BaseModel class is a base class for all aggregate root classes.

    ***This class is abstract and should not be instantiated directly***.

    Example:
    ```python
    from datetime import datetime

    from value_object_pattern import BaseModel


    class User(BaseModel):
        name: str
        _birthdate: datetime
        __password: str

        def __init__(self, name: str, birthdate: datetime, password: str) -> None:
            self.name = name
            self.birthdate = birthdate
            self.__password = password


    user = User(name='John Doe', birthdate=datetime.now(), password='password')
    print(user)
    # >>> User(birthdate=1900-01-01T00:00:00+00:00, name=John Doe)
    ```
    """

    @abstractmethod
    def __init__(self) -> None:
        """
        Initialize the BaseModel class.

        ***This method is abstract and should be implemented by the child class***.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User(name='John Doe', birthdate=datetime.now(), password='password')
        print(user)
        # >>> User(birthdate=1900-01-01T00:00:00+00:00, name=John Doe)
        ```
        """

    @override
    def __repr__(self) -> str:
        """
        Returns the class representation as a string. Private attributes that start with "__" are not included, this
        can be used to hide sensitive information.

        Returns:
            str: String representation of the class.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User(name='John Doe', birthdate=datetime.now(), password='password')
        print(repr(user))
        # >>> User(birthdate=datetime.datetime(1900, 1, 1, 0, 0), name='John Doe')
        ```
        """
        attributes = []
        for key, value in sorted(self._to_dict(ignore_private=True).items()):
            attributes.append(f'{key}={value!r}')

        return f'{self.__class__.__name__}({", ".join(attributes)})'

    @override
    def __str__(self) -> str:
        """
        Returns the class string representation. Private attributes that start with "__" are not included, this can be
        used to hide sensitive information.

        Returns:
            str: String representation of the class.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User(name='John Doe', birthdate=datetime.now(), password='password')
        print(str(user))
        # >>> User(birthdate=1900-01-01T00:00:00+00:00, name=John Doe)
        ```
        """
        attributes = []
        for key, value in sorted(self.to_primitives().items()):
            attributes.append(f'{key}={value}')

        return f'{self.__class__.__name__}({", ".join(attributes)})'

    @override
    def __hash__(self) -> int:
        """
        Returns the hash of the class. Private attributes that start with "__" are not included, this can be used to
        hide sensitive information.

        Returns:
            int: Hash of the class.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User(name='John Doe', birthdate=datetime.now(), password='password')
        print(hash(user))
        # >>> 4606426846015488538
        ```
        """
        return hash(tuple(sorted(self._to_dict(ignore_private=True).items())))

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the class is equal to another object. Private attributes that start with "__" are not included, this
        can be used to hide sensitive information.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if the objects are equal, otherwise False.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        today = datetime.now()
        user = User(name='John Doe', birthdate=today, password='password')
        user_2 = User(name='John Doe', birthdate=today, password='another-password')
        print(user == user_2)
        # >>> True
        ```
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._to_dict(ignore_private=True) == other._to_dict(ignore_private=True)

    def __copy__(self) -> BaseModel:
        """
        Return a new instance of the same class, with all attributes copied.

        Returns:
            BaseModel: A shallow clone of the instance.

        Example:
        ```python
        # TODO:
        ```
        """
        cls = self.__class__
        clone = cls.__new__(cls)
        for key, value in self.__dict__.items():
            object.__setattr__(clone, key, value)

        return clone

    def __deepcopy__(self, memo: dict[int, Any]) -> BaseModel:
        """
        Return a deep clone, recursively copying the wrapped value.

        Args:
            memo (dict[str, Any]): Dictionary of id's to already copied objects to avoid infinite recursion.

        Returns:
            BaseModel: A deep clone of the instance.

        Example:
        ```python
        # TODO:
        ```
        """
        if id(self) in memo:
            return memo[id(self)]  # type: ignore[no-any-return]

        cls = self.__class__
        clone = cls.__new__(cls)
        memo[id(self)] = clone
        for key, value in self.__dict__.items():
            object.__setattr__(clone, key, deepcopy(value, memo))

        return clone

    def _to_dict(self, *, ignore_private: bool = True) -> dict[str, Any]:
        """
        Returns the class as a dictionary. The difference between this method and `to_primitives` is that this method
        does not convert attributes to primitives.

        ***This method is not intended to be used directly, use `to_primitives` instead.***

        Args:
            ignore_private (bool, optional): Whether to ignore private attributes (those that start with double
            underscore "__"). Defaults to True.

        Returns:
            dict[str, Any]: Dictionary representation of the class.
        """
        dictionary: dict[str, Any] = {}
        for key, value in self.__dict__.items():
            if ignore_private and key.startswith(f'_{self.__class__.__name__}__'):
                continue  # ignore private attributes

            key = key.replace(f'_{self.__class__.__name__}__', '')

            if key.startswith('_'):
                key = key[1:]

            dictionary[key] = value

        return dictionary

    @classmethod
    def from_primitives(cls, primitives: dict[str, Any]) -> Self:
        """
        Create an instance of the class with a dictionary of its primitives.

        Args:
            primitives (dict[str, Any]): Dictionary to create the instance from.

        Raises:
            TypeError: If the `primitives` is not a dictionary of strings.
            ValueError: If the `primitives` does not have all the required attributes.

        Returns:
            Self: Instance of the class.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User.from_primitives(primitives={'name': 'John Doe', 'birthdate': datetime.now(), 'password': 'password'})
        print(user.to_primitives())
        # >>> {'name': 'John Doe', 'birthdate': '1900-01-01T00:00:00+00:00'}
        ```
        """  # noqa: E501
        if not isinstance(primitives, dict) or not all(isinstance(key, str) for key in primitives):  # type: ignore[redundant-expr]
            cls._raise_value_is_not_dict_of_strings(value=primitives)

        constructor_signature = signature(obj=cls.__init__)
        parameters: dict[str, Parameter] = {parameter.name: parameter for parameter in constructor_signature.parameters.values() if parameter.name != 'self'}  # noqa: E501  # fmt: skip
        missing = {name for name, parameter in parameters.items() if parameter.default is _empty and name not in primitives}  # noqa: E501  # fmt: skip
        extra = set(primitives) - parameters.keys()

        if missing or extra:
            cls._raise_value_constructor_parameters_mismatch(primitives=set(primitives), missing=missing, extra=extra)

        return cls(**primitives)

    @classmethod
    def _raise_value_is_not_dict_of_strings(cls, value: Any) -> NoReturn:
        """
        Raises a TypeError if the value object `value` is not a dictionary of strings.

        Args:
            value (Any): The provided value.

        Raises:
            TypeError: If the `value` is not a dictionary of strings.
        """
        raise TypeError(f'{cls.__name__} primitives <<<{value}>>> must be a dictionary of strings. Got <<<{type(value).__name__}>>> type.')  # noqa: E501  # fmt: skip

    @classmethod
    def _raise_value_constructor_parameters_mismatch(
        cls,
        primitives: set[str],
        missing: set[str],
        extra: set[str],
    ) -> NoReturn:
        """
        Raises a ValueError if the value object constructor parameters do not match the provided primitives.

        Args:
            primitives (set[str]): Set of primitives keys. Only the keys are used to not expose private attributes.
            missing (set[str]): Set of missing parameters.
            extra (set[str]): Set of extra parameters.

        Raises:
            ValueError: If the constructor parameters do not match the provided primitives.
        """
        primitives_names = ', '.join(sorted(primitives))
        missing_names = ', '.join(sorted(missing))
        extra_names = ', '.join(sorted(extra))

        raise ValueError(f'{cls.__name__} primitives <<<{primitives_names}>>> must contain all constructor parameters. Missing parameters: <<<{missing_names}>> and extra parameters: <<<{extra_names}>>>.')  # noqa: E501  # fmt: skip

    def to_primitives(self) -> dict[str, Any]:
        """
        Returns the class as a dictionary of its primitives. Private attributes that start with "__" are not included,
        this can be used to hide sensitive information.

        Returns:
            dict[str, Any]: Primitives dictionary representation of the class.

        Example:
        ```python
        from datetime import datetime

        from value_object_pattern import BaseModel


        class User(BaseModel):
            name: str
            _birthdate: datetime
            __password: str

            def __init__(self, name: str, birthdate: datetime, password: str) -> None:
                self.name = name
                self.birthdate = birthdate
                self.__password = password


        user = User(name='John Doe', birthdate=datetime.now(), password='password')
        print(user.to_primitives())
        # >>> {'name': 'John Doe', 'birthdate': '1900-01-01T00:00:00+00:00'}
        ```
        """
        primitive_types: tuple[type, ...] = (int, float, str, bool, bytes, bytearray, memoryview, type(None))
        collection_types: tuple[type, ...] = (list, dict, tuple, set, frozenset)

        dictionary = self._to_dict(ignore_private=True)
        for key, value in dictionary.items():
            if isinstance(value, BaseModel) or hasattr(value, 'to_primitives'):
                value = value.to_primitives()

            elif isinstance(value, Enum):
                value = value.value

            elif isinstance(value, ValueObject) or hasattr(value, 'value'):
                value = value.value

                if isinstance(value, Enum):
                    value = value.value

            elif isinstance(value, primitive_types):  # noqa: SIM114
                pass

            elif isinstance(value, collection_types):
                pass

            else:
                value = str(object=value)

            dictionary[key] = value

        return dictionary
