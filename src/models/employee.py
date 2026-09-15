from models.person import Person


class Employee(Person):
    """Um funcionario e uma Pessoa que trabalha no condominio (porteiro, zelador, etc)."""

    def __init__(self, name: str, cpf: str, role: str, shift: str):
        super().__init__(name, cpf)
        self._role = role
        self._shift = shift

    @property
    def role(self) -> str:
        return self._role

    @property
    def shift(self) -> str:
        return self._shift

    def describe(self) -> str:
        base_info = super().describe()
        return f"{base_info} - Funcionario ({self._role}), turno da {self._shift}"
