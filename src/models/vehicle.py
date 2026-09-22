"""Veiculo associado a uma pessoa."""

from errors import InvalidPlateError


class Vehicle:
    """Um veiculo, com placa, modelo e cor."""

    def __init__(self, plate: str, model: str = "", color: str = ""):
        self.plate = plate
        self._model = model.strip()
        self._color = color.strip()

    @property
    def plate(self) -> str:
        return self._plate

    @plate.setter
    def plate(self, value: str) -> None:
        value = (value or "").strip().upper().replace("-", "")
        if not self.is_valid_plate(value):
            raise InvalidPlateError(f"Placa invalida: {value}")
        self._plate = value

    @property
    def model(self) -> str:
        return self._model

    @property
    def color(self) -> str:
        return self._color

    @staticmethod
    def is_valid_plate(plate: str) -> bool:
        """Aceita o padrao antigo (ABC1234) e o Mercosul (ABC1D23)."""
        if len(plate) != 7:
            return False
        if not plate[:3].isalpha() or not plate[3].isdigit():
            return False
        if plate[4].isalpha():  # Mercosul: ABC1D23
            return plate[5:].isdigit()
        return plate[4:].isdigit()  # antigo: ABC1234

    def describe(self) -> str:
        detalhes = " ".join(p for p in (self._color, self._model) if p)
        if detalhes:
            return f"{detalhes}, placa {self._plate}"
        return f"placa {self._plate}"

    def to_dict(self) -> dict:
        return {"plate": self._plate, "model": self._model, "color": self._color}

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"Vehicle(plate={self._plate!r}, model={self._model!r}, color={self._color!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self._plate == other._plate
