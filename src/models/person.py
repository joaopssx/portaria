"""Classe base abstrata de todas as pessoas do sistema."""

from abc import ABCMeta, abstractmethod

from errors import EmptyNameError, InvalidCpfError


class Person(metaclass=ABCMeta):
    """Classe base abstrata para qualquer pessoa cadastrada no condominio.

    E abstrata porque "pessoa" sozinha nao existe na portaria: toda pessoa e
    um morador, um visitante, um entregador ou um funcionario. Tentar criar
    um Person() direto levanta TypeError.
    """

    _total = 0  # atributo de classe: compartilhado por todas as instancias

    def __init__(self, name: str, cpf: str):
        # A atribuicao passa pelos setters, entao a validacao sempre roda.
        self.name = name
        self.cpf = cpf
        Person._total += 1

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = (value or "").strip()
        if not value:
            raise EmptyNameError("O nome nao pode ficar em branco.")
        self._name = value.title()

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str) -> None:
        digits = "".join(c for c in (value or "") if c.isdigit())
        if not self.is_valid_cpf(digits):
            raise InvalidCpfError(f"CPF invalido: {value}")
        self._cpf = digits

    @property
    def formatted_cpf(self) -> str:
        """CPF no formato 000.000.000-00 (somente leitura, calculado na hora)."""
        d = self._cpf
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

    @staticmethod
    def is_valid_cpf(cpf: str) -> bool:
        """Confere os dois digitos verificadores do CPF.

        E estatico porque nao depende de nenhuma instancia: da para chamar
        Person.is_valid_cpf('12345678909') sem ter criado ninguem ainda.
        """
        if len(cpf) != 11 or not cpf.isdigit():
            return False
        if cpf == cpf[0] * 11:  # 00000000000, 11111111111... sao invalidos
            return False

        for posicao in (9, 10):
            soma = 0
            for i in range(posicao):
                soma += int(cpf[i]) * (posicao + 1 - i)
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if digito != int(cpf[posicao]):
                return False
        return True

    @classmethod
    def total_cadastrados(cls) -> int:
        """Quantas pessoas ja foram criadas (usa o atributo de classe)."""
        return cls._total

    @abstractmethod
    def describe(self) -> str:
        """Texto de apresentacao da pessoa.

        Tem @abstractmethod, entao toda subclasse e obrigada a escrever a sua
        versao. O corpo aqui nao e desperdicio: as subclasses reaproveitam
        este texto base chamando super().describe().
        """
        return f"{self._name} (CPF: {self.formatted_cpf})"

    def to_dict(self) -> dict:
        """Converte o objeto em dicionario, para gravar em CSV."""
        return {"name": self._name, "cpf": self._cpf}

    # --- Sobrecarga de operadores (metodos dunder) ---

    def __str__(self) -> str:
        """Representacao para o usuario final: print(pessoa)."""
        return self.describe()

    def __repr__(self) -> str:
        """Representacao tecnica, para o programador depurar."""
        return f"{type(self).__name__}(name={self._name!r}, cpf={self._cpf!r})"

    def __eq__(self, other) -> bool:
        """Duas pessoas sao a mesma se o CPF for igual (pessoa in lista)."""
        if not isinstance(other, Person):
            return NotImplemented
        return self._cpf == other._cpf

    def __hash__(self) -> int:
        return hash(self._cpf)

    def __lt__(self, other) -> bool:
        """Ordena por nome, fazendo sorted(pessoas) funcionar sem key=."""
        if not isinstance(other, Person):
            return NotImplemented
        return self._name < other._name
