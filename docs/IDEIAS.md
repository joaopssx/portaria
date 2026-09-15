




### 2. Classe `DeliveryPerson` (entregador)
Subclasse de `Visitor` com o atributo `company` (iFood, Correios, transportadora).
Entregador é um caso específico de visitante, então herdar de `Visitor` e não de
`Person` mostra que você entendeu hierarquia em mais de um nível.
**Conceito:** herança em três níveis (`Person` → `Visitor` → `DeliveryPerson`).

### 3. Classe `Unit` (unidade/apartamento)
Hoje o morador guarda `block` e `unit_number` como texto solto. Crie uma classe
`Unit` com `number`, `block` e uma lista de moradores. O morador passa a guardar
um objeto `Unit` em vez de duas strings. **Conceito:** composição — um objeto
tendo outro objeto como atributo.

### 4. Classe `Vehicle` (veículo)
Em vez de `license_plate` ser uma string dentro de `Visitor`, crie `Vehicle` com
`plate`, `model` e `color`. Visitantes e moradores podem ter um veículo
associado. **Conceito:** composição e reaproveitamento — a mesma classe serve a
duas outras.

### 5. Classe `AccessLog` (registro de acesso)
Classe que representa uma entrada na portaria: quem entrou (`Person`), a data e
hora, e o destino (unidade). É o coração do próximo passo já previsto no README.
**Conceito:** composição — o registro guarda uma referência a uma pessoa.

### 6. Classe `Condominium` (condomínio)
Uma classe que guarda as listas de moradores, visitantes e unidades, hoje soltas
como variáveis globais no menu. Os métodos viram `add_resident()`,
`find_by_cpf()`, `list_residents()`. **Conceito:** encapsulamento — o estado do
programa deixa de ser global e passa a ser atributo de um objeto.

### 7. Classe `CommonArea` (área comum)
Salão de festas, churrasqueira, quadra. Atributos: `name`, `capacity` e se está
disponível. É o segundo item da seção "Próximos passos" do README.
**Conceito:** modelagem de domínio — traduzir uma coisa do mundo real em classe.

### 8. Classe `Reservation` (reserva)
Liga um `Resident` a uma `CommonArea` numa data. Guarda quem reservou, o que
reservou e quando. **Conceito:** composição — um objeto que só existe ligando
outros dois.

### 9. Classe `Package` (encomenda)
Encomenda que chegou na portaria: destinatário (morador), remetente, data de
chegada e se já foi retirada. **Conceito:** encapsulamento — o campo "retirada"
só muda por um método `withdraw()`, nunca por atribuição direta.

### 10. Classe `Guest` (convidado autorizado)
Visitante que o morador autorizou **antes** de chegar. Guarda quem autorizou e
até quando a autorização vale. **Conceito:** relacionamento entre objetos — o
convidado aponta para o morador que o liberou.

### 11. Classe `Pet`
Cachorros e gatos cadastrados por unidade, com `name`, `species` e `size`.
Pequeno, mas é mais uma classe para exercitar composição com `Unit`.
**Conceito:** composição e lista de objetos dentro de outro objeto.

### 12. Classe `Notice` (aviso/comunicado)
Comunicados que o síndico publica: título, texto e data. A portaria lista os
avisos ativos. **Conceito:** modelagem simples, boa para praticar `__str__`.

---

## 2. Encapsulamento e validação (13–24)

### 13. Validar nome vazio
No `__init__` de `Person`, rejeite nome em branco ou só com espaços, lançando
`ValueError("Nome nao pode ser vazio")`. **Conceito:** encapsulamento — a classe
protege o próprio estado, não confia em quem a instancia.

### 14. Validar formato do CPF
Checar se o CPF tem 11 dígitos depois de remover pontos e traços. Não precisa
validar o dígito verificador (mas veja a ideia 15). **Conceito:** validação no
construtor.

