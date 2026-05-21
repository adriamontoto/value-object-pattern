"""
Decorator used to register value-object validation hooks.
"""

from functools import wraps
from typing import Any, Callable


def validation(
    order: int | None = None,
    early_process: bool = False,
) -> Callable[[Callable[..., None]], Callable[..., None]]:
    """
    Register a method that validates a value before it is stored.

    Validation methods run in ascending `order`. Methods without an explicit order are ordered by method name. When
    `early_process=True`, the value object processes the input first and passes both the raw value and the processed
    value to the validator.

    Args:
        order: Execution order for the validation method.
        early_process: Whether to pass a processed value into the validation method.

    Raises:
        TypeError: If the order is not an integer.
        ValueError: If the order is not equal or greater than 0.
        TypeError: If early_process is not a boolean.

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
        Mark `function` as a validation hook.

        Args:
            function: Validation method to register.

        Raises:
            TypeError: If the order is not an integer.
            ValueError: If the order is not equal or greater than 0.
            TypeError: If early_process is not a boolean.

        Returns:
            Callable[..., None]: Wrapper function for the validation.
        """
        if order is not None:
            if type(order) is not int:
                raise TypeError(f'Validation order <<<{order}>>> must be an integer. Got <<<{type(order).__name__}>>> type.')  # noqa: E501  # fmt: skip

            if order < 0:
                raise ValueError(f'Validation order <<<{order}>>> must be equal or greater than 0.')

        if type(early_process) is not bool:
            raise TypeError(f'Validation early_process <<<{early_process}>>> must be a boolean. Got <<<{type(early_process).__name__}>>> type.')  # noqa: E501  # fmt: skip

        function._is_validation = True  # type: ignore[attr-defined]
        function._order = function.__name__ if order is None else str(order)  # type: ignore[attr-defined]
        function._early_process = early_process  # type: ignore[attr-defined]

        @wraps(function)
        def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
            """
            Execute the wrapped validation method.

            Args:
                *args (tuple[Any, ...]): The arguments for the function.
                **kwargs (dict[str, Any]): The keyword arguments for the function.
            """
            function(*args, **kwargs)

        return wrapper

    return decorator
