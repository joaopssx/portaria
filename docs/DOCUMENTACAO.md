# Documentação do Sistema de Portaria

Explicação de como o código está organizado e como cada parte funciona.
Serve como guia rápido para entender o projeto sem precisar ler tudo do
zero.

## Visão geral

O programa é um cadastro de portaria de condomínio rodando no terminal.
Ele guarda, em memória (enquanto o programa está aberto), quatro tipos de
pessoa: **moradores**, **visitantes**, **entregadores** e
**funcionários**. Não existe banco de dados nem arquivo salvo — ao fechar
o programa, os cadastros são perdidos.

## Estrutura de pastas

```
src/
├── main.py            # ponto de entrada
├── models/            # classes de dominio (o "o que existe" no sistema)
│   ├── __init__.py
│   ├── person.py
│   ├── resident.py
│   ├── visitor.py
│   ├── delivery_person.py
│   └── employee.py
└── ui/                 # interface com o usuario (o "como se usa")
    ├── __init__.py
    └── menu.py
```

A ideia por trás dessa divisão: `models` não sabe nada sobre `input()` ou
`print()` — só define os dados e comportamentos de cada tipo de pessoa.
Quem conversa com o usuário é o `ui`. Essa separação facilita trocar a
interface no futuro (por exemplo, para uma interface gráfica) sem precisar
mexer nas classes de domínio.

## As classes em `models/`

### `Person` ([person.py](../src/models/person.py))

Classe base de todo mundo que entra no sistema. Guarda `name` e `cpf`.

```python
class Person:
    def __init__(self, name: str, cpf: str):
        self._name = name
        self._cpf = cpf
```

Os atributos começam com `_` (underscore) por convenção de
**encapsulamento**: eles não deveriam ser acessados diretamente de fora da
classe. O jeito correto de ler o nome ou o CPF é pelas `@property`:

```python
@property
def name(self) -> str:
    return self._name
```

Isso permite, no futuro, adicionar validação dentro do getter (ou criar um
setter) sem quebrar quem já usa `pessoa.name`.

O método `describe()` devolve um texto pronto para exibir:

```python
def describe(self) -> str:
    return f"{self._name} (CPF: {self._cpf})"
```

### `Resident` ([resident.py](../src/models/resident.py))

Um morador **é** uma pessoa (herança), então:

```python
class Resident(Person):
    def __init__(self, name, cpf, unit_number, block):
        super().__init__(name, cpf)
        self._unit_number = unit_number
        self._block = block
```

`super().__init__(name, cpf)` chama o construtor de `Person` para não
repetir a lógica de guardar nome e CPF. `Resident` só adiciona o que é
específico dele: unidade e bloco.

O `describe()` também reaproveita o de `Person`:

```python
def describe(self) -> str:
    base_info = super().describe()
    return f"{base_info} - Morador do bloco {self._block}, unidade {self._unit_number}"
```

`super().describe()` pega o texto básico (`"Nome (CPF: ...)"`) e
`Resident` só completa com a parte que é dele. Isso é **polimorfismo**: a
mesma chamada `describe()` se comporta de um jeito diferente em cada
subclasse.

### `Visitor` ([visitor.py](../src/models/visitor.py))

Mesmo padrão do `Resident`, mas para visitantes: adiciona `license_plate`
(placa do veículo, opcional). O `describe()` verifica se a placa foi
informada para escolher a frase certa:

```python
if self._license_plate:
    return f"{base_info} - Visitante, veiculo placa {self._license_plate}"
return f"{base_info} - Visitante, sem veiculo"
```

### `DeliveryPerson` ([delivery_person.py](../src/models/delivery_person.py))

Um entregador é um caso específico de visitante (chega, entrega, sai), por
isso herda de `Visitor` e não de `Person` diretamente:

```python
class DeliveryPerson(Visitor):
    def __init__(self, name, cpf, company, license_plate=""):
        super().__init__(name, cpf, license_plate)
        self._company = company
```