### 15. Calcular o dígito verificador do CPF
Um passo além da ideia 14: implemente o cálculo real dos dois dígitos
verificadores num método estático `Person.is_valid_cpf(cpf)`. É um bom exercício
de lógica e de `@staticmethod`. **Conceito:** método estático — não depende de
nenhuma instância.

### 16. Normalizar o CPF no setter
Guardar o CPF sempre só com números, mesmo que o usuário digite com pontos.
Assim `123.456.789-00` e `12345678900` viram a mesma coisa e a busca funciona.
**Conceito:** o setter como lugar de transformar dado, não só de guardar.

### 17. Property com setter para nome
Hoje `name` só tem getter. Adicione um `@name.setter` que valida antes de
atribuir, permitindo corrigir um nome digitado errado sem mexer no `_name`
direto. **Conceito:** `@property` completa (getter + setter).

### 18. Padronizar a capitalização do nome
No setter, aplicar `.strip().title()` para que "joão da silva" vire "João Da
Silva". **Conceito:** o objeto garante consistência dos próprios dados.

### 19. Validar formato da placa
Aceitar placa antiga (`ABC1234`) e Mercosul (`ABC1D23`), rejeitando o resto.
Use `len()` e checagens de caractere, sem precisar de regex.
**Conceito:** validação em subclasse, específica do `Visitor`.

### 20. Validar bloco e número da unidade
Número da unidade tem que ser numérico; bloco tem que ser uma letra.
**Conceito:** cada classe valida o que é responsabilidade dela — `Resident`
valida o que é de morador, `Person` valida o que é de pessoa.

### 21. Atributo de classe com contador de cadastros
Um `_total = 0` na classe `Person`, incrementado a cada `__init__`, e um
`@classmethod total_registered()` que devolve o número. **Conceito:** diferença
entre atributo de classe (compartilhado) e de instância (individual).

### 22. Gerar ID automático para cada pessoa
Um contador de classe que dá a cada objeto um `id` único e sequencial, exposto
só por getter (sem setter). **Conceito:** atributo somente-leitura — o ID nasce
com o objeto e nunca muda.

### 23. Usar `__slots__` ou nome com dois underscores
Trocar `_name` por `__name` em `Person` e ver o *name mangling* do Python na
prática, discutindo a diferença entre "privado por convenção" e "privado de
verdade". **Conceito:** níveis de encapsulamento em Python.

### 24. Método `update_data()` para alterar cadastro
Em vez de mexer nos atributos um a um de fora, um método que recebe os novos
valores, valida todos e só então altera. Se um for inválido, nada muda.
**Conceito:** o objeto controla suas próprias transições de estado.

---

## 3. Herança e polimorfismo (25–36)

### 25. Implementar `__str__` em todas as classes
Substituir (ou complementar) `describe()` por `__str__`, permitindo escrever
`print(resident)` direto. **Conceito:** sobrescrita de método mágico — a forma
"pythônica" de polimorfismo.

### 26. Implementar `__repr__` para depuração
`__repr__` mostra a forma técnica (`Resident(name='Joao', cpf='111')`), útil ao
imprimir uma lista de objetos. **Conceito:** diferença entre representação para
o usuário (`__str__`) e para o programador (`__repr__`).

### 27. Implementar `__eq__` para comparar por CPF
Duas pessoas com o mesmo CPF são a mesma pessoa. Isso faz `pessoa in lista`
funcionar sozinho. **Conceito:** sobrecarga de operador (`==`).

### 28. Implementar `__lt__` para ordenar por nome
Com `__lt__` definido, `sorted(residents)` passa a funcionar sem precisar de
`key=`. **Conceito:** sobrecarga de operador de comparação.

### 29. Tornar `Person` uma classe abstrata
Usar `ABC` e `@abstractmethod` no `describe()`, impedindo criar uma `Person`
solta — só `Resident`, `Visitor` e `Employee` existem de fato.
**Conceito:** classe abstrata, um dos pontos mais cobrados em prova de POO.

### 30. Método abstrato `access_permission()`
Cada subclasse responde de um jeito: morador tem acesso livre, visitante precisa
de autorização, funcionário tem acesso no horário do turno.
**Conceito:** polimorfismo puro — mesma chamada, comportamentos diferentes.

