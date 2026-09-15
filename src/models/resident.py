from models.person import Person
from models.unit import Unit


class Resident(Person):
    """Um morador e uma Pessoa vinculada a uma Unidade."""

    def __init__(self, name: str, cpf: str, unit: Unit):
        super().__init__(name, cpf)
        self._unit = unit
        self._unit.add_resident(self)

    @property
    def unit(self) -> Unit:
        return self._unit

    def describe(self) -> str:
        base_info = super().describe()
        return f"{base_info} - Morador do {self._unit.describe()}"
