"""Views da portaria: cada funcao responde por uma pagina do site."""

from django.shortcuts import redirect, render

from errors import PortariaError
from models import DeliveryPerson, Employee, Resident, Vehicle, Visitor
from portaria_app.servico import condominio, salvar

import config


def _monta_veiculo(post):
    """Cria um Vehicle a partir do formulario, ou None se nao houver placa."""
    placa = post.get("placa", "").strip()
    if not placa:
        return None
    return Vehicle(placa, post.get("modelo", ""), post.get("cor", ""))


def index(request):
    """Pagina inicial: numeros gerais e quem esta dentro do condominio."""
    contexto = {
        "condominio": config.CONDOMINIO,
        "total": len(condominio),
        "moradores": len(condominio.residents),
        "visitantes": len(condominio.visitors),
        "entregadores": len(condominio.deliveries),
        "funcionarios": len(condominio.employees),
        "unidades": len(condominio.units),
        "dentro": list(condominio.people_inside()),
    }
    return render(request, "portaria_app/index.html", contexto)


def pessoas(request):
    """Lista todos os cadastros, com busca opcional por nome."""
    busca = request.GET.get("busca", "").strip()
    if busca:
        # find_by_name e um generator: produz os resultados sob demanda.
        lista = list(condominio.find_by_name(busca))
    else:
        lista = sorted(condominio)  # sorted usa o __lt__ de Person

    contexto = {
        "condominio": config.CONDOMINIO,
        "pessoas": lista,
        "busca": busca,
    }
    return render(request, "portaria_app/pessoas.html", contexto)


def cadastrar(request):
    """Formulario de cadastro dos quatro tipos de pessoa."""
    erro = None

    if request.method == "POST":
        tipo = request.POST.get("tipo", "")
        nome = request.POST.get("nome", "")
        cpf = request.POST.get("cpf", "")

        try:
            if tipo == "morador":
                unidade = condominio.find_or_create_unit(
                    request.POST.get("unidade", ""), request.POST.get("bloco", "")
                )
                pessoa = Resident(nome, cpf, unidade, _monta_veiculo(request.POST))
            elif tipo == "visitante":
                pessoa = Visitor(nome, cpf, _monta_veiculo(request.POST))
            elif tipo == "entregador":
                pessoa = DeliveryPerson(
                    nome, cpf, request.POST.get("empresa", ""), _monta_veiculo(request.POST)
                )
            elif tipo == "funcionario":
                pessoa = Employee(
                    nome, cpf, request.POST.get("funcao", ""), request.POST.get("turno", "")
                )
            else:
                raise PortariaError("Escolha o tipo de cadastro.")

            condominio.add_person(pessoa)
        except PortariaError as e:
            # Captura a classe pai: pega qualquer erro do sistema de uma vez.
            erro = str(e)
        else:
            salvar()
            return redirect("pessoas")

    contexto = {
        "condominio": config.CONDOMINIO,
        "turnos": config.TURNOS,
        "erro": erro,
        "dados": request.POST if request.method == "POST" else {},
    }
    return render(request, "portaria_app/cadastrar.html", contexto)


def acesso(request):
    """Registra entrada e saida na portaria."""
    erro = None
    aviso = None

    if request.method == "POST":
        cpf = request.POST.get("cpf", "")
        acao = request.POST.get("acao", "")

        try:
            if acao == "entrada":
                pessoa = condominio.find_by_cpf(cpf)
                if isinstance(pessoa, Resident):
                    destino = pessoa.unit
                else:
                    destino = condominio.find_or_create_unit(
                        request.POST.get("unidade", ""), request.POST.get("bloco", "")
                    )
                condominio.register_entry(pessoa, destino)
                aviso = f"Entrada de {pessoa.name} registrada."
            elif acao == "saida":
                log = condominio.register_exit(cpf)
                aviso = f"Saida de {log.person.name} registrada ({log.duration_minutes()} min)."
            else:
                raise PortariaError("Escolha entrada ou saida.")
        except PortariaError as e:
            erro = str(e)
        else:
            salvar()

    contexto = {
        "condominio": config.CONDOMINIO,
        "erro": erro,
        "aviso": aviso,
        "dentro": list(condominio.people_inside()),
        "registros": sorted(condominio.access_logs, reverse=True)[:10],
    }
    return render(request, "portaria_app/acesso.html", contexto)
