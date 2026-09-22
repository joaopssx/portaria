"""Morador do condominio."""

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
        info = f"{super().describe()} - Morador do {self._unit.describe()}"
        if self._vehicle:
            info += f", veiculo {self._vehicle.describe()}"
        return info

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados.update(self._unit.to_dict())
        dados["plate"] = self._vehicle.plate if self._vehicle else ""
        dados["model"] = self._vehicle.model if self._vehicle else ""
        dados["color"] = self._vehicle.color if self._vehicle else ""
        return dados