Isso cria uma cadeia de herança de três níveis:
`Person` → `Visitor` → `DeliveryPerson`. Quando um `DeliveryPerson` chama
`describe()`, a cadeia de `super()` roda assim:

1. `DeliveryPerson.describe()` chama `super().describe()`
2. que é `Visitor.describe()`, que chama `super().describe()`
3. que é `Person.describe()`, que monta a base com nome e CPF

Cada nível só acrescenta a sua parte, sem repetir o que já foi feito pelo
nível anterior.

### `Employee` ([employee.py](../src/models/employee.py))

Funcionário do condomínio (porteiro, zelador, faxineiro), com `role`
(função) e `shift` (turno). Herda direto de `Person`, porque um
funcionário não é um caso de visitante nem de morador.

### `models/__init__.py`

Reexporta as cinco classes para que o resto do código possa importar de
um lugar só:

```python
from models import Resident, Visitor, Employee, DeliveryPerson
```

em vez de precisar saber o nome do arquivo de cada classe.

## A interface em `ui/menu.py`

O menu guarda quatro listas em memória, uma para cada tipo de cadastro:

```python
residents = []
visitors = []
employees = []
deliveries = []
```

Para cada tipo existe uma função `register_*()` que faz três coisas:
pergunta os dados com `input()`, cria o objeto da classe correspondente e
guarda na lista certa. Exemplo:

```python
def register_resident():
    name = input("Nome do morador: ")
    cpf = input("CPF: ")
    unit_number = input("Numero da unidade: ")
    block = input("Bloco: ")
    resident = Resident(name, cpf, unit_number, block)
    residents.append(resident)
    print("Morador cadastrado com sucesso!\n")
```

A função `list_all()` percorre as quatro listas e chama `describe()` em
cada objeto. Repare que ela nunca pergunta "isso é um morador ou um
visitante?" — ela só chama `.describe()` e cada classe sabe responder do
seu próprio jeito. Esse é o uso prático do polimorfismo: o código que
imprime é o mesmo para qualquer tipo de pessoa.

A função `run_menu()` é o laço principal: mostra as opções, lê a escolha
do usuário e chama a função correspondente, até a opção `0` ser escolhida.

## O ponto de entrada: `main.py`

```python
from ui import run_menu

def main():
    run_menu()

if __name__ == "__main__":
    main()
```

`main.py` não faz nada sozinho: ele só chama `run_menu()`. O
`if __name__ == "__main__":` garante que `main()` só roda quando o
arquivo é executado diretamente (`python main.py`), e não quando é
importado por outro módulo.

## Fluxo de uma execução

1. `python src/main.py` roda `main()`.
2. `main()` chama `run_menu()`, que mostra o menu em laço.
3. O usuário escolhe uma opção (ex.: "1 - Cadastrar morador").
4. `run_menu()` chama a função correspondente (`register_resident()`).
5. Essa função pergunta os dados, cria um objeto (`Resident(...)`) e
   guarda na lista `residents`.
6. O laço volta ao início e mostra o menu de novo, até o usuário escolher
   sair.

## Conceitos de POO usados, com exemplo de cada um

| Conceito | Onde aparece | Como |
|---|---|---|
| Encapsulamento | Todas as classes em `models/` | Atributos com `_` e acesso via `@property` |
| Herança | `Resident`, `Visitor`, `Employee` → `Person`; `DeliveryPerson` → `Visitor` | `class X(Person):` e `super().__init__(...)` |
| Polimorfismo | `describe()` em cada classe | `list_all()` chama `describe()` sem saber o tipo exato do objeto |
| Composição de comportamento | `describe()` nas subclasses | Cada `describe()` reaproveita `super().describe()` e só acrescenta sua parte |

## Como rodar

```bash
cd src
python main.py
```

## Onde ver mais

Uma lista de 100 ideias de melhoria para evoluir o projeto (com o
conceito de POO de cada uma) está em `docs/IDEIAS.md` — esse arquivo fica
só na máquina local (não é enviado ao GitHub, veja o `.gitignore`).
