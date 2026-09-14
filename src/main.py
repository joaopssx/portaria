from resident import Resident
from visitor import Visitor

residents = []
visitors = []


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


def list_all():
    print("\n--- Moradores ---")
    for resident in residents:
        print(resident.describe())

    print("\n--- Visitantes ---")
    for visitor in visitors:
        print(visitor.describe())
    print()


def main():
    while True:
        print("1 - Cadastrar morador")
        print("2 - Cadastrar visitante")
        print("3 - Listar cadastros")
        print("0 - Sair")
        option = input("Escolha uma opcao: ")

        if option == "1":
            register_resident()
        elif option == "2":
            register_visitor()
        elif option == "3":
            list_all()
        elif option == "0":
            break
        else:
            print("Opcao invalida.\n")


if __name__ == "__main__":
    main()
