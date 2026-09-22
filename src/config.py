"""Constantes de configuracao do sistema (caminhos, nomes, limites)."""

from pathlib import Path

CONDOMINIO = "Residencial Jardim das Flores"

# Caminho absoluto montado a partir da localizacao deste arquivo, para o
# programa funcionar independente da pasta de onde foi executado.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "dados"

ARQUIVO_MORADORES = DATA_DIR / "moradores.csv"
ARQUIVO_VISITANTES = DATA_DIR / "visitantes.csv"
ARQUIVO_ENTREGADORES = DATA_DIR / "entregadores.csv"
ARQUIVO_FUNCIONARIOS = DATA_DIR / "funcionarios.csv"
ARQUIVO_ACESSOS = DATA_DIR / "acessos.csv"

TURNOS = ("manha", "tarde", "noite")
