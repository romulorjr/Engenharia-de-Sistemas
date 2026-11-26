# ADR 0002 — Persistência e atomicidade das operações

Data: 25/11/2026 (proposto). Status: **Aceito** em 26/11/2026 pelo responsável (opção A).
Requisitos: ENG-PERSIST, RN02, RN03, RN04, RN05, RN06. Issues: #4, #9, #10, #11, #19.

## Contexto
O PDF exige que estoque, crédito, estado da máquina e pedidos sobrevivam a uma reinicialização. RN02/RN03 exigem que a aceitação do pedido debite crédito e estoque e crie o pedido; RN05 exige que o cancelamento devolva o valor e mude o pedido. Uma falha no meio de qualquer dessas operações não pode deixar estado parcial. O [ADR 0001](0001-escolha-da-stack.md) escolheu SQLAlchemy 2.x + Alembic + SQLite.

Em 25/11/2026 foram avaliadas duas opções de acesso ao banco: manter o ADR 0001 (opção A) ou usar o módulo `sqlite3` da biblioteca padrão (opção B). O ambiente do agente não acessa o PyPI; essa limitação de ferramenta não é motivo para mudar a stack. Testes que não rodam nesse ambiente rodam na CI (#3) e nas máquinas dos integrantes.

## Decisão
**Opção A: manter SQLAlchemy 2.x (ORM, modo síncrono) + Alembic + SQLite em arquivo**, conforme o ADR 0001.

- Modelos e repositories ficam em `persistence/`. Só essa camada importa `sqlalchemy` e `alembic`.
- O esquema evolui por migrações Alembic versionadas. A configuração usa `render_as_batch=True`, necessário para alterar tabelas no SQLite.
- A inicialização aplica as migrações pendentes e grava o estoque cheio apenas na primeira execução (#4).
- O controle explícito de transação (`BEGIN IMMEDIATE` / `COMMIT` / `ROLLBACK`) fica na camada de serviços, pela unidade de trabalho descrita abaixo.

## Atomicidade
Fronteiras de transação. Cada linha é uma única transação: tudo é gravado ou nada é gravado.

| Operação | Regras | Pré-condições verificadas dentro da transação | Escritas |
|---|---|---|---|
| Inserir crédito | RN01 | estado PRONTA; denominação aceita; saldo + valor ≤ 5000 centavos | saldo |
| Aceitar pedido | RN02, RN03, RN04 | estado PRONTA; saldo ≥ preço; estoque da receita, do açúcar e de um copo | saldo −= preço; estoque −= consumo; INSERT do pedido EM_PREPARO com preço cobrado e previsão de término; estado = PREPARANDO |
| Concluir preparo | RN04, RN07 | pedido EM_PREPARO e previsão de término ≤ agora | pedido CONCLUIDO com instante; contador += 1; estado PRONTA ou AGUARDANDO_LIMPEZA |
| Cancelar pedido | RN05 | pedido EM_PREPARO e previsão de término > agora | pedido CANCELADO; saldo += preço cobrado; estado PRONTA |
| Devolver troco | RN06 | — | saldo = 0 |

Mecanismo:
- O serviço abre e fecha a transação por uma unidade de trabalho (`with unidade_de_trabalho() as uow:`), que envolve `Session.begin()` do SQLAlchemy. Ao sair do bloco sem exceção, faz `COMMIT`; com exceção, `ROLLBACK`.
- Repositories recebem a sessão da unidade de trabalho e **nunca** fazem commit.
- Toda transação de escrita começa com `BEGIN IMMEDIATE`, que obtém o bloqueio de escrita do SQLite antes das leituras. Assim, dois pedidos simultâneos não leem PRONTA ao mesmo tempo.
- Configuração do driver pysqlite conforme a documentação do SQLAlchemy para SQLite:
  - evento `connect`: desativa o `BEGIN` automático do pysqlite (`isolation_level = None`);
  - evento `begin`: emite `BEGIN IMMEDIATE`;
  - `timeout` da conexão (busy timeout), para que um segundo escritor espere em vez de falhar imediatamente.

Testes de integração obrigatórios (falham se a operação não for atômica):
- `test_order_rollback_on_midway_failure` (#9): substitui o repository de pedidos por um que lança exceção depois do débito de crédito e estoque. Por uma conexão nova, verifica que saldo, estoque, estado e quantidade de pedidos não mudaram.
- `test_cancel_rollback_on_midway_failure` (#11): injeta falha depois da restituição do crédito e verifica que o pedido continua EM_PREPARO e o saldo não mudou.
- `test_order_atomicity_and_concurrency` (#9): duas threads com conexões independentes pedem ao mesmo tempo; exatamente um pedido é aceito e o estoque é debitado uma vez.

Se cada repository fizesse commit por conta própria, o débito persistiria depois da falha injetada e os dois primeiros testes falhariam.

## Consequências
- Serviços dependem da unidade de trabalho, não de `Session` diretamente; os testes de serviço podem usar banco real em arquivo temporário.
- Testes de integração usam SQLite em arquivo temporário (não `:memory:`), para permitir conexões independentes.
- Dependências de execução incluem SQLAlchemy e Alembic (#4). A instalação delas e os testes de persistência são verificados na CI; o agente não os executa localmente.
- Mudanças de esquema exigem uma migração Alembic no mesmo PR, revisada como código.

## Alternativas consideradas
| Alternativa | Benefícios | Custos no contexto | Motivo da rejeição |
|---|---|---|---|
| A — SQLAlchemy + Alembic (escolhida) | ORM, migrações versionadas, documentação ampla, portabilidade para outro banco | Mais dependências; `BEGIN IMMEDIATE` exige configurar eventos do driver | — |
| B — `sqlite3` da biblioteca padrão + Repository, `BEGIN IMMEDIATE`/`COMMIT` explícitos | Nenhuma dependência de persistência; transação visível no código; testes executáveis no ambiente do agente | Mapeamento manual de linhas; migrador próprio com scripts SQL numerados | Rejeitada em 26/11/2026: o grupo mantém ORM e migrações para evoluir o esquema e manter portabilidade. O controle explícito de transação, principal ganho de B, já existe na opção A pela unidade de trabalho nos serviços. A limitação do ambiente do agente não justifica trocar a stack |

## Referências
- [SQLAlchemy: SQLite, transações e `BEGIN IMMEDIATE`](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [Alembic: batch migrations para SQLite](https://alembic.sqlalchemy.org/en/latest/batch.html)
- [SQLite: `BEGIN IMMEDIATE`](https://www.sqlite.org/lang_transaction.html)
