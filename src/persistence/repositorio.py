"""Persistencia em arquivos CSV.

As classes de dominio nao sabem nada sobre arquivos: quem le e grava e o
repositorio. Assim, trocar CSV por banco de dados no futuro nao mexe em
models/.
"""

import csv
from datetime import datetime

import config
from errors import PersonNotFoundError
from models import AccessLog, DeliveryPerson, Employee, Resident, Vehicle, Visitor
from models.access_log import FORMATO


class ArquivoCsv:
    """Context manager proprio para abrir um CSV com seguranca.

    Implementa __enter__ e __exit__, entao funciona com "with". O __exit__
    roda mesmo se der erro no meio do bloco, garantindo o fechamento.
    """

    def __init__(self, caminho, modo="r"):
        self._caminho = caminho
        self._modo = modo
        self._arquivo = None

    def __enter__(self):
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        self._arquivo = open(self._caminho, self._modo, newline="", encoding="utf-8")
        return self._arquivo

    def __exit__(self, exc_type, exc_value, traceback):
        if self._arquivo:
            self._arquivo.close()
        return False  # False = nao engole a excecao, ela continua subindo


def _gravar(caminho, colunas, objetos):
    """Grava uma lista de objetos em CSV usando DictWriter."""
    with ArquivoCsv(caminho, "w") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=colunas)
        writer.writeheader()
        for obj in objetos:
            writer.writerow(obj.to_dict())


def _ler(caminho):
    """Le um CSV e devolve a lista de dicionarios (DictReader).

    Se o arquivo ainda nao existe (primeira execucao), devolve lista vazia em
    vez de quebrar o programa.
    """
    try:
        with ArquivoCsv(caminho, "r") as arquivo:
            return list(csv.DictReader(arquivo))
    except FileNotFoundError:
        return []


class Repositorio:
    """Salva e carrega o condominio inteiro em arquivos CSV."""

    COLUNAS_MORADOR = ["name", "cpf", "unit_number", "block", "plate", "model", "color"]
    COLUNAS_VISITANTE = ["name", "cpf", "plate", "model", "color"]
    COLUNAS_ENTREGADOR = ["name", "cpf", "plate", "model", "color", "company"]
    COLUNAS_FUNCIONARIO = ["name", "cpf", "role", "shift"]
    COLUNAS_ACESSO = ["cpf", "name", "unit_number", "block", "entry_time", "exit_time"]

    def salvar(self, condominio) -> None:
        _gravar(config.ARQUIVO_MORADORES, self.COLUNAS_MORADOR, condominio.residents)
        _gravar(config.ARQUIVO_VISITANTES, self.COLUNAS_VISITANTE, condominio.visitors)
        _gravar(config.ARQUIVO_ENTREGADORES, self.COLUNAS_ENTREGADOR, condominio.deliveries)
        _gravar(config.ARQUIVO_FUNCIONARIOS, self.COLUNAS_FUNCIONARIO, condominio.employees)
        _gravar(config.ARQUIVO_ACESSOS, self.COLUNAS_ACESSO, condominio.access_logs)

    def carregar(self, condominio) -> None:
        """Le os CSVs e recria os objetos dentro do condominio."""
        for linha in _ler(config.ARQUIVO_MORADORES):
            unit = condominio.find_or_create_unit(linha["unit_number"], linha["block"])
            condominio.add_person(Resident(linha["name"], linha["cpf"], unit, self._veiculo(linha)))

        for linha in _ler(config.ARQUIVO_VISITANTES):
            condominio.add_person(Visitor(linha["name"], linha["cpf"], self._veiculo(linha)))

        for linha in _ler(config.ARQUIVO_ENTREGADORES):
            condominio.add_person(
                DeliveryPerson(linha["name"], linha["cpf"], linha["company"], self._veiculo(linha))
            )

        for linha in _ler(config.ARQUIVO_FUNCIONARIOS):
            condominio.add_person(Employee(linha["name"], linha["cpf"], linha["role"], linha["shift"]))

        for linha in _ler(config.ARQUIVO_ACESSOS):
            try:
                pessoa = condominio.find_by_cpf(linha["cpf"])
            except PersonNotFoundError:
                continue  # acesso de alguem que nao esta mais cadastrado
            unit = condominio.find_or_create_unit(linha["unit_number"], linha["block"])
            log = AccessLog(pessoa, unit, datetime.strptime(linha["entry_time"], FORMATO))
            if linha["exit_time"]:
                log.register_exit(datetime.strptime(linha["exit_time"], FORMATO))
            condominio.add_access_log(log)

    @staticmethod
    def _veiculo(linha):
        """Recria o Vehicle a partir da linha do CSV, se houver placa."""
        if linha.get("plate"):
            return Vehicle(linha["plate"], linha.get("model", ""), linha.get("color", ""))
        return None
