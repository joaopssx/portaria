class Vehicle:
    """Um veiculo, com placa, modelo e cor, associado a uma pessoa."""

    def __init__(self, plate: str, model: str = "", color: str = ""):
        self._plate = plate
        self._model = model
        self._color = color

    @property
    def plate(self) -> str:
        return self._plate

    @property
    def model(self) -> str:
        return self._model

    @property
    def color(self) -> str:
        return self._color

    def describe(self) -> str:
        details = " ".join(part for part in (self._color, self._model) if part)
        if details:
            return f"{details}, placa {self._plate}"
        return f"placa {self._plate}"