### 31. Lista única e polimórfica de pessoas
Trocar as duas listas (`residents` e `visitors`) por uma só, `people`, e iterar
chamando `describe()` sem perguntar o tipo de ninguém.
**Conceito:** polimorfismo aplicado — é o argumento principal a favor da
herança que você já escreveu no README.

### 32. Filtrar por tipo com `isinstance()`
Com a lista única da ideia 31, um método `list_by_type(Resident)` devolve só os
moradores. **Conceito:** checagem de tipo em tempo de execução, e discussão de
quando ela é aceitável e quando é sinal de design ruim.

### 33. Mixin `Contactable` para telefone e e-mail
Uma classe pequena com `phone`, `email` e `send_message()`, herdada junto com
`Person` por quem precisa. **Conceito:** herança múltipla e MRO, em dose
pequena e controlada.

### 34. `super()` com `**kwargs` no construtor
Refatorar os `__init__` para repassar argumentos por palavra-chave, mostrando
por que `super()` é melhor que chamar `Person.__init__` na mão.
**Conceito:** cadeia de construtores.

### 35. Método de classe `from_input()` como construtor alternativo
`Resident.from_input()` faz os `input()` e devolve o objeto pronto. O menu fica
com uma linha só por cadastro. **Conceito:** `@classmethod` como construtor
alternativo (*factory method*).

### 36. Método de classe `from_dict()` / `to_dict()`
Converter objeto para dicionário e vice-versa. Prepara o terreno para salvar em
JSON (ideia 64). **Conceito:** serialização de objetos.

---

## 4. Composição e relacionamentos (37–46)

### 37. Morador pertence a uma unidade
Aplicar a classe `Unit` (ideia 3): `resident.unit.block` em vez de
`resident.block`. **Conceito:** navegação entre objetos relacionados.

### 38. Unidade com lista de moradores
Cada `Unit` guarda seus moradores, permitindo perguntar "quem mora no 101?".
**Conceito:** relacionamento um-para-muitos.

### 39. Definir um morador responsável pela unidade
Entre os moradores da unidade, um é o titular. É ele quem autoriza visitantes.
**Conceito:** relacionamento com papel específico.

### 40. Visitante ligado à unidade que vai visitar
Todo visitante tem um destino. Sem isso, a portaria não sabe para onde mandar a
pessoa. **Conceito:** associação obrigatória (o objeto não existe sem a relação).

### 41. Visitante ligado ao morador que autorizou
Além do destino, guardar quem liberou a entrada — informação essencial se algo
der errado. **Conceito:** duas associações diferentes na mesma classe.

### 42. Histórico de visitas por morador
Cada `Resident` guarda a lista de visitantes que já recebeu, alimentada
automaticamente no registro de entrada. **Conceito:** agregação — a lista cresce
como efeito de outra operação.

### 43. Classe `Turn` / turno do porteiro
Um turno tem hora de início, hora de fim, o funcionário responsável e os acessos
registrados nele. **Conceito:** objeto que agrupa outros objetos por contexto.

### 44. Encomenda ligada a morador e entregador
`Package` guarda quem entregou e para quem é. **Conceito:** objeto no meio de um
relacionamento entre dois outros.

### 45. Reserva ligada a área comum e morador
Aplicar as ideias 7 e 8 juntas, com verificação de conflito de data.
**Conceito:** regra de negócio que depende de dois objetos ao mesmo tempo.

### 46. Método `is_authorized()` no visitante
Devolve `True` se existe um morador autorizador e a autorização ainda está no
prazo. **Conceito:** comportamento derivado do estado — o objeto responde sobre
si mesmo em vez de expor os dados para outro decidir.

---

## 5. Funcionalidades da portaria (47–62)

### 47. Registrar entrada
Opção de menu que marca a data/hora de entrada de uma pessoa já cadastrada,
criando um `AccessLog`. **Conceito:** o objeto que representa um evento, não uma
coisa.

