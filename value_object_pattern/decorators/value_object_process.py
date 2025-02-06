"""
Process decorator for value object pattern.
"""

from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T')


def process(order: int | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for process the value after the value is validated.

    Args:
        order (int | None, optional): The order of the process that will be executed, if None the functions will be
        executed alphabetically. Defaults to None.

    Raises:
        TypeError: If the order is not an integer.
        ValueError: If the order is not equal or greater than 0.

    Returns:
        Callable[[Callable[..., T]], Callable[..., T]]: Wrapper function for the process.

    Example:
    ```python
    from value_object_pattern import ValueObject, process


    class UpperStringValueObject(ValueObject[str]):
        @process()
        def ensure_value_is_upper(self, value: str) -> str:
            return value.upper()


    string = UpperStringValueObject(value='hello world')
    print(string)
    # >>> HELLO WORLD
    ```
    """

    def decorator(function: Callable[..., T]) -> Callable[..., T]:
        """
        Decorator for process the value after the value is validated.

        Args:
            function (Callable[..., T]): Function to be execution after the value object is validated.

        Raises:
            TypeError: If the order is not an integer.
            ValueError: If the order is not equal or greater than 0.

        Returns:
            Callable[..., T]: Wrapper function for the process.
        """
        if order is not None:
            if type(order) is not int:
                raise TypeError(f'Process order <<<{order}>>> must be an integer. Got <<<{type(order).__name__}>>> type.')  # noqa: E501  # fmt: skip

            if order < 0:
                raise ValueError(f'Process order <<<{order}>>> must be equal or greater than 0.')

        function._is_process = True  # type: ignore[attr-defined]
        function._order = function.__name__ if order is None else str(order)  # type: ignore[attr-defined]

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
            """
            Wrapper for process.

            Args:
                *args (tuple[Any, ...]): The arguments for the function.
                **kwargs (dict[str, Any]): The keyword arguments for the function.

            Returns:
                T: The return value of the function.
            """
            return function(*args, **kwargs)

        return wrapper

    return decorator
