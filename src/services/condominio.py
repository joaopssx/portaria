"""Regras de negocio do condominio: guarda as colecoes e faz as buscas."""

from decorators import contar_chamadas, log_operacao
from errors import DuplicateCpfError, PersonNotFoundError
from models import AccessLog, Employee, Resident, Unit


class Condominium:
    """Agrupa moradores, visitantes, entregadores, funcionarios e acessos.

    Antes essas listas eram variaveis globais soltas no menu. Agora sao
    atributos privados de um objeto, e so mudam pelos metodos da classe.

    Implementa __iter__ e __len__, entao "for pessoa in condominio" e
    len(condominio) funcionam direto.
    """

    def __init__(self, nome: str):
        self._nome = nome
        self._residents = []
        self._visitors = []
        self._deliveries = []
        self._employees = []
        self._units = []
        self._access_logs = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def residents(self) -> list:
        return list(self._residents)

    @property
    def visitors(self) -> list:
        return list(self._visitors)

    @property
    def deliveries(self) -> list:
        return list(self._deliveries)

    @property
    def employees(self) -> list:
        return list(self._employees)

    @property
    def units(self) -> list:
        return list(self._units)

    @property
    def access_logs(self) -> list:
        return list(self._access_logs)

    # --- Cadastro ---

    def find_or_create_unit(self, number: str, block: str) -> Unit:
        nova = Unit(number, block)
        for unit in self._units:
            if unit == nova:  # usa o __eq__ de Unit
                return unit
        self._units.append(nova)
        return nova

    @log_operacao
    def add_person(self, person) -> None:
        """Cadastra qualquer tipo de pessoa, escolhendo a lista certa.

        Recebe Resident, Visitor, DeliveryPerson ou Employee sem perguntar o
        tipo com if: cada objeto ja sabe quem e. So o destino da lista muda.
        """
        if self.exists(person.cpf):
            raise DuplicateCpfError(f"Ja existe alguem cadastrado com o CPF {person.cpf}.")

        # DeliveryPerson herda de Visitor, entao precisa ser testado antes.
        from models import DeliveryPerson, Visitor

        if isinstance(person, Resident):
            self._residents.append(person)
        elif isinstance(person, DeliveryPerson):
            self._deliveries.append(person)
        elif isinstance(person, Visitor):
            self._visitors.append(person)
        elif isinstance(person, Employee):
            self._employees.append(person)

    def exists(self, cpf: str) -> bool:
        digits = "".join(c for c in cpf if c.isdigit())
        return any(p.cpf == digits for p in self)

    @contar_chamadas
    def find_by_cpf(self, cpf: str):
        """Busca uma pessoa pelo CPF. Levanta PersonNotFoundError se nao achar."""
        digits = "".join(c for c in cpf if c.isdigit())
        for person in self:
            if person.cpf == digits:
                return person
        raise PersonNotFoundError(f"Nenhuma pessoa cadastrada com o CPF {cpf}.")

    # --- Generators: produzem os resultados sob demanda, com yield ---

    def find_by_name(self, trecho: str):
        """Gera as pessoas cujo nome contem o trecho informado."""
        trecho = trecho.strip().lower()
        for person in self:
            if trecho in person.name.lower():
                yield person

    def residents_of_block(self, block: str):
        """Gera os moradores de um bloco."""
        block = block.strip().upper()
        for resident in self._residents:
            if resident.unit.block == block:
                yield resident

    def people_inside(self):
        """Gera os registros de quem entrou e ainda nao saiu."""
        for log in self._access_logs:
            if log.is_open:
                yield log

    # --- Controle de acesso ---

    @log_operacao
    def register_entry(self, person, destination: Unit) -> AccessLog:
        log = AccessLog(person, destination)
        self._access_logs.append(log)
        return log

    def add_access_log(self, log: AccessLog) -> None:
        """Adiciona um registro ja pronto (usado ao carregar do arquivo)."""
        self._access_logs.append(log)

    @log_operacao
    def register_exit(self, cpf: str) -> AccessLog:
        """Fecha o ultimo registro aberto da pessoa."""
        person = self.find_by_cpf(cpf)
        for log in reversed(self._access_logs):
            if log.person == person and log.is_open:
                log.register_exit()
                return log
        raise PersonNotFoundError(f"{person.name} nao tem entrada em aberto.")

    def relatorio(self) -> str:
        """Resumo consolidando dados de varias colecoes."""
        dentro = list(self.people_inside())
        return (
            f"{self._nome}\n"
            f"  Moradores:    {len(self._residents)}\n"
            f"  Visitantes:   {len(self._visitors)}\n"
            f"  Entregadores: {len(self._deliveries)}\n"
            f"  Funcionarios: {len(self._employees)}\n"
            f"  Unidades:     {len(self._units)}\n"
            f"  Acessos:      {len(self._access_logs)} (dentro agora: {len(dentro)})"
        )

    # --- Protocolos ---

    def __iter__(self):
        """Percorre todas as pessoas, de qualquer tipo, em um unico for."""
        for pessoa in self._residents + self._visitors + self._deliveries + self._employees:
            yield pessoa

    def __len__(self) -> int:
        return len(self._residents) + len(self._visitors) + len(self._deliveries) + len(self._employees)

    def __contains__(self, person) -> bool:
        return any(p == person for p in self)

    def __str__(self) -> str:
        return f"{self._nome} ({len(self)} pessoas cadastradas)"

    def __repr__(self) -> str:
        return f"Condominium(nome={self._nome!r})"
