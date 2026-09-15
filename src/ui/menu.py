"""Menu do terminal: le as opcoes do usuario e chama o cadastro."""

from models import Resident, Visitor, Employee

residents = []
visitors = []
employees = []


def register_resident():
    name = input("Nome do morador: ")
    cpf = input("CPF: ")
    unit_number = input("Numero da unidade: ")
    block = input("Bloco: ")
    resident = Resident(name, cpf, unit_number, block)
    residents.append(resident)
    print("Morador cadastrado com sucesso!\n")


def register_visitor():
    name = input("Nome do visitante: ")
    cpf = input("CPF: ")
    license_plate = input("Placa do veiculo (deixe em branco se nao tiver): ")
    visitor = Visitor(name, cpf, license_plate)
    visitors.append(visitor)
    print("Visitante cadastrado com sucesso!\n")


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

    print("\n--- Funcionarios ---")
    for employee in employees:
        print(employee.describe())
    print()


def run_menu():
    while True:
        print("1 - Cadastrar morador")
        print("2 - Cadastrar visitante")
        print("3 - Cadastrar funcionario")
        print("4 - Listar cadastros")
        print("0 - Sair")
        option = input("Escolha uma opcao: ")

        if option == "1":
            register_resident()
        elif option == "2":
            register_visitor()
        elif option == "3":
            register_employee()
        elif option == "4":
            list_all()
        elif option == "0":
            break
        else:
            print("Opcao invalida.\n")
