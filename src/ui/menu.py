"""Menu do terminal: le as opcoes do usuario e chama o cadastro."""

from models import Resident, Visitor, Employee, DeliveryPerson, Unit, Vehicle

residents = []
visitors = []
employees = []
deliveries = []
units = []


def find_or_create_unit(number: str, block: str) -> Unit:
    for unit in units:
        if unit.number == number and unit.block == block:
            return unit
    unit = Unit(number, block)
    units.append(unit)
    return unit


def read_vehicle():
    plate = input("Placa do veiculo (deixe em branco se nao tiver): ")
    if not plate:
        return None
    model = input("Modelo do veiculo (opcional): ")
    color = input("Cor do veiculo (opcional): ")
    return Vehicle(plate, model, color)


def register_resident():
    name = input("Nome do morador: ")
    cpf = input("CPF: ")
    unit_number = input("Numero da unidade: ")
    block = input("Bloco: ")
    unit = find_or_create_unit(unit_number, block)
    vehicle = read_vehicle()
    resident = Resident(name, cpf, unit, vehicle)
    residents.append(resident)
    print("Morador cadastrado com sucesso!\n")


def register_visitor():
    name = input("Nome do visitante: ")
    cpf = input("CPF: ")
    vehicle = read_vehicle()
    visitor = Visitor(name, cpf, vehicle)
    visitors.append(visitor)
    print("Visitante cadastrado com sucesso!\n")


def register_delivery():
    name = input("Nome do entregador: ")
    cpf = input("CPF: ")
    company = input("Empresa (iFood, Correios, transportadora...): ")
    vehicle = read_vehicle()
    delivery = DeliveryPerson(name, cpf, company, vehicle)
    deliveries.append(delivery)
    print("Entregador cadastrado com sucesso!\n")


def register_employee():
    name = input("Nome do funcionario: ")
    cpf = input("CPF: ")
    role = input("Funcao (porteiro, zelador, faxineiro...): ")
    shift = input("Turno (manha, tarde ou noite): ")
    employee = Employee(name, cpf, role, shift)
    employees.append(employee)
    print("Funcionario cadastrado com sucesso!\n")


def list_all():
    print("\n--- Moradores ---")
    for resident in residents:
        print(resident.describe())

    print("\n--- Visitantes ---")
    for visitor in visitors:
        print(visitor.describe())

    print("\n--- Entregadores ---")
    for delivery in deliveries:
        print(delivery.describe())

    print("\n--- Funcionarios ---")
    for employee in employees:
        print(employee.describe())
    print()


def run_menu():
    while True:
        print("1 - Cadastrar morador")
        print("2 - Cadastrar visitante")
        print("3 - Cadastrar entregador")
        print("4 - Cadastrar funcionario")
        print("5 - Listar cadastros")
        print("0 - Sair")
        option = input("Escolha uma opcao: ")

        if option == "1":
            register_resident()
        elif option == "2":
            register_visitor()
        elif option == "3":
            register_delivery()
        elif option == "4":
            register_employee()
        elif option == "5":
            list_all()
        elif option == "0":
            break
        else:
            print("Opcao invalida.\n")