### 48. Registrar saída
Fecha o registro de acesso aberto, preenchendo a hora de saída.
**Conceito:** ciclo de vida de um objeto (aberto → fechado).

### 49. Listar quem está dentro do condomínio agora
Filtrar os registros com entrada preenchida e saída vazia.
**Conceito:** consulta sobre uma coleção de objetos.

### 50. Calcular o tempo de permanência
Método que devolve quantos minutos a pessoa ficou, a partir de entrada e saída.
**Conceito:** método que calcula em vez de guardar — evita dado redundante.

### 51. Buscar pessoa por CPF
Método `find_by_cpf()` que percorre a lista e devolve o objeto ou `None`.
**Conceito:** busca em coleção e tratamento do caso "não encontrado".

### 52. Buscar por nome parcial
Procurar "jo" e encontrar "João" e "Joana", usando `in` e `.lower()`.
**Conceito:** busca com critério flexível.

### 53. Editar um cadastro existente
Buscar pelo CPF e chamar `update_data()` (ideia 24). **Conceito:** o "U" do
CRUD, aplicando os setters validados.

### 54. Remover um cadastro
Excluir morador ou visitante, com confirmação antes. **Conceito:** o "D" do
CRUD, e cuidado com objetos que ainda são referenciados por outros.

### 55. Desativar em vez de excluir
Um campo `active` que marca o cadastro como inativo, preservando o histórico.
É o que sistemas reais fazem. **Conceito:** exclusão lógica vs. física.

### 56. Impedir CPF duplicado
Antes de cadastrar, verificar se o CPF já existe e avisar em vez de criar um
segundo registro. **Conceito:** regra de unicidade, validada por quem gerencia a
coleção — não pela classe `Person`.

### 57. Bloquear visitante na lista negra
Um conjunto de CPFs bloqueados; ao registrar entrada, o sistema recusa e explica.
**Conceito:** regra de negócio antes de criar o objeto.

### 58. Registrar entrega de encomenda
Cadastrar a encomenda na chegada e dar baixa na retirada, guardando quem retirou.
**Conceito:** mudança de estado controlada por método.

### 59. Listar encomendas pendentes por unidade
Relatório simples filtrando as não retiradas e agrupando por unidade.
**Conceito:** agrupamento de objetos com dicionário.

### 60. Reservar área comum com checagem de conflito
Antes de criar a reserva, verificar se já existe outra na mesma área e data.
**Conceito:** validação que envolve a coleção inteira, não um objeto só.

### 61. Cancelar reserva
Remover ou marcar a reserva como cancelada, liberando a data.
**Conceito:** operação inversa, com o cuidado de não quebrar o histórico.

### 62. Relatório do dia
Resumo em tela: quantas entradas, quantas saídas, quem ainda está dentro e
quantas encomendas chegaram. **Conceito:** método que consolida dados de várias
coleções.

---

## 6. Persistência de dados (63–72)

### 63. Salvar cadastros em arquivo de texto
Gravar uma pessoa por linha, com campos separados por `;`, usando `with open()`.
**Conceito:** persistência básica e o gerenciador de contexto `with`.

### 64. Salvar em JSON
Usar `json.dump()` com os dicionários da ideia 36. Fica bem mais legível e fácil
de carregar que o texto puro. **Conceito:** serialização — do objeto para o
arquivo e de volta.

### 65. Carregar os dados ao iniciar o programa
No começo do `main()`, ler o arquivo e recriar os objetos, para que os cadastros
sobrevivam ao fechamento do programa. **Conceito:** desserialização — o passo
que fecha o ciclo da ideia 64.

### 66. Salvar automaticamente ao sair
Chamar o salvamento na opção "0 - Sair", para o usuário não perder dado por
esquecimento. **Conceito:** garantir a persistência sem depender do usuário.

### 67. Usar CSV com o módulo `csv`
Gravar em formato que abre direto no Excel, usando `csv.DictWriter`.
**Conceito:** usar a biblioteca padrão em vez de reinventar o parser.

