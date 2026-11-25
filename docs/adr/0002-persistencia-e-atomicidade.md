# ADR 0002 — Persistência e atomicidade das operações

Data: 25/11/2026. Status: **Proposto. Aguarda a escolha do responsável entre as opções A e B.** A parte "Atomicidade" vale para as duas opções.
Requisitos: ENG-PERSIST, RN02, RN03, RN04, RN05, RN06. Issues: #4, #9, #10, #11, #19.

## Contexto
O PDF exige que estoque, crédito, estado da máquina e pedidos sobrevivam a uma reinicialização. RN02/RN03 exigem que a aceitação do pedido debite crédito e estoque e crie o pedido; RN05 exige que o cancelamento devolva o valor e mude o pedido. Uma falha no meio de qualquer dessas operações não pode deixar estado parcial. O [ADR 0001](0001-escolha-da-stack.md) escolheu SQLAlchemy 2.x + Alembic + SQLite.

Em 25/11/2026 o responsável recebeu duas opções e ainda não escolheu:

| Opção | Resumo | Ganha | Perde |
|---|---|---|---|
| A — manter ADR 0001 | SQLAlchemy 2.x + Alembic + SQLite. Testes que não rodam no ambiente do agente rodam na CI; a stack não muda por limitação de ferramenta. | ORM, migrações versionadas pelo Alembic, documentação ampla | Mais dependências; `BEGIN IMMEDIATE` exige configurar eventos do driver pysqlite |
| B — substituir ADR 0001 na persistência | `sqlite3` da biblioteca padrão, padrão Repository, `BEGIN IMMEDIATE`/`COMMIT` explícitos | Nenhuma dependência de persistência; controle de transação visível no código; testes executáveis em qualquer ambiente com Python | Sem ORM (mapeamento manual de linhas) e sem Alembic; mudanças de esquema por scripts SQL numerados aplicados por um migrador próprio com tabela de versão |

## Atomicidade (independente da opção)
Fronteiras de transação. Cada linha é uma única transação: tudo é gravado ou nada é gravado.

| Operação | Regras | Pré-condições verificadas dentro da transação | Escritas |
|---|---|---|---|
| Inserir crédito | RN01 | estado PRONTA; denominação aceita; saldo + valor ≤ 5000 centavos | saldo |
| Aceitar pedido | RN02, RN03, RN04 | estado PRONTA; saldo ≥ preço; estoque da receita, do açúcar e de um copo | saldo −= preço; estoque −= consumo; INSERT do pedido EM_PREPARO com preço cobrado e previsão de término; estado = PREPARANDO |
| Concluir preparo | RN04, RN07 | pedido EM_PREPARO e previsão de término ≤ agora | pedido CONCLUIDO com instante; contador += 1; estado PRONTA ou AGUARDANDO_LIMPEZA |
| Cancelar pedido | RN05 | pedido EM_PREPARO e previsão de término > agora | pedido CANCELADO; saldo += preço cobrado; estado PRONTA |
| Devolver troco | RN06 | — | saldo = 0 |

Mecanismo:
- O serviço abre e fecha a transação (unidade de trabalho). Repositories recebem a conexão ou sessão e **nunca** fazem commit.
- Toda transação de escrita começa com `BEGIN IMMEDIATE`, que obtém o bloqueio de escrita do SQLite antes das leituras. Assim, dois pedidos simultâneos não leem PRONTA ao mesmo tempo.
- `COMMIT` ao final; qualquer exceção provoca `ROLLBACK`.
- `busy_timeout` configurado para que um segundo escritor espere em vez de falhar imediatamente.
- Na opção A, o driver pysqlite é configurado conforme a documentação do SQLAlchemy para SQLite (eventos `connect` e `begin`). Na opção B, a conexão usa controle manual de transação (`isolation_level=None` ou `autocommit=True` do Python 3.12) e emite `BEGIN IMMEDIATE` explicitamente.

Testes de integração obrigatórios (falham se a operação não for atômica):
- `test_order_rollback_on_midway_failure` (#9): substitui o repository de pedidos por um que lança exceção depois do débito de crédito e estoque. Por uma conexão nova, verifica que saldo, estoque, estado e quantidade de pedidos não mudaram.
- `test_cancel_rollback_on_midway_failure` (#11): injeta falha depois da restituição do crédito e verifica que o pedido continua EM_PREPARO e o saldo não mudou.
- `test_order_atomicity_and_concurrency` (#9): duas threads com conexões independentes pedem ao mesmo tempo; exatamente um pedido é aceito e o estoque é debitado uma vez.

Se cada repository fizesse commit por conta própria, o débito persistiria depois da falha injetada e os dois primeiros testes falhariam.

## Decisão
Pendente. Ao escolher: mudar o status para Aceito, registrar a opção aqui e atualizar o [índice](README.md). Na opção B, marcar o ADR 0001 como "Substituído parcialmente por 0002 (persistência)" e documentar o formato dos scripts de migração.

## Consequências
Comuns: serviços passam a depender de uma abstração de unidade de trabalho; testes de integração usam banco SQLite em arquivo temporário (não `:memory:`), para permitir conexões independentes.

## Referências
- [SQLAlchemy: SQLite, transações e `BEGIN IMMEDIATE`](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [Python: `sqlite3`, controle de transações](https://docs.python.org/3.12/library/sqlite3.html#transaction-control)
- [SQLite: `BEGIN IMMEDIATE`](https://www.sqlite.org/lang_transaction.html)
