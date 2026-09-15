from models.person import Person


class Resident(Person):
    """A resident is a Person linked to a specific unit and block."""

    def __init__(self, name: str, cpf: str, unit_number: str, block: str):
        super().__init__(name, cpf)
        self._unit_number = unit_number
        self._block = block

    @property
    def unit_number(self) -> str:
        return self._unit_number

    @property
    def block(self) -> str:
        return self._block

    def describe(self) -> str:
        base_info = super().describe()
        return f"{base_info} - Morador do bloco {self._block}, unidade {self._unit_number}"
