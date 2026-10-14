# ADR 0001 — Stack do MVP

Data: 14/10/2026. Status: decisão inicial para implementação, revisável pelo grupo. A escolha foi delegada sem restrições tecnológicas; a experiência dos integrantes ainda não foi informada.

## Contexto e critérios
Entrega em 09/12/2026 com checkpoint em 18/11. Priorizar execução local simples, documentação HTTP, testes, persistência transacional, legibilidade e baixo custo de configuração. Não supor experiência prévia do grupo.

| Alternativa | Benefícios | Custos no contexto |
|---|---|---|
| Python + FastAPI + SQLAlchemy + SQLite | OpenAPI integrado, testes com pytest, banco local sem serviço externo | Tipagem exige disciplina; transações SQLite precisam ser configuradas e testadas |
| Java + Spring Boot + JPA | Tipagem estática, ecossistema integrado | Mais configuração inicial e conceitos de framework |
| TypeScript + NestJS + ORM relacional | Tipagem e módulos explícitos | Mais ferramentas no início; escolher e integrar ORM |
| Código local sem HTTP | Menor infraestrutura | Exige adaptar contrato e demonstração; opção de contingência permitida pelo PDF |

## Decisão
Python 3.12 como versão-base planejada; FastAPI com Pydantic e Uvicorn; SQLAlchemy 2.x síncrono; Alembic para migrações; SQLite em arquivo. pytest, pytest-cov e HTTPX para testes; Ruff para lint/formatação e Radon para métricas de complexidade. Versões exatas e compatibilidade serão verificadas e fixadas na issue de infraestrutura; não há dependências instaladas ou validadas neste PR.

SQLite atende à demonstração de uma máquina sem provisionar servidor. Operações que alteram crédito, estoque, pedido e estado devem ser atômicas; serialização das escritas e recuperação exigem testes com conexões independentes. Não usar apenas um lock em memória como garantia. Reavaliar PostgreSQL se houver múltiplos processos/clientes ou contenção incompatível com a demonstração.

## Arquitetura e consequências
Controllers finos → serviços/domínio → persistência. Dinheiro em centavos inteiros, evitando ponto flutuante binário. Relógio injetável para testes rápidos de preparo. Manter o preço cobrado no pedido. Banco não deve ser recriado a cada início.
Não adotar infraestrutura distribuída, filas ou frontend neste escopo. A escolha reduz preparação operacional, mas requer cuidado explícito com concorrência e tipos monetários.

## Padrões
Considerar Repository para isolar consultas e transações, sem interface genérica obrigatória. Para estados, começar com enum e tabela de transições; avaliar State apenas se simplificar o código. Strategy e Factory não serão introduzidos sem variação real. Registrar problema, benefícios, custos e decisão final no documento de projeto.

## Referências oficiais consultadas
- [FastAPI: recursos/OpenAPI](https://fastapi.tiangolo.com/features/)
- [FastAPI: testes](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy: SQLite e transações](https://docs.sqlalchemy.org/en/20/dialects/sqlite.html)
- [Ruff: análise](https://docs.astral.sh/ruff/linter/) e [formatação](https://docs.astral.sh/ruff/formatter/)
