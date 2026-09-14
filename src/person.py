class Person:
    """Base class for anyone registered in the condominium system."""

    def __init__(self, name: str, cpf: str):
        self._name = name
        self._cpf = cpf

    @property
    def name(self) -> str:
        return self._name

    @property
    def cpf(self) -> str:
        return self._cpf

    def describe(self) -> str:
        return f"{self._name} (CPF: {self._cpf})"
