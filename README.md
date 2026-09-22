# Sistema de Portaria para Condominios

Projeto da disciplina de **Programacao Orientada a Objetos**.

Sistema de controle de portaria: cadastra moradores, visitantes,
entregadores e funcionarios, e registra as entradas e saidas do condominio
com data, hora e tempo de permanencia.

Funciona por **duas interfaces** que compartilham as mesmas classes e os
mesmos dados: um menu no terminal e uma pagina web em Django.

## Estrutura do repositorio

```
portaria/
├── src/                  # codigo-fonte do sistema
│   ├── main.py           # ponto de entrada do terminal
│   ├── config.py         # constantes e caminhos dos arquivos
│   ├── errors.py         # excecoes proprias do sistema
│   ├── decorators.py     # decoradores (@log_operacao, @contar_chamadas)
│   ├── models/           # classes de dominio (Person, Unit, Vehicle...)
│   ├── services/         # regras de negocio (Condominium)
│   ├── persistence/      # leitura e gravacao em CSV
│   └── ui/               # menu do terminal
├── web/                  # projeto Django (interface web)
├── tests/                # testes automatizados (unittest)
├── docs/                 # documentacao, relatorio e diagrama de classes
├── dados/                # arquivos CSV gerados ao usar o sistema
├── requirements.txt
├── LICENSE
└── README.md
```

## Como rodar

### Terminal (nao precisa instalar nada)

```bash
python3 src/main.py
```

### Web (precisa do Django)

```bash
pip install -r requirements.txt
```

```bash
python3 web/manage.py runserver
```

Depois e so abrir `http://127.0.0.1:8000`.

### Testes

```bash
python3 -m unittest discover -s tests -v
```

## Documentacao

| Arquivo | Conteudo |
|---|---|
| [docs/RELATORIO.md](docs/RELATORIO.md) | Relatorio completo do trabalho |
| [docs/DIAGRAMA_CLASSES.md](docs/DIAGRAMA_CLASSES.md) | Diagrama de classes (UML em Mermaid) |
| [docs/DOCUMENTACAO.md](docs/DOCUMENTACAO.md) | Explicacao do codigo, classe por classe |
| [docs/BANCO_DE_DADOS.md](docs/BANCO_DE_DADOS.md) | Notas sobre banco de dados (a preencher) |

## Conceitos de POO aplicados

Heranca em tres niveis (`Person` -> `Visitor` -> `DeliveryPerson`), classe
abstrata com `ABCMeta`, encapsulamento com `@property`, polimorfismo em
`describe()`, composicao com `Unit` e `Vehicle`, protocolos (`__len__`,
`__getitem__`, `__enter__`/`__exit__`), sobrecarga de operadores, iteradores
e generators, decoradores, excecoes proprias e persistencia em CSV.

A lista completa, com o lugar exato de cada conceito no codigo, esta na
secao "Temas abordados" do [relatorio](docs/RELATORIO.md).

## Observacao sobre o CPF

O sistema valida o CPF pelos **digitos verificadores reais**, entao numeros
inventados como `111.111.111-11` sao recusados. Para testar, use um gerador
de CPF valido ou um destes: `526.018.159-06`, `083.016.613-05`,
`186.091.390-34`.
