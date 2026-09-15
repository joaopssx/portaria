from models.person import Person


class Visitor(Person):
    """Um visitante e uma Pessoa entrando no condominio de forma temporaria."""

    def __init__(self, name: str, cpf: str, license_plate: str = ""):
        super().__init__(name, cpf)
        self._license_plate = license_plate

    @property
    def license_plate(self) -> str:
        return self._license_plate

    def describe(self) -> str:
        base_info = super().describe()
        if self._license_plate:
            return f"{base_info} - Visitante, veiculo placa {self._license_plate}"
        return f"{base_info} - Visitante, sem veiculo"
