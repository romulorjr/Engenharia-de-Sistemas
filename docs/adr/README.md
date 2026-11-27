# Registros de decisão de arquitetura (ADR)

Um ADR por decisão significativa: stack, banco, autenticação, modelo de erros, padrões de projeto, estratégia de testes. Decisões pequenas e reversíveis ficam em [CONTEXT](../CONTEXT.md), seção "Decisões".

## Como registrar
1. Copie [0000-modelo.md](0000-modelo.md) para `NNNN-titulo-curto.md`, com o próximo número livre.
2. Preencha Contexto, Decisão, Consequências e Alternativas. Cite o requisito (RNxx/ENG-xx) e a issue.
3. Abra o ADR com status **Proposto** no mesmo PR da mudança ou antes dela. Passa a **Aceito** quando o grupo aprova o PR ou o responsável confirma a decisão.
4. Não reescreva ADR aceito. Para mudar a decisão, crie outro ADR e marque o antigo como **Substituído por NNNN**.
5. Registre a entrada no [CHANGELOG](../../CHANGELOG.md) (seção Changed ou Added) e no índice abaixo.

## Índice
| ADR | Título | Status | Data |
|---|---|---|---|
| [0001](0001-escolha-da-stack.md) | Stack do MVP | Aceito (decisão inicial, revisável) | 14/10/2026 |
| [0002](0002-persistencia-e-atomicidade.md) | Persistência e atomicidade das operações (SQLAlchemy + Alembic) | Aceito (opção A) em 26/11/2026 | 25/11/2026 |
| [0003](0003-modelo-de-erros.md) | Modelo de erros e mapeamento HTTP | Aceito | 25/11/2026 |
| [0004](0004-autenticacao-operador-jwt.md) | Autenticação do operador por JWT | Aceito | 25/11/2026 |
| [0005](0005-representacao-monetaria.md) | Representação monetária | Aceito | 25/11/2026 |
| [0006](0006-estrategia-de-testes.md) | Estratégia de testes e medição de cobertura | Proposto (spec da #3) | 26/11/2026 |

## Decisões que ainda precisam de ADR
Lista mantida até cada decisão ser tomada; ver issue indicada.

| Tema | Issue | Situação |
|---|---|---|
| Controle de estados: padrão State ou enum + tabela de transições | #10 | A propor na spec de #10 |
