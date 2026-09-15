# Sistema de Condomínio (POO)

Projeto simples de cadastro para um condomínio, feito para a disciplina de
Programação Orientada a Objetos. Permite cadastrar **moradores** e
**visitantes** e listar os cadastros feitos.

## Estrutura do projeto

```
condominio-poo/
├── src/
│   ├── main.py            # ponto de entrada do programa
│   ├── models/            # classes de dominio
│   │   ├── person.py       # classe base, com nome e CPF
│   │   ├── resident.py     # morador, herda de Person
│   │   └── visitor.py      # visitante, herda de Person
│   └── ui/                # interface com o usuario
│       └── menu.py         # menu no terminal
├── docs/
│   └── IDEIAS.md          # 100 ideias de melhoria para o projeto
├── README.md
├── LICENSE
└── .gitignore
```

## Conceitos de POO aplicados

- **Encapsulamento**: os atributos de `Person` e das subclasses são privados
  (prefixo `_`) e acessados por `@property`.
- **Herança**: `Resident` e `Visitor` herdam de `Person`, reaproveitando
  `name` e `cpf` sem repetir código.
- **Polimorfismo**: tanto `Resident` quanto `Visitor` sobrescrevem o método
  `describe()`, e o `main.py` chama esse método da mesma forma para
  qualquer um dos dois, sem precisar saber qual é qual.

## Como rodar

Requisitos: Python 3.10 ou superior instalado.

```bash
cd src
python main.py
```

O programa mostra um menu no terminal para cadastrar morador, cadastrar
visitante, listar os cadastros feitos, ou sair.

## Próximos passos

Este é o MVP inicial, cobrindo só o cadastro. As próximas etapas planejadas
são: controle de acesso (entrada/saída na portaria) e reserva de área comum.

Uma lista completa de ideias de melhoria, detalhadas uma a uma, está em
[docs/IDEIAS.md](docs/IDEIAS.md).
