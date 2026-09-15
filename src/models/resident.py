from models.person import Person
from models.unit import Unit
from models.vehicle import Vehicle


class Resident(Person):
    """Um morador e uma Pessoa vinculada a uma Unidade."""

    def __init__(self, name: str, cpf: str, unit: Unit, vehicle: Vehicle = None):
        super().__init__(name, cpf)
        self._unit = unit
        self._unit.add_resident(self)
        self._vehicle = vehicle

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    def describe(self) -> str:
        base_info = super().describe()
        info = f"{base_info} - Morador do {self._unit.describe()}"
        if self._vehicle:
            info += f", veiculo {self._vehicle.describe()}"
        return info
