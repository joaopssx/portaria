"""Entregador: um caso especifico de visitante."""

from models.vehicle import Vehicle
from models.visitor import Visitor


class DeliveryPerson(Visitor):
    """Um entregador e um Visitante que traz uma encomenda de uma empresa.

    Herda de Visitor (e nao de Person), formando uma cadeia de tres niveis:
    Person -> Visitor -> DeliveryPerson.
    """

    def __init__(self, name: str, cpf: str, company: str, vehicle: Vehicle = None):
        super().__init__(name, cpf, vehicle)
        self._company = company.strip()

    @property
    def company(self) -> str:
        return self._company

    def describe(self) -> str:
        return f"{super().describe()} - Entregador da {self._company}"

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["company"] = self._company
        return dados
