"""
CarPlateValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .plates import (
    AgriculturalPlateValueObject,
    AirForcePlateValueObject,
    ArmyPlateValueObject,
    CatalanPolicePlateValueObject,
    CivilGuardPlateValueObject,
    NationalPolicePlateValueObject,
    NavyPlateValueObject,
    OrdinaryPlateValueObject,
)


class CarPlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    CarPlateValueObject value object ensures the provided value is a valid Spanish car plate.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.countries.spain import CarPlateValueObject

    plate = CarPlateValueObject(value='1234-BCD')

    print(repr(plate))
    # >>> CarPlateValueObject(value=1234-BCD)
    ```
    """

    __CAR_PLATE_VALUE_OBJECT_VARIATIONS: tuple[type[ValueObject[str]], ...] = (
        AgriculturalPlateValueObject,
        ArmyPlateValueObject,
        AirForcePlateValueObject,
        CatalanPolicePlateValueObject,
        CivilGuardPlateValueObject,
        NationalPolicePlateValueObject,
        NavyPlateValueObject,
        OrdinaryPlateValueObject,
    )

    @process(order=0)
    def _ensure_value_is_upper(self, value: str) -> str:  # type: ignore[return]
        """
        Ensures the value object `value` is an upper string.

        Args:
            value (str): The provided value.

        Returns:
            str: Upper case value.
        """
        for variation in self.__CAR_PLATE_VALUE_OBJECT_VARIATIONS:
            try:
                return variation(value=value).value

            except Exception:  # noqa: S112
                continue

    @validation(order=0)
    def _ensure_value_is_spanish_car_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish car plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish car plate.
        """
        for variation in self.__CAR_PLATE_VALUE_OBJECT_VARIATIONS:
            try:
                variation(value=value)
                return

            except Exception:  # noqa: S112
                continue

        self._raise_value_is_not_spanish_car_plate(value=value)

    def _raise_value_is_not_spanish_car_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish car plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish car plate.
        """
        raise ValueError(f'CarPlateValueObject value <<<{value}>>> is not a valid Spanish car plate.')
