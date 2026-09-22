# Documentacao do Sistema de Portaria

Explicacao de como o codigo esta organizado e como cada parte funciona.
Para o relatorio da disciplina, ver [RELATORIO.md](RELATORIO.md); para o
diagrama, ver [DIAGRAMA_CLASSES.md](DIAGRAMA_CLASSES.md).

## Visao geral

O sistema cadastra quatro tipos de pessoa (morador, visitante, entregador e
funcionario) e registra as entradas e saidas da portaria. Os dados ficam
guardados em arquivos CSV na pasta `dados/`, entao sobrevivem ao fechamento
do programa.

Duas interfaces usam o mesmo nucleo: o menu do terminal e o site Django.

## Arquitetura em camadas

```
ui/menu.py  (terminal)  ─┐
                         ├─> services/  ─> models/
web/portaria_app (Django)┘       │
                                 └─> persistence/ ─> dados/*.csv
```

A regra e simples: **uma camada so conversa com a de baixo**. `models/` nao
sabe o que e `input()`, `print()` ou HTTP; `persistence/` e a unica que sabe
o que e arquivo. Por isso foi possivel acrescentar a interface web sem
alterar nenhuma linha das classes de dominio.

## As classes de dominio (`src/models/`)

### `Person` — a base abstrata

```python
class Person(metaclass=ABCMeta):
    _total = 0

    def __init__(self, name, cpf):
        self.name = name   # passa pelo setter, entao valida
        self.cpf = cpf
        Person._total += 1
```

Pontos importantes:

- **E abstrata** (`metaclass=ABCMeta` + `@abstractmethod describe()`).
  "Pessoa" sozinha nao existe na portaria, entao `Person(...)` direto
  levanta `TypeError`. As subclasses ainda reaproveitam o corpo do metodo
  chamando `super().describe()`.
- **Encapsulamento com property**: `name` e `cpf` sao `@property` com
  setter. O setter normaliza (nome vira `Title Case`, CPF perde pontos) e
  valida, levantando excecao propria se o dado estiver errado.
- **`@staticmethod is_valid_cpf()`**: calcula os dois digitos verificadores
  de verdade. E estatico porque nao depende de nenhuma instancia.
- **`@classmethod total_cadastrados()`**: le o atributo de classe `_total`,
  compartilhado por todas as instancias.
- **Operadores**: `__str__`, `__repr__`, `__eq__` (compara por CPF),
  `__hash__` e `__lt__` (ordena por nome, fazendo `sorted()` funcionar).

### As subclasses

| Classe | Herda de | Acrescenta |
|---|---|---|
| `Resident` | `Person` | `unit` (obrigatorio) e `vehicle` (opcional) |
| `Visitor` | `Person` | `vehicle` (opcional) |
| `DeliveryPerson` | `Visitor` | `company` |
| `Employee` | `Person` | `role` e `shift` (turno validado) |

`DeliveryPerson` herda de `Visitor`, e nao de `Person`, formando tres
niveis. Quando ele chama `describe()`, a cadeia sobe inteira:

1. `DeliveryPerson.describe()` chama `super().describe()`
2. que e `Visitor.describe()`, que chama `super().describe()`
3. que e `Person.describe()`, que monta o texto com nome e CPF

Resultado: `Pedro Alves (CPF: ...) - Visitante, sem veiculo - Entregador da iFood`.

### `Unit` — composicao e protocolo de sequencia

Guarda numero, bloco e a lista de moradores. Implementa `__len__`,
`__getitem__` e `__contains__`, entao funciona assim **sem herdar de nada**:

```python
len(unidade)            # quantos moradores
unidade[0]              # primeiro morador
morador in unidade      # pertence?
for m in unidade: ...   # itera
```

Isso e duck typing: basta ter os metodos que o Python espera.

### `Vehicle` e `AccessLog`

`Vehicle` valida a placa nos padroes antigo e Mercosul, e e reaproveitado
por `Resident` e `Visitor` (a mesma classe servindo a duas outras).

`AccessLog` guarda quem entrou, o destino, a entrada e a saida. O tempo de
permanencia e **calculado** por `duration_minutes()`, nunca armazenado, para
nao existir dado redundante que possa ficar desatualizado.

## Regras de negocio (`src/services/condominio.py`)

A classe `Condominium` substituiu as listas globais que existiam no menu.
Ela concentra:

