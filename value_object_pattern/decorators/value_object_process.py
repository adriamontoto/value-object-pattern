"""
Decorator used to register value-object processing hooks.
"""

from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T')


def process(order: int | None = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Register a method that normalizes a value after validation.

    Processing methods run in ascending `order`. Methods without an explicit order are ordered by method name. Each
    processing method receives the current value and returns the value passed to the next processor.

    Args:
        order: Execution order for the processing method.

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
        Mark `function` as a processing hook.

        Args:
            function: Processing method to register.

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

        @wraps(function)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> T:
            """
            Execute the wrapped processing method.

            Args:
                *args (tuple[Any, ...]): The arguments for the function.
                **kwargs (dict[str, Any]): The keyword arguments for the function.

            Returns:
                T: The return value of the function.
            """
            return function(*args, **kwargs)

        return wrapper

    return decorator
