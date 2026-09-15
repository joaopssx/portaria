from models.visitor import Visitor
from models.vehicle import Vehicle


class DeliveryPerson(Visitor):
    """Um entregador e um Visitante que traz uma encomenda de uma empresa."""

    def __init__(self, name: str, cpf: str, company: str, vehicle: Vehicle = None):
        super().__init__(name, cpf, vehicle)
        self._company = company

    @property
    def company(self) -> str:
        return self._company

    def describe(self) -> str:
        base_info = super().describe()
        return f"{base_info} - Entregador da {self._company}"