- **Cadastro** com `add_person()`, que recusa CPF duplicado
  (`DuplicateCpfError`);
- **Buscas**: `find_by_cpf()` (levanta `PersonNotFoundError` em vez de
  devolver `None` silenciosamente);
- **Generators** com `yield`: `find_by_name()`, `residents_of_block()` e
  `people_inside()` produzem os resultados sob demanda;
- **Controle de acesso**: `register_entry()` e `register_exit()`;
- **Protocolos**: `__iter__`, `__len__` e `__contains__`, entao
  `for pessoa in condominio` percorre os quatro tipos de uma vez so.

## Excecoes proprias (`src/errors.py`)

```
Exception
└── PortariaError
    ├── EmptyNameError
    ├── InvalidCpfError
    ├── InvalidPlateError
    ├── InvalidShiftError
    ├── DuplicateCpfError
    └── PersonNotFoundError
```

Como capturar a classe pai captura as filhas, o menu e as views escrevem
apenas `except PortariaError` e tratam qualquer erro do sistema de uma vez.

## Decoradores (`src/decorators.py`)

- `@log_operacao` — registra no historico toda execucao da funcao;
- `@contar_chamadas` — conta quantas vezes a funcao foi chamada.

Ambos usam `@functools.wraps` para preservar o nome e a docstring da funcao
original.

## Persistencia (`src/persistence/repositorio.py`)

- `ArquivoCsv` e um **context manager proprio** (`__enter__` / `__exit__`),
  usado com `with`. O `__exit__` roda mesmo se der erro no meio, garantindo
  o fechamento do arquivo.
- `Repositorio.salvar()` grava com `csv.DictWriter`;
  `Repositorio.carregar()` le com `csv.DictReader` e **recria os objetos**.
- Se o arquivo ainda nao existe (primeira execucao), `FileNotFoundError` e
  tratado e o sistema comeca com lista vazia em vez de quebrar.
- Os caminhos vem de `src/config.py`, montados com `pathlib.Path` a partir
  da localizacao do proprio arquivo — funciona de qualquer pasta.

## Menu do terminal (`src/ui/menu.py`)

O menu usa um **dicionario de opcoes** em vez de uma cadeia de `if/elif`:

```python
OPCOES = {
    "1": ("Cadastrar morador", cadastrar_morador),
    ...
}
```

As funcoes sao tratadas como valores. O laco principal usa
`try/except/finally`: captura `PortariaError`, trata `KeyboardInterrupt`
(Ctrl+C) com elegancia, e o `finally` salva os dados sempre — com ou sem
erro.

## Interface web (`web/`)

Projeto Django simples, com quatro paginas:

| Rota | View | O que mostra |
|---|---|---|
| `/` | `index` | Numeros gerais e quem esta dentro agora |
| `/pessoas/` | `pessoas` | Lista de cadastros, com busca por nome |
| `/cadastrar/` | `cadastrar` | Formulario dos quatro tipos de pessoa |
| `/acesso/` | `acesso` | Registrar entrada/saida e ver o historico |

Detalhes:

- **Nao usa o ORM do Django.** Nao ha `models.py` com modelos do Django: as
  views importam as mesmas classes de `src/models/` e a mesma persistencia
  em CSV. O `settings.py` acrescenta `src/` ao caminho de importacao.
- `portaria_app/servico.py` carrega o condominio dos CSVs uma vez e o
  compartilha entre as requisicoes.
- As views usam `try/except PortariaError` e mostram a mensagem de erro na
  propria pagina; quando da certo, salvam e redirecionam.

## Testes (`tests/test_models.py`)

22 testes com `unittest`, organizados em cinco classes e usando `setUp()`
para montar os objetos uma vez so. Cobrem validacao, o caminho de erro
(`assertRaises`), polimorfismo, composicao e o controle de acesso.

```bash
python3 -m unittest discover -s tests -v
```

## Fluxo de uma execucao (terminal)

1. `python3 src/main.py` chama `run_menu()`.
2. O repositorio carrega os CSVs e recria os objetos.
3. O usuario escolhe uma opcao; o dicionario `OPCOES` chama a funcao certa.
4. A funcao monta o objeto e entrega ao `Condominium`, que aplica as regras.
5. Ao sair (ou em caso de erro), o `finally` grava tudo de volta nos CSVs.
