"""Liga a interface web as classes de dominio que ja existem em src/.

O site nao tem modelos proprios do Django: ele reaproveita as mesmas
classes usadas pelo programa de terminal e a mesma persistencia em CSV.
"""

import config
from persistence import Repositorio
from services import Condominium

# Um unico condominio compartilhado por todas as requisicoes do servidor.
condominio = Condominium(config.CONDOMINIO)
repositorio = Repositorio()
repositorio.carregar(condominio)


def salvar() -> None:
    """Grava o estado atual nos arquivos CSV."""
    repositorio.salvar(condominio)
