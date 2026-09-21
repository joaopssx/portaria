from datetime import datetime

from models.person import Person
from models.unit import Unit


class AccessLog:
    """Registro de uma entrada na portaria: quem entrou, quando e para onde."""

    def __init__(self, person: Person, destination: Unit, entry_time: datetime = None):
        self._person = person
        self._destination = destination
        self._entry_time = entry_time or datetime.now()

    @property
    def person(self) -> Person:
        return self._person

    @property
    def destination(self) -> Unit:
        return self._destination

    @property
    def entry_time(self) -> datetime:
        return self._entry_time

    def describe(self) -> str:
        when = self._entry_time.strftime("%d/%m/%Y %H:%M")
        return f"{self._person.name} entrou em {when} - destino: {self._destination.describe()}"
