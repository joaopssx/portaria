# Relatorio do Projeto

**Disciplina:** Programacao Orientada a Objetos
**Entrega:** 28/09/2026
**Repositorio:** https://github.com/joaopssx/portaria

---

## 1. Titulo

**Sistema de Portaria para Condominios**

---

## 2. Descricao

O projeto e um sistema de controle de portaria para condominios
residenciais, escrito em Python. Ele resolve o trabalho diario de um
porteiro: manter o cadastro de quem pode entrar e registrar quem entrou e
quem saiu, com data e hora.

O sistema trabalha com quatro tipos de pessoa:

- **Morador** — vinculado a uma unidade (apartamento) de um bloco;
- **Visitante** — entrada temporaria, com destino informado na portaria;
- **Entregador** — um caso especifico de visitante, vinculado a uma empresa
  (iFood, Correios, transportadora);
- **Funcionario** — porteiro, zelador ou faxineiro, com funcao e turno.

Cada acesso gera um registro com a pessoa, o destino, o horario de entrada
e, quando a pessoa sai, o horario de saida e o tempo de permanencia.

O mesmo sistema pode ser usado por **duas interfaces diferentes**: um menu
no terminal e uma pagina web feita em Django. As duas compartilham as
mesmas classes de dominio e os mesmos arquivos de dados.

---

## 3. Justificativa

Em muitos condominios o controle de entrada ainda e feito em caderno de
papel. Isso gera tres problemas concretos:

1. **Dificuldade de consulta** — descobrir quem visitou o apartamento 101 no
   mes passado exige folhear o caderno pagina por pagina.
2. **Perda de informacao** — caderno molha, rasga, some ou fica ilegivel.
3. **Falta de controle em tempo real** — o porteiro do turno seguinte nao
   tem como saber rapidamente quem ainda esta dentro do condominio.

O problema tambem e um bom exercicio de Orientacao a Objetos, porque o
dominio ja vem naturalmente organizado em hierarquia: morador, visitante,
entregador e funcionario sao todos *pessoas*, mas com dados e regras
diferentes. Isso permite aplicar heranca e polimorfismo em uma situacao
real, e nao em um exemplo artificial.

---

## 4. Funcionalidades

### Cadastro
- Cadastrar morador (com unidade, bloco e veiculo opcional)
- Cadastrar visitante (com veiculo opcional)
- Cadastrar entregador (com empresa e veiculo opcional)
- Cadastrar funcionario (com funcao e turno)
- Impedir CPF duplicado
- Validar CPF pelos digitos verificadores
- Validar placa nos padroes antigo (ABC1234) e Mercosul (ABC1D23)
- Validar turno e nome em branco
- Reaproveitar a mesma unidade quando dois moradores moram juntos

### Controle de acesso
- Registrar entrada (destino automatico para morador)
- Registrar saida, calculando o tempo de permanencia
- Listar quem esta dentro do condominio agora
- Listar o historico dos ultimos acessos

### Consulta
- Listar todos os cadastros em ordem alfabetica
- Buscar pessoa por CPF
- Buscar pessoa por parte do nome
- Listar moradores de um bloco
- Relatorio com os numeros gerais do condominio

### Dados
- Salvar automaticamente em arquivos CSV ao sair
- Carregar os dados salvos ao iniciar
- Funcionar normalmente na primeira execucao, quando ainda nao ha arquivo

### Interfaces
- Menu no terminal
- Pagina web em Django (inicio, cadastros, novo cadastro, entrada/saida)

---

## 5. Temas abordados

Todos os temas vistos na disciplina, com o lugar exato onde cada um aparece:

| # | Tema | Onde esta no codigo |
|---|---|---|
| 1 | Programacao estruturada (fluxo, funcoes, estruturas de dados) | `src/ui/menu.py` — lacos, condicionais, listas e dicionarios |
| 2 | Abstracao e classes | `src/models/` — cada conceito do mundo real virou uma classe |
| 3 | Encapsulamento | Atributos com `_` em todas as classes de `src/models/` |
| 4 | Property (getter e setter) | `Person.name`, `Person.cpf`, `Vehicle.plate`, `Employee.shift` |
| 5 | Heranca | `Resident`, `Visitor`, `Employee` herdam de `Person` |
| 6 | Heranca em varios niveis | `Person` -> `Visitor` -> `DeliveryPerson` |
| 7 | Polimorfismo | `describe()` sobrescrito; `listar_cadastros()` chama sem saber o tipo |
| 8 | Modulos e pacotes | Pacotes `models`, `services`, `persistence`, `ui` com `__init__.py` |
| 9 | Classe abstrata (ABC) | `Person(metaclass=ABCMeta)` com `@abstractmethod describe()` |
| 10 | Contratos e protocolos | `Unit` implementa `__len__`, `__getitem__`, `__contains__` |
| 11 | Duck typing | `Condominium.add_person()` aceita qualquer pessoa que saiba `describe()` |
| 12 | Context manager (`with`) | `ArquivoCsv` com `__enter__` e `__exit__` |
| 13 | Tratamento de excecoes | `try/except/else/finally` no menu e nas views |
| 14 | Excecoes proprias | `src/errors.py` — hierarquia a partir de `PortariaError` |
| 15 | Decoradores | `src/decorators.py` — `@log_operacao` e `@contar_chamadas` |
| 16 | `@staticmethod` e `@classmethod` | `Person.is_valid_cpf()` e `Person.total_cadastrados()` |
| 17 | Atributo de classe | `Person._total`, contando quantas pessoas foram criadas |
| 18 | Iteradores | `Condominium.__iter__()` percorre todas as pessoas |
| 19 | Generators (`yield`) | `find_by_name()`, `residents_of_block()`, `people_inside()` |
| 20 | Sobrecarga de operadores | `__str__`, `__repr__`, `__eq__`, `__lt__`, `__hash__` |
| 21 | Persistencia em arquivo | `src/persistence/repositorio.py` com `open()` e `with` |
| 22 | CSV | `csv.DictWriter` e `csv.DictReader` no repositorio |
| 23 | Caminhos de arquivo | `pathlib.Path` em `src/config.py` |
| 24 | Interface grafica / web | `web/` — projeto Django |
| 25 | Testes automatizados | `tests/test_models.py` — 22 testes com `unittest` |

