"""Menu do terminal: le as opcoes do usuario e chama as regras de negocio."""

import config
from errors import PortariaError
from models import DeliveryPerson, Employee, Resident, Vehicle, Visitor
from persistence import Repositorio
from services import Condominium

condominio = Condominium(config.CONDOMINIO)
repositorio = Repositorio()


def cabecalho(titulo: str) -> None:
    print(f"\n=== {config.CONDOMINIO} | {titulo} ===")


def ler_texto(rotulo: str) -> str:
    return input(rotulo).strip()


def ler_veiculo():
    """Le os dados do veiculo; devolve None se nao houver placa."""
    placa = ler_texto("Placa do veiculo (deixe em branco se nao tiver): ")
    if not placa:
        return None
    modelo = ler_texto("Modelo (opcional): ")
    cor = ler_texto("Cor (opcional): ")
    return Vehicle(placa, modelo, cor)


def cadastrar_morador():
    cabecalho("Cadastro de morador")
    nome = ler_texto("Nome: ")
    cpf = ler_texto("CPF: ")
    numero = ler_texto("Numero da unidade: ")
    bloco = ler_texto("Bloco: ")
    unidade = condominio.find_or_create_unit(numero, bloco)
    condominio.add_person(Resident(nome, cpf, unidade, ler_veiculo()))
    print("[OK] Morador cadastrado!")


def cadastrar_visitante():
    cabecalho("Cadastro de visitante")
    nome = ler_texto("Nome: ")
    cpf = ler_texto("CPF: ")
    condominio.add_person(Visitor(nome, cpf, ler_veiculo()))
    print("[OK] Visitante cadastrado!")


def cadastrar_entregador():
    cabecalho("Cadastro de entregador")
    nome = ler_texto("Nome: ")
    cpf = ler_texto("CPF: ")
    empresa = ler_texto("Empresa (iFood, Correios...): ")
    condominio.add_person(DeliveryPerson(nome, cpf, empresa, ler_veiculo()))
    print("[OK] Entregador cadastrado!")


def cadastrar_funcionario():
    cabecalho("Cadastro de funcionario")
    nome = ler_texto("Nome: ")
    cpf = ler_texto("CPF: ")
    funcao = ler_texto("Funcao (porteiro, zelador...): ")
    turno = ler_texto(f"Turno {config.TURNOS}: ")
    condominio.add_person(Employee(nome, cpf, funcao, turno))
    print("[OK] Funcionario cadastrado!")


def registrar_entrada():
    cabecalho("Registrar entrada")
    pessoa = condominio.find_by_cpf(ler_texto("CPF de quem esta entrando: "))
    if isinstance(pessoa, Resident):
        destino = pessoa.unit
    else:
        numero = ler_texto("Unidade de destino: ")
        bloco = ler_texto("Bloco de destino: ")
        destino = condominio.find_or_create_unit(numero, bloco)
    condominio.register_entry(pessoa, destino)
    print("[OK] Entrada registrada!")


def registrar_saida():
    cabecalho("Registrar saida")
    log = condominio.register_exit(ler_texto("CPF de quem esta saindo: "))
    print(f"[OK] Saida registrada! Permanencia: {log.duration_minutes()} min")


def listar_cadastros():
    cabecalho("Cadastros")
    # Um unico for para todos os tipos: cada objeto responde do seu jeito.
    print(f"{'NOME':<25}{'CPF':<16}DESCRICAO")
    print("-" * 78)
    for pessoa in sorted(condominio):  # sorted usa o __lt__ de Person
        print(f"{pessoa.name:<25}{pessoa.formatted_cpf:<16}{pessoa}")
    if len(condominio) == 0:
        print("(nenhum cadastro ainda)")


def listar_quem_esta_dentro():
    cabecalho("Quem esta dentro agora")
    encontrou = False
    for log in condominio.people_inside():
        print(f"- {log}")
        encontrou = True
    if not encontrou:
        print("(ninguem dentro no momento)")


def buscar_pessoa():
    cabecalho("Buscar por nome")
    trecho = ler_texto("Digite parte do nome: ")
    encontrou = False
    for pessoa in condominio.find_by_name(trecho):
        print(f"- {pessoa}")
        encontrou = True
    if not encontrou:
        print("(nada encontrado)")


def mostrar_relatorio():
    cabecalho("Relatorio")
    print(condominio.relatorio())


def salvar():
    repositorio.salvar(condominio)
    print(f"[OK] Dados salvos em {config.DATA_DIR}")


OPCOES = {
    "1": ("Cadastrar morador", cadastrar_morador),
    "2": ("Cadastrar visitante", cadastrar_visitante),
    "3": ("Cadastrar entregador", cadastrar_entregador),
    "4": ("Cadastrar funcionario", cadastrar_funcionario),
    "5": ("Registrar entrada", registrar_entrada),
    "6": ("Registrar saida", registrar_saida),
    "7": ("Listar cadastros", listar_cadastros),
    "8": ("Quem esta dentro agora", listar_quem_esta_dentro),
    "9": ("Buscar por nome", buscar_pessoa),
    "10": ("Relatorio", mostrar_relatorio),
    "11": ("Salvar dados", salvar),
}


def run_menu():
    """Laco principal do menu."""
    repositorio.carregar(condominio)
    print(f"Dados carregados: {len(condominio)} pessoas cadastradas.")

    try:
        while True:
            cabecalho("Menu")
            for chave, (rotulo, _) in OPCOES.items():
                print(f"{chave:>2} - {rotulo}")
            print(" 0 - Sair")

            escolha = input("Escolha uma opcao: ").strip()

            if escolha == "0":
                break
            if escolha not in OPCOES:
                print("[ERRO] Opcao invalida.")
                continue

            try:
                OPCOES[escolha][1]()
            except PortariaError as erro:
                # Captura a classe pai: pega qualquer erro do sistema.
                print(f"[ERRO] {erro}")
            except ValueError as erro:
                print(f"[ERRO] Valor invalido: {erro}")
    except KeyboardInterrupt:
        print("\nEncerrando...")
    finally:
        # O finally roda sempre, com ou sem erro: os dados nunca se perdem.
        repositorio.salvar(condominio)
        print("Dados salvos. Ate logo!")