### 68. Separar um arquivo por tipo de dado
`residents.json`, `visitors.json`, `access_log.json`, cada um com sua
responsabilidade. **Conceito:** organização de dados espelhando a organização das
classes.

### 69. Criar uma classe `Repository`
Classe com `save(lista)` e `load()` que centraliza toda a leitura e escrita. As
classes de domínio não sabem nada sobre arquivos. **Conceito:** separação de
responsabilidades — a classe mais importante dessa seção.

### 70. Tratar arquivo inexistente na primeira execução
Se o arquivo ainda não existe, começar com lista vazia em vez de quebrar.
**Conceito:** `try/except FileNotFoundError`.

### 71. Usar `pathlib` para montar os caminhos
`Path(__file__).parent / "data"` funciona independente de onde o programa foi
executado, ao contrário de `"../data/arquivo.json"`. **Conceito:** caminhos
robustos, um erro clássico em trabalho de faculdade.

### 72. Fazer backup antes de sobrescrever
Copiar o arquivo atual para `.bak` antes de gravar por cima.
**Conceito:** cuidado com perda de dados.

---

## 7. Interface e experiência de uso (73–82)

### 73. Menu em laço com dicionário de opções
Trocar a cadeia de `if/elif` por um dicionário `{"1": register_resident, ...}`,
tratando funções como valores. **Conceito:** funções como objetos de primeira
classe.

### 74. Submenus por área
Um menu principal (Cadastros / Acessos / Encomendas / Relatórios), cada um com
suas opções. **Conceito:** organização da interface espelhando a do código.

### 75. Função utilitária de entrada validada
`read_int("Numero: ")` que insiste até o usuário digitar um número válido, em vez
de quebrar com `ValueError`. **Conceito:** reaproveitamento — uma função usada em
todos os cadastros.

### 76. Limpar a tela entre as telas
`os.system("clear" ou "cls")` para o terminal não virar uma parede de texto.
**Conceito:** detalhe de usabilidade que melhora muito a apresentação.

### 77. Cabeçalho fixo com o nome do condomínio
Uma função `print_header()` reaproveitada em todas as telas.
**Conceito:** evitar repetição (DRY).

### 78. Listagem em formato de tabela
Alinhar as colunas com f-strings (`f"{nome:<20}{cpf:<15}"`), deixando a saída
muito mais profissional. **Conceito:** formatação de strings.

### 79. Pedir confirmação antes de apagar
"Tem certeza? (s/n)" antes de qualquer exclusão.
**Conceito:** proteger o usuário de operações irreversíveis.

### 80. Mensagens de sucesso e erro padronizadas
Funções `show_success()` e `show_error()` com prefixos fixos (`[OK]`, `[ERRO]`),
em vez de `print()` solto com texto diferente cada vez.
**Conceito:** consistência de interface.

### 81. Aceitar entradas em maiúscula ou minúscula
Tratar a opção do menu com `.strip().lower()` para "S", "s" e " s " funcionarem
igual. **Conceito:** normalização de entrada.

### 82. Opção de ajuda no menu
Uma opção que explica o que cada número faz e quais dados o sistema pede.
**Conceito:** documentação embutida no programa.

---

## 8. Tratamento de erros (83–88)

### 83. Proteger todos os `input()` numéricos
Envolver conversões em `try/except ValueError` para o programa não morrer quando
alguém digitar "abc" onde se esperava número. **Conceito:** tratamento de
exceções.

### 84. Criar uma exceção própria `InvalidCpfError`
Uma classe herdando de `Exception`, lançada pela validação de CPF. Deixa o erro
específico e fácil de capturar. **Conceito:** herança aplicada a exceções — um
uso de herança que quase ninguém lembra que existe.

### 85. Exceção `PersonNotFoundError`
Lançada pela busca quando nada é encontrado, em vez de devolver `None` e deixar o
chamador esquecer de checar. **Conceito:** erro explícito vs. retorno silencioso.