---

## 6. Tecnologias

| Tecnologia | Versao | Para que foi usada |
|---|---|---|
| Python | 3.13 | Linguagem do projeto inteiro |
| Django | 5.0+ | Interface web (paginas, rotas, templates) |
| CSV | — | Formato de armazenamento dos dados |
| HTML e CSS | — | Estrutura e estilo das paginas web |
| JavaScript | — | Mostrar/esconder campos do formulario conforme o tipo |
| Git e GitHub | — | Controle de versao e entrega do trabalho |
| Mermaid | — | Diagrama de classes escrito como texto |

---

## 7. Bibliotecas

### Biblioteca padrao do Python (nao precisa instalar nada)

| Biblioteca | Onde e usada |
|---|---|
| `abc` | `ABCMeta` e `@abstractmethod` na classe `Person` |
| `csv` | `DictWriter` e `DictReader` na persistencia |
| `datetime` | Horario de entrada e saida, calculo de permanencia |
| `pathlib` | Caminhos de arquivo independentes da pasta de execucao |
| `functools` | `@functools.wraps` dentro dos decoradores |
| `unittest` | Testes automatizados |

### Biblioteca externa

| Biblioteca | Versao | Motivo |
|---|---|---|
| Django | >= 5.0 | Unica dependencia externa, usada so na interface web |

O programa de terminal roda **somente com a biblioteca padrao**: o Django e
necessario apenas para abrir o site.

---

## 8. Distribuicao das Tarefas

> **A preencher com os nomes do grupo antes da entrega.** Se o trabalho for
> individual, basta deixar so a primeira linha.

| Integrante | Tarefas |
|---|---|
| Joao Pedro | Modelagem das classes, heranca e polimorfismo, camada de dominio (`src/models/`) |
| (integrante 2) | Regras de negocio e controle de acesso (`src/services/`) |
| (integrante 3) | Persistencia em CSV e tratamento de excecoes (`src/persistence/`, `src/errors.py`) |
| (integrante 4) | Interface web em Django (`web/`) |
| (integrante 5) | Testes automatizados, documentacao e diagrama (`tests/`, `docs/`) |

---

## 9. Como executar

### Programa de terminal (so biblioteca padrao)

```bash
python3 src/main.py
```

### Interface web (precisa do Django)

```bash
pip install -r requirements.txt
```

```bash
python3 web/manage.py runserver
```

Depois abrir `http://127.0.0.1:8000` no navegador.

### Testes automatizados

```bash
python3 -m unittest discover -s tests -v
```

---

## 10. Organizacao do repositorio

```
portaria/
├── src/                  # codigo-fonte do sistema
│   ├── main.py           # ponto de entrada do terminal
│   ├── config.py         # constantes e caminhos
│   ├── errors.py         # excecoes proprias
│   ├── decorators.py     # decoradores
│   ├── models/           # classes de dominio
│   ├── services/         # regras de negocio
│   ├── persistence/      # gravacao e leitura em CSV
│   └── ui/               # menu do terminal
├── web/                  # projeto Django (interface web)
├── tests/                # testes automatizados
├── docs/                 # documentacao e diagrama
├── dados/                # arquivos CSV gerados (nao versionados)
├── requirements.txt
└── README.md
```

---

## 11. Roteiro para a defesa oral

Pontos sugeridos para apresentar, do mais simples ao mais avancado:

1. **O problema** — mostrar o caderno de papel da portaria e os tres
   problemas da secao Justificativa.
2. **O diagrama de classes** (`docs/DIAGRAMA_CLASSES.md`) — explicar por que
   `Person` e abstrata e por que `DeliveryPerson` herda de `Visitor`.
3. **Demonstracao no terminal** — cadastrar, registrar entrada, listar.
4. **Demonstracao na web** — as mesmas operacoes na pagina Django, mostrando
   que os dados sao os mesmos (a mesma pasta `dados/`).
5. **Polimorfismo na pratica** — abrir `listar_cadastros()` e mostrar o
   unico `for` que atende os quatro tipos de pessoa.
6. **Tratamento de erro** — tentar cadastrar um CPF invalido e mostrar a
   excecao propria sendo capturada.
7. **Testes** — rodar `unittest` ao vivo e mostrar os 22 testes passando.
