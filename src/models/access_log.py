"""Registro de entrada e saida na portaria."""

from datetime import datetime

from models.person import Person
from models.unit import Unit

FORMATO = "%d/%m/%Y %H:%M"


class AccessLog:
    """Registro de um acesso: quem entrou, quando, para onde e quando saiu."""

    def __init__(self, person: Person, destination: Unit, entry_time: datetime = None):
        self._person = person
        self._destination = destination
        self._entry_time = entry_time or datetime.now()
        self._exit_time = None

    @property
    def person(self) -> Person:
        return self._person

    @property
    def destination(self) -> Unit:
        return self._destination

    @property
    def entry_time(self) -> datetime:
        return self._entry_time

    @property
    def exit_time(self):
        return self._exit_time

    @property
    def is_open(self) -> bool:
        """True enquanto a pessoa nao registrou a saida (ainda esta dentro)."""
        return self._exit_time is None

    def register_exit(self, exit_time: datetime = None) -> None:
        """Fecha o registro, marcando a hora da saida."""
        self._exit_time = exit_time or datetime.now()

    def duration_minutes(self) -> int:
        """Quantos minutos a pessoa ficou (calculado, nao armazenado)."""
        fim = self._exit_time or datetime.now()
        return int((fim - self._entry_time).total_seconds() // 60)

    def describe(self) -> str:
        entrada = self._entry_time.strftime(FORMATO)
        texto = f"{self._person.name} entrou em {entrada} - destino: {self._destination.describe()}"
        if self.is_open:
            return f"{texto} (ainda dentro, ha {self.duration_minutes()} min)"
        saida = self._exit_time.strftime(FORMATO)
        return f"{texto} - saiu em {saida} ({self.duration_minutes()} min)"

    def to_dict(self) -> dict:
        return {
            "cpf": self._person.cpf,
            "name": self._person.name,
            "unit_number": self._destination.number,
            "block": self._destination.block,
            "entry_time": self._entry_time.strftime(FORMATO),
            "exit_time": self._exit_time.strftime(FORMATO) if self._exit_time else "",
        }

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"AccessLog(person={self._person.name!r}, entry_time={self._entry_time!r})"

    def __lt__(self, other) -> bool:
        """Ordena os registros por horario de entrada."""
        if not isinstance(other, AccessLog):
            return NotImplemented
        return self._entry_time < other._entry_time
