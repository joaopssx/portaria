"""Funcionario do condominio."""

from config import TURNOS
from errors import InvalidShiftError
from models.person import Person


class Employee(Person):
    """Um funcionario e uma Pessoa que trabalha no condominio."""

    def __init__(self, name: str, cpf: str, role: str, shift: str):
        super().__init__(name, cpf)
        self._role = role.strip()
        self.shift = shift

    @property
    def role(self) -> str:
        return self._role

    @property
    def shift(self) -> str:
        return self._shift

    @shift.setter
    def shift(self, value: str) -> None:
        value = (value or "").strip().lower()
        if value not in TURNOS:
            raise InvalidShiftError(f"Turno invalido: {value}. Use um de {TURNOS}.")
        self._shift = value

    def describe(self) -> str:
        return f"{super().describe()} - Funcionario ({self._role}), turno da {self._shift}"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["role"] = self._role
        dados["shift"] = self._shift
        return dados
