# Diagrama de Classes

Diagrama UML das classes do sistema de portaria, escrito em Mermaid (o
GitHub renderiza automaticamente ao abrir este arquivo).

## Visao geral

```mermaid
classDiagram
    class Person {
        <<abstract>>
        -str _name
        -str _cpf
        -int _total$
        +name: str
        +cpf: str
        +formatted_cpf: str
        +is_valid_cpf(cpf)$ bool
        +total_cadastrados()$ int
        +describe()* str
        +to_dict() dict
        +__str__() str
        +__repr__() str
        +__eq__(other) bool
        +__lt__(other) bool
    }

    class Resident {
        -Unit _unit
        -Vehicle _vehicle
        +unit: Unit
        +vehicle: Vehicle
        +describe() str
    }

    class Visitor {
        -Vehicle _vehicle
        +vehicle: Vehicle
        +describe() str
    }

    class DeliveryPerson {
        -str _company
        +company: str
        +describe() str
    }

    class Employee {
        -str _role
        -str _shift
        +role: str
        +shift: str
        +describe() str
    }

    class Unit {
        -str _number
        -str _block
        -list _residents
        +number: str
        +block: str
        +residents: list
        +add_resident(resident)
        +describe() str
        +__len__() int
        +__getitem__(i)
        +__contains__(r) bool
    }

    class Vehicle {
        -str _plate
        -str _model
        -str _color
        +plate: str
        +is_valid_plate(plate)$ bool
        +describe() str
    }

    class AccessLog {
        -Person _person
        -Unit _destination
        -datetime _entry_time
        -datetime _exit_time
        +is_open: bool
        +register_exit(t)
        +duration_minutes() int
        +describe() str
        +__lt__(other) bool
    }

    class Condominium {
        -str _nome
        -list _residents
        -list _visitors
        -list _deliveries
        -list _employees
        -list _units
        -list _access_logs
        +add_person(person)
        +find_by_cpf(cpf) Person
        +find_by_name(t) generator
        +people_inside() generator
        +register_entry(p, u) AccessLog
        +register_exit(cpf) AccessLog
        +relatorio() str
        +__iter__()
        +__len__() int
    }

    class Repositorio {
        +salvar(condominio)
        +carregar(condominio)
    }

    class ArquivoCsv {
        -Path _caminho
        -str _modo
        +__enter__()
        +__exit__(...)
    }

    Person <|-- Resident : heranca
    Person <|-- Visitor : heranca
    Person <|-- Employee : heranca
    Visitor <|-- DeliveryPerson : heranca

    Resident *-- Unit : composicao
    Resident o-- Vehicle : agregacao
    Visitor o-- Vehicle : agregacao
    Unit o-- Resident : moradores

    AccessLog --> Person : registra
    AccessLog --> Unit : destino

    Condominium o-- Person : cadastros
    Condominium o-- Unit : unidades
    Condominium o-- AccessLog : acessos

    Repositorio ..> Condominium : salva/carrega
    Repositorio ..> ArquivoCsv : usa
```

## Hierarquia de excecoes

```mermaid
classDiagram
    class Exception {
        <<built-in>>
    }
    class PortariaError
    class EmptyNameError
    class InvalidCpfError
    class InvalidPlateError
    class InvalidShiftError
    class DuplicateCpfError
    class PersonNotFoundError

    Exception <|-- PortariaError
    PortariaError <|-- EmptyNameError
    PortariaError <|-- InvalidCpfError
    PortariaError <|-- InvalidPlateError
    PortariaError <|-- InvalidShiftError
    PortariaError <|-- DuplicateCpfError
    PortariaError <|-- PersonNotFoundError
```

Capturar `PortariaError` captura todas as filhas de uma vez, que e
exatamente o que o menu e as views do Django fazem.

## Arquitetura em camadas

```mermaid
flowchart TD
    A["ui/menu.py<br/>(terminal)"] --> C
    B["web/portaria_app<br/>(Django)"] --> C
    C["services/condominio.py<br/>(regras de negocio)"] --> D
    D["models/<br/>(classes de dominio)"]
    C --> E["persistence/repositorio.py<br/>(CSV)"]
    E --> F[("dados/*.csv")]
```

As duas interfaces (terminal e web) usam exatamente as mesmas classes de
dominio e a mesma persistencia. Trocar a interface nao exige mexer em
`models/`.

## Legenda dos relacionamentos

| Simbolo | Nome | Significado no projeto |
|---|---|---|
| `<\|--` | Heranca | `Resident` **e um** `Person` |
| `*--` | Composicao | Um `Resident` sempre pertence a uma `Unit` |
| `o--` | Agregacao | Um `Resident` **pode ter** um `Vehicle` |
| `-->` | Associacao | `AccessLog` aponta para a `Person` que entrou |
| `..>` | Dependencia | `Repositorio` usa `ArquivoCsv` para gravar |
