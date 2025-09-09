"""
classproperty module.
"""

from __future__ import annotations

from contextlib import suppress as suppress_exception
from typing import Any, Callable


class classproperty:  # noqa: N801
    """
    A read-only descriptor that behaves like @property but for classes.

    Example:
    ```python
    from value_object_pattern.decorators import classproperty


    class Foo:
        _name = 'foo'

        @classproperty
        def name(cls) -> str:
            return cls._name


    print(Foo.name, Foo().name)
    # >>> foo foo
    ```
    """

    def __init__(self, function: Callable[[Any], str]) -> None:
        """
        Initialize a classproperty.

        Args:
            function (Callable[[Any], str]): The getter function for the property.

        Raises:
            TypeError: If `function` is not callable.
        """
        if not callable(function):
            raise TypeError(f'Wrapped function must be callable. Got <<<{type(function).__name__}>>> instead.')

        self._function = function

        with suppress_exception(AttributeError):
            self.__doc__ = getattr(function, '__doc__', None)

    def __get__(self, obj: Any, owner: type) -> str:
        """
        Get the value of the class property.

        Args:
            obj (Any): The instance of the class (ignored).
            owner (type): The class itself.

        Returns:
            str: The value of the class property.
        """
        return self._function(owner)
