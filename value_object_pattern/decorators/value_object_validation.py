"""
Validation decorator for value object pattern.
"""

from functools import wraps
from typing import Any, Callable


def validation(order: int | None = None) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Decorator for validation the value before the value is created.

    Args:
        order (int | None, optional): The order of the validation that will be executed, if None the functions will be
        executed alphabetically. Defaults to None.

    Raises:
        TypeError: If the order is not an integer.
        ValueError: If the order is not equal or greater than 0.

    Returns:
        Callable[[Callable[..., None]], Callable[..., None]]: Wrapper function for the validation.

    Example:
    ```python
    from value_object_pattern import ValueObject, validation


    class IntegerValueObject(ValueObject[int]):
        @validation()
        def ensure_value_is_integer(self, value: int) -> None:
            if type(value) is not int:
                raise TypeError(f'IntegerValueObject value <<<{value}>>> must be an integer. Got <<<{type(value).__name__}>>> type.')


    integer = IntegerValueObject(value='invalid')
    # >>> TypeError: IntegerValueObject value <<<invalid>>> must be an integer. Got <<<str>>> type.
    ```
    """  # noqa: E501 # fmt: skip

    def decorator(function: Callable[..., None]) -> Callable[..., None]:
        """
        Decorator for validation the value before the value is created.

        Args:
            function (Callable[..., None]): Function to be execution before the value object is created.

        Raises:
            TypeError: If the order is not an integer.
            ValueError: If the order is not equal or greater than 0.

        Returns:
            Callable[..., None]: Wrapper function for the validation.
        """
        if order is not None:
            if type(order) is not int:
                raise TypeError(f'Validation order <<<{order}>>> must be an integer. Got <<<{type(order).__name__}>>> type.')  # noqa: E501  # fmt: skip

            if order < 0:
                raise ValueError(f'Validation order <<<{order}>>> must be equal or greater than 0.')

        function._is_validation = True  # type: ignore[attr-defined]
        function._order = function.__name__ if order is None else str(order)  # type: ignore[attr-defined]

        @wraps(wrapped=function)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
            """
            Wrapper for validation.

            Args:
                *args (tuple[Any, ...]): The arguments for the function.
                **kwargs (dict[str, Any]): The keyword arguments for the function.
            """
            function(*args, **kwargs)

        return wrapper

    return decorator
