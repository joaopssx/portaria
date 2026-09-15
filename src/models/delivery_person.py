from models.visitor import Visitor


class DeliveryPerson(Visitor):
    """Um entregador e um Visitante que traz uma encomenda de uma empresa."""

    def __init__(self, name: str, cpf: str, company: str, license_plate: str = ""):
        super().__init__(name, cpf, license_plate)
        self._company = company

    @property
    def company(self) -> str:
        return self._company

    def describe(self) -> str:
        base_info = super().describe()
        return f"{base_info} - Entregador da {self._company}"
