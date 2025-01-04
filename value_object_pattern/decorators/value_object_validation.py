"""
Validation decorator for value object pattern.
"""

from functools import wraps
from typing import Any, Callable


def validation(function: Callable[..., Any]) -> Callable[..., None]:
    """
    Decorator for validation.

    Args:
        function (Callable[..., Any]): Function to be execution when the value object is created.

    Returns:
        Callable[..., None]: Wrapper function for the validation.

    Example:
    ```python
    from value_object_pattern import ValueObject, validation


    class IntegerValueObject(ValueObject[int]):
        @validation
        def ensure_value_is_integer(self, value: int) -> None:
            if type(value) is not int:
                raise TypeError(f'IntegerValueObject value <<<{value}>>> must be an integer. Got <<<{type(value).__name__}>>> type.')


    integer = IntegerValueObject(value='invalid')
    # >>> TypeError: IntegerValueObject value <<<invalid>>> must be an integer. Got <<<str>>> type.
    ```
    """  # noqa: E501 # fmt: skip
    function._is_validation = True  # type: ignore[attr-defined]

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
