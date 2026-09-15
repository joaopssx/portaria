class Unit:
    """Uma unidade (apartamento) de um bloco, com os moradores que vivem nela."""

    def __init__(self, number: str, block: str):
        self._number = number
        self._block = block
        self._residents = []

    @property
    def number(self) -> str:
        return self._number

    @property
    def block(self) -> str:
        return self._block

    @property
    def residents(self) -> list:
        return list(self._residents)

    def add_resident(self, resident) -> None:
        self._residents.append(resident)

    def describe(self) -> str:
        return f"bloco {self._block}, unidade {self._number}"
