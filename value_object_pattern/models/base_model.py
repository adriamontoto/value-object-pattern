"""
BaseModel module.
"""

from sys import version_info

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Self


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
        return cls(**primitives)

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
            if isinstance(value, BaseModel):
                value = value.to_primitives()

            elif isinstance(value, Enum):
                value = value.name

            elif hasattr(value, 'value'):
                value = value.value

                if isinstance(value, Enum):
                    value = value.name

            elif isinstance(value, primitive_types):  # noqa: SIM114
                pass

            elif isinstance(value, collection_types):
                pass

            else:
                value = str(value)

            dictionary[key] = value

        return dictionary
