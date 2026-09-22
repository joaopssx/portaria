"""Visitante do condominio."""

from models.person import Person
from models.vehicle import Vehicle


class Visitor(Person):
    """Um visitante e uma Pessoa entrando no condominio de forma temporaria."""

    def __init__(self, name: str, cpf: str, vehicle: Vehicle = None):
        super().__init__(name, cpf)
        self._vehicle = vehicle

    @property
    def vehicle(self) -> Vehicle:
        return self._vehicle

    def describe(self) -> str:
        base_info = super().describe()
        if self._vehicle:
            return f"{base_info} - Visitante, veiculo {self._vehicle.describe()}"
        return f"{base_info} - Visitante, sem veiculo"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["plate"] = self._vehicle.plate if self._vehicle else ""
        dados["model"] = self._vehicle.model if self._vehicle else ""
        dados["color"] = self._vehicle.color if self._vehicle else ""
        return dados
