"""Excecoes proprias do sistema de portaria.

Todas herdam de PortariaError, que por sua vez herda de Exception. Assim quem
chama pode capturar um erro especifico (InvalidCpfError) ou todos os erros do
sistema de uma vez (PortariaError), porque capturar a classe pai captura
tambem as filhas.
"""


class PortariaError(Exception):
    """Classe base de todos os erros do sistema."""


class EmptyNameError(PortariaError):
    """Lancada quando o nome informado esta em branco."""


class InvalidCpfError(PortariaError):
    """Lancada quando o CPF nao e valido."""


class InvalidPlateError(PortariaError):
    """Lancada quando a placa do veiculo esta fora do padrao."""


class InvalidShiftError(PortariaError):
    """Lancada quando o turno informado nao existe."""


class DuplicateCpfError(PortariaError):
    """Lancada ao tentar cadastrar um CPF que ja existe."""


class PersonNotFoundError(PortariaError):
    """Lancada quando a busca por CPF nao encontra ninguem."""
