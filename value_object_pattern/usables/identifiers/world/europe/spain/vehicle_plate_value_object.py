"""
VehiclePlateValueObject value object.
"""

from typing import NoReturn

from value_object_pattern.decorators import process, validation
from value_object_pattern.models.value_object import ValueObject
from value_object_pattern.usables import NotEmptyStringValueObject, TrimmedStringValueObject

from .plates import (
    AdministrativeTechnicianVehiclePlateValueObject,
    AirForceVehiclePlateValueObject,
    ArmyVehiclePlateValueObject,
    CanariasPoliceVehiclePlateValueObject,
    CatalanPoliceVehiclePlateValueObject,
    CivilGuardVehiclePlateValueObject,
    ConsularCorpsVehiclePlateValueObject,
    DiplomaticCorpsVehiclePlateValueObject,
    EspecialVehiclePlateValueObject,
    HistoricalVehiclePlateValueObject,
    InternationalOrganizationVehiclePlateValueObject,
    MinistryDevelopmentVehiclePlateValueObject,
    MinistryEnvironmentVehiclePlateValueObject,
    NationalPoliceVehiclePlateValueObject,
    NavyVehiclePlateValueObject,
    OrdinaryTruckVehiclePlateValueObject,
    OrdinaryVehiclePlateValueObject,
    ProvincialSystemVehiclePlateValueObject,
    StateMotorPoolVehiclePlateValueObject,
    TemporalCompanyNotRegisteredVehiclePlateValueObject,
    TemporalCompanyRegisteredVehiclePlateValueObject,
    TemporalPrivateIndividualVehiclePlateValueObject,
    TwoWheelsVehiclePlateValueObject,
)


class VehiclePlateValueObject(NotEmptyStringValueObject, TrimmedStringValueObject):
    """
    VehiclePlateValueObject value object ensures the provided value is a valid Spanish vehicle plate.

    References:
        Plates: https://matriculasdelmundo.com/espana.html

    Example:
    ```python
    from value_object_pattern.usables.identifiers.world.europe.spain import VehiclePlateValueObject

    plate = VehiclePlateValueObject(value='1234-BCD')

    print(repr(plate))
    # >>> VehiclePlateValueObject(value=1234-BCD)
    ```
    """

    _VEHICLE_PLATE_VARIATIONS: tuple[type[ValueObject[str]], ...] = (
        AdministrativeTechnicianVehiclePlateValueObject,
        AirForceVehiclePlateValueObject,
        ArmyVehiclePlateValueObject,
        CanariasPoliceVehiclePlateValueObject,
        CatalanPoliceVehiclePlateValueObject,
        CivilGuardVehiclePlateValueObject,
        ConsularCorpsVehiclePlateValueObject,
        DiplomaticCorpsVehiclePlateValueObject,
        EspecialVehiclePlateValueObject,
        HistoricalVehiclePlateValueObject,
        InternationalOrganizationVehiclePlateValueObject,
        MinistryDevelopmentVehiclePlateValueObject,
        MinistryEnvironmentVehiclePlateValueObject,
        NationalPoliceVehiclePlateValueObject,
        NavyVehiclePlateValueObject,
        OrdinaryVehiclePlateValueObject,
        OrdinaryTruckVehiclePlateValueObject,
        ProvincialSystemVehiclePlateValueObject,
        StateMotorPoolVehiclePlateValueObject,
        TemporalCompanyNotRegisteredVehiclePlateValueObject,
        TemporalCompanyRegisteredVehiclePlateValueObject,
        TemporalPrivateIndividualVehiclePlateValueObject,
        TwoWheelsVehiclePlateValueObject,
    )

    @process(order=0)
    def _ensure_value_is_formatted(self, value: str) -> str:  # type: ignore[return]
        """
        Ensures the value object `value` is stored without separators.

        Args:
            value (str): The provided value.

        Returns:
            str: Formatted value.
        """
        for variation in self._VEHICLE_PLATE_VARIATIONS:
            try:
                return variation(value=value).value

            except Exception:  # noqa: S112
                continue

    @validation(order=0)
    def _ensure_value_is_spanish_vehicle_plate(self, value: str) -> None:
        """
        Ensures the value object `value` is a valid Spanish vehicle plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish vehicle plate.
        """
        for variation in self._VEHICLE_PLATE_VARIATIONS:
            try:
                variation(value=value)
                return

            except Exception:  # noqa: S112
                continue

        self._raise_value_is_not_spanish_vehicle_plate(value=value)

    def _raise_value_is_not_spanish_vehicle_plate(self, value: str) -> NoReturn:
        """
        Raises a ValueError if the value object `value` is not a valid Spanish vehicle plate.

        Args:
            value (str): The provided value.

        Raises:
            ValueError: If the `value` is not a valid Spanish vehicle plate.
        """
        raise ValueError(f'VehiclePlateValueObject value <<<{value}>>> is not a valid Spanish vehicle plate.')