### 86. Exceção `DuplicateCpfError`
Lançada ao tentar cadastrar um CPF que já existe (ideia 56).
**Conceito:** família de exceções do projeto, todas herdando de uma base comum
`PortariaError`.

### 87. Tratar `Ctrl+C` com elegância
Capturar `KeyboardInterrupt` no `main()`, salvar os dados e sair com uma
mensagem, em vez de despejar o *traceback* na tela.
**Conceito:** encerramento controlado.

### 88. Usar `finally` para garantir o salvamento
O bloco `finally` roda mesmo se houver erro, garantindo que os dados sejam
gravados. **Conceito:** `try/except/finally` completo.

---

## 9. Testes e qualidade (89–94)

### 89. Testes automatizados com `unittest`
Um arquivo `tests/test_models.py` verificando que `describe()` devolve o texto
certo e que o construtor rejeita nome vazio. **Conceito:** testar o comportamento
público de uma classe.

### 90. Testar que a exceção é lançada
`with self.assertRaises(InvalidCpfError):` ao criar uma pessoa com CPF inválido.
**Conceito:** testar o caminho de erro, não só o caminho feliz.

### 91. Testar o polimorfismo
Um teste que percorre uma lista com `Resident` e `Visitor` e confirma que cada um
devolve uma descrição diferente. **Conceito:** provar na prática o que o README
afirma sobre polimorfismo.

### 92. Usar `setUp()` para preparar os objetos
Criar os objetos de teste uma vez no `setUp()` em vez de repetir em cada método.
**Conceito:** organização de testes e reaproveitamento.

### 93. Adicionar *type hints* em tudo
Anotar parâmetros e retornos de todos os métodos, como já foi feito em `Person`.
**Conceito:** contrato explícito de cada método.

### 94. Rodar um formatador e um linter
Passar `black` para formatar e `flake8` para achar variável não usada e import
esquecido. **Conceito:** padrão de código — o professor percebe.

---

## 10. Organização e documentação (95–100)

### 95. Docstring em todas as classes e métodos públicos
As classes já têm; faltam os métodos. Uma linha explicando o que o método faz e o
que devolve. **Conceito:** documentação que aparece no `help()`.

### 96. Diagrama de classes UML no README
Um diagrama simples (pode ser feito no draw.io ou em texto) mostrando `Person` no
topo e as subclasses embaixo, com as setas de composição.
**Conceito:** representação visual do modelo — costuma valer nota.

### 97. Constantes num arquivo `config.py`
Nome do condomínio, caminho dos arquivos de dados e limites ficam num lugar só,
sem números mágicos espalhados. **Conceito:** centralização de configuração.

### 98. Separar em camadas: `models`, `services`, `ui`
`models` guarda as classes de domínio, `services` as regras de negócio e `ui` o
menu. Uma camada só conversa com a de baixo.
**Conceito:** arquitetura em camadas — a evolução natural da organização de
pastas atual.

### 99. Arquivo `CHANGELOG.md`
Registrar o que mudou em cada versão do trabalho. Mostra evolução ao longo do
semestre, o que ajuda na apresentação.
**Conceito:** versionamento e histórico do projeto.

### 100. Commits pequenos e descritivos no Git
Um commit por funcionalidade, com mensagem no imperativo ("adiciona classe
Employee"), em vez de um único commit gigante no fim.
**Conceito:** boa prática de versionamento — o histórico conta a história do
trabalho.

---

## Sugestão de roteiro

| Etapa | Ideias sugeridas | O que fica pronto |
|---|---|---|
| 1 | 6, 13, 14, 25, 51, 56 | Base sólida: classe `Condominium`, validação e busca |
| 2 | 1, 29, 30, 31 | Herança e polimorfismo bem demonstrados |
| 3 | 3, 4, 37, 40 | Composição entre unidade, veículo e pessoas |
| 4 | 5, 47, 48, 49 | Controle de acesso funcionando |
| 5 | 36, 64, 65, 69 | Dados persistindo entre execuções |
| 6 | 84, 85, 89, 91 | Exceções próprias e testes automatizados |
