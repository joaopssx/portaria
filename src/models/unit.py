"""Unidade (apartamento) do condominio."""


class Unit:
    """Uma unidade de um bloco, com os moradores que vivem nela.

    Implementa o protocolo de sequencia (__len__, __getitem__, __contains__),
    entao da para usar len(unidade), unidade[0] e "for morador in unidade"
    sem herdar de nada: basta ter os metodos que o Python espera.
    """

    def __init__(self, number: str, block: str):
        self._number = str(number).strip()
        self._block = str(block).strip().upper()
        self._residents = []

    @property
    def number(self) -> str:
        return self._number

    @property
    def block(self) -> str:
        return self._block

    @property
    def residents(self) -> list:
        # Devolve uma copia: ninguem de fora altera a lista interna direto.
        return list(self._residents)

    def add_resident(self, resident) -> None:
        if resident not in self._residents:
            self._residents.append(resident)

    def describe(self) -> str:
        return f"bloco {self._block}, unidade {self._number}"

    def to_dict(self) -> dict:
        return {"unit_number": self._number, "block": self._block}

    # --- Protocolo de sequencia ---

    def __len__(self) -> int:
        """len(unidade) devolve quantos moradores ela tem."""
        return len(self._residents)

    def __getitem__(self, index):
        """unidade[0] devolve o primeiro morador; tambem habilita o for."""
        return self._residents[index]

    def __contains__(self, resident) -> bool:
        """morador in unidade."""
        return resident in self._residents

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"Unit(number={self._number!r}, block={self._block!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Unit):
            return NotImplemented
        return (self._number, self._block) == (other._number, other._block)

    def __hash__(self) -> int:
        return hash((self._number, self._block))
