"""
Value object generic type.
"""

from abc import ABC
from collections import deque
from sys import version_info
from typing import Any, Callable, Generic, NoReturn, TypeVar

if version_info >= (3, 12):
    from typing import override  # pragma: no cover
else:
    from typing_extensions import override  # pragma: no cover

T = TypeVar('T')


class ValueObject(ABC, Generic[T]):  # noqa: UP046
    """
    ValueObject generic type.

    Example:
    ```python
    from value_object_pattern import ValueObject


    class IntegerValueObject(ValueObject[int]):
        pass


    integer = IntegerValueObject(value=10)
    print(repr(integer))
    # >>> IntegerValueObject(value=10)
    ```
    """

    __slots__ = ('_parameter', '_title', '_value')
    __match_args__ = ('_parameter', '_title', '_value')

    _value: T
    _title: str
    _parameter: str

    def __init__(self, *, value: T, title: str | None = None, parameter: str | None = None) -> None:
        """
        ValueObject value object constructor.

        Args:
            value (T): The value to store in the value object.
            title (str | None, optional): The title of the value object when raising exceptions, if title is None, the
            class name is used instead. Defaults to None.
            parameter (str | None, optional): The parameter name of the value object when raising exceptions, if
            parameter is None, the string "value" is used instead. Defaults to None.

        Raises:
            TypeError: If the title is not a string.
            ValueError: If the title is an empty string.
            ValueError: If the title contains leading or trailing whitespaces.
            TypeError: If the parameter is not a string.
            ValueError: If the parameter is an empty string.
            ValueError: If the parameter contains leading or trailing whitespaces.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(repr(integer))
        # >>> IntegerValueObject(value=10)
        ```
        """
        if title is None:
            title = self.__class__.__name__

        if type(title) is not str:
            raise TypeError(f'ValueObject title <<<{title}>>> must be a string. Got <<<{type(title).__name__}>>> instead.')  # noqa: E501  # fmt: skip

        if title == '':
            raise ValueError(f'ValueObject title <<<{title}>>> must not be an empty string.')  # noqa: E501  # fmt: skip

        if title.strip() != title:
            raise ValueError(f'ValueObject title <<<{title}>>> contains leading or trailing whitespaces. Only trimmed values are allowed.')  # noqa: E501  # fmt: skip

        if parameter is None:
            parameter = 'value'

        if type(parameter) is not str:
            raise TypeError(f'ValueObject parameter <<<{parameter}>>> must be a string. Got <<<{type(parameter).__name__}>>> instead.')  # noqa: E501  # fmt: skip

        if parameter == '':
            raise ValueError(f'ValueObject parameter <<<{parameter}>>> must not be an empty string.')  # noqa: E501  # fmt: skip

        if parameter.strip() != parameter:
            raise ValueError(f'ValueObject parameter <<<{parameter}>>> contains leading or trailing whitespaces. Only trimmed values are allowed.')  # noqa: E501  # fmt: skip

        object.__setattr__(self, '_title', title)
        object.__setattr__(self, '_parameter', parameter)

        self._validate(value=value)
        value = self._process(value=value)

        object.__setattr__(self, '_value', value)

    @override
    def __repr__(self) -> str:
        """
        Returns a detailed string representation of the value object.

        Returns:
            str: A string representation of the value object in the format 'ClassName(value=value)'.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(repr(integer))
        # >>> IntegerValueObject(value=10)
        ```
        """
        return f'{self.__class__.__name__}(value={self._value!s})'

    @override
    def __str__(self) -> str:
        """
        Returns a simple string representation of the value object.

        Returns:
            str: The string representation of the value object value.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer)
        # >>> 10
        ```
        """
        return str(object=self._value)

    @override
    def __hash__(self) -> int:
        """
        Returns the hash of the value object.

        Returns:
            int: Hash of the value object.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(hash(integer))
        # >>> 10
        ```
        """
        return hash(self._value)

    @override
    def __eq__(self, other: object) -> bool:
        """
        Check if the value object is equal to another value object.

        Args:
            other (object): Object to compare.

        Returns:
            bool: True if both objects are equal, otherwise False.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer_a = IntegerValueObject(value=10)
        integer_b = IntegerValueObject(value=16)
        print(integer_a == integer_b)
        # >>> False
        ```
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._value == other.value

    @override
    def __setattr__(self, key: str, value: T) -> NoReturn:
        """
        Prevents modification or addition of attributes in the value object.

        Args:
            key (str): The name of the attribute.
            value (T): The value to be assigned to the attribute.

        Raises:
            AttributeError: If there is an attempt to modify an existing attribute.
            AttributeError: If there is an attempt to add a new attribute.
        """
        public_key = key.replace('_', '')
        public_slots1 = [slot.replace('_', '') for slot in self.__slots__]

        if key in self.__slots__:
            raise AttributeError(f'Cannot modify attribute "{key}" of immutable instance.')

        if public_key in public_slots1:
            raise AttributeError(f'Cannot modify attribute "{public_key}" of immutable instance.')

        raise AttributeError(f'{self.__class__.__name__} object has no attribute "{key}".')

    def _process(self, value: T) -> T:
        """
        This method processes the value object value after validation. It ensure that the value object is stored in the
        correct format, by executing all methods with the `@process` decorator.

        Args:
            value (T): The value object value.

        Returns:
            T: The processed value object value.
        """
        methods = self._gather_decorated_methods(instance=self, attribute_name='_is_process')
        while methods:
            method: Callable[..., T] = methods.popleft().__get__(self, self.__class__)
            value = method(value=value)

        return value

    def _validate(self, value: T) -> None:
        """
        This method validates that the value follows the domain rules, by executing all methods with the `@validation`
        decorator.

        Args:
            value (T): The value object value.
        """
        try:
            methods = self._gather_decorated_methods(instance=self, attribute_name='_is_validation')
            while methods:
                method: Callable[..., T] = methods.popleft().__get__(self, self.__class__)
                method(value=value)

        except Exception as error:
            classes = self._post_order_dfs_mro(cls=self.__class__, cut_off=ValueObject)
            for class_name in {cls.__name__ for cls in classes}:
                error.args = (str(object=error.args[0]).replace(class_name, self.title),)

            error.args = (str(object=error.args[0]).replace('value', self.parameter, 1),)

            raise error

    def _post_order_dfs_mro(self, cls: type, visited: set[type] | None = None, cut_off: type = object) -> list[type]:
        """
        Computes the Post-Order Depth-First Search (DFS) Method Resolution Order (MRO) of a class.

        Args:
            cls (type): The class to process.
            visited (set[type] | None, optional): A set of already visited classes (to prevent duplicates). Defaults
            to None.
            cut_off (type, optional): The class to stop the search. Defaults to object.

        Returns:
            list[type]: A list of classes type sorted by post-order DFS MRO.

        References:
            DFS: https://en.wikipedia.org/wiki/Depth-first_search
            MRO: https://docs.python.org/3/howto/mro.html
        """
        if cls is cut_off:
            return []

        if visited is None:
            visited = set()

        result = []
        for parent in cls.__bases__:
            if parent not in visited and parent is not object:  # pragma: no cover
                result.extend(self._post_order_dfs_mro(cls=parent, visited=visited, cut_off=cut_off))

        if cls not in visited:  # pragma: no cover
            visited.add(cls)
            result.append(cls)

        return result

    def _gather_decorated_methods(self, instance: object, attribute_name: str) -> deque[Callable[..., Any]]:
        """
        Gathers decorated methods from instance.__class__ and its parent classes following the post-order DFS MRO,
        returning them in a deque with the methods sorted by class hierarchy, method order, and method name.

        Args:
            instance (object): The object instance whose class hierarchy is inspected.
            attribute_name (str): The attribute name used to identify the methods.

        Returns
            deque[Callable[..., Any]]: A deque of methods sorted by class hierarchy, method order, and method name.

        References:
            DFS: https://en.wikipedia.org/wiki/Depth-first_search
            MRO: https://docs.python.org/3/howto/mro.html
        """

        def sort_key(item: tuple[str, str, Callable[..., Any]]) -> tuple[int, str, str]:
            """
            Sorts the methods by class hierarchy, method order attribute, and method name.
            The only global variable used is classes_names.

            Args:
                item (tuple[str, str, Callable[..., Any]]): The item to sort.

            Returns:
                tuple[int, str, str]: A tuple with the class index, method order, and method name.
            """
            class_name, method_name, method = item
            class_index = classes_names.get(class_name, 999)
            order = getattr(method, '_order', method_name)

            return int(class_index), order, method_name

        classes = self._post_order_dfs_mro(cls=instance.__class__, cut_off=ValueObject)
        classes_names = {cls.__name__: index for index, cls in enumerate(iterable=classes)}

        classes_methods: deque[tuple[str, str, Callable[..., Any]]] = deque()
        for cls in classes:
            for method_name, method in cls.__dict__.items():
                if not callable(method):
                    continue

                if not getattr(method, attribute_name, False):
                    continue  # only methods with the attribute

                classes_methods.append((method.__qualname__.split('.')[0], method_name, method))

        # sort by class hierarchy, method order attribute, and method name
        return deque([method for _, _, method in sorted(classes_methods, key=sort_key)])

    @property
    def value(self) -> T:
        """
        Returns the value object value.

        Returns:
            T: The value object value.

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
        return self._value

    @property
    def title(self) -> str:
        """
        Returns the value object title.

        Returns:
            str: The value object title.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer.title)
        # >>> IntegerValueObject
        ```
        """
        return self._title

    @property
    def parameter(self) -> str:
        """
        Returns the value object parameter name.

        Returns:
            str: The value object parameter name.

        Example:
        ```python
        from value_object_pattern import ValueObject


        class IntegerValueObject(ValueObject[int]):
            pass


        integer = IntegerValueObject(value=10)
        print(integer.parameter)
        # >>> value
        ```
        """
        return self._parameter
