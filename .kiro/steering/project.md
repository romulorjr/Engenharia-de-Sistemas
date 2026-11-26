---
inclusion: always
---

# Máquina de Café ESI — regras do projeto

## Propósito
Back-end de uma máquina de café automática (disciplina ESI, EACH-USP), entregue como API REST. Objetivo do PDF: poucas funcionalidades, funcionando, testadas e bem escritas, com evidência de participação de todos os integrantes. Prazo final: 09/12/2026.

## Fontes da verdade (nesta ordem)
1. `ESI - projeto maquina-cafe.pdf` — especificação oficial. Não inventar requisitos.
2. `docs/requisitos.md` — transcrição do PDF, identificadores (RN01–RN12, CAT01, EST01, ENG-*, E01–E07) e questões em aberto.
3. `docs/adr/` — decisões aceitas. `docs/adr/0001-escolha-da-stack.md` define a stack.
4. `docs/CONTEXT.md` — estado atual, próximos passos, decisões e bloqueios.
5. `docs/plano-de-projeto.md` e `docs/rastreabilidade.md` — backlog, milestones, Definition of Done e matriz.

Se o PDF for ambíguo, registrar a dúvida em `docs/requisitos.md` e perguntar ao responsável antes de decidir.

## Arquitetura
- Camadas em `src/maquina_cafe/`: `api/` (controllers: recebem requisição, validam formato, chamam serviço, produzem resposta HTTP), `services/` (coordenam regras RN01–RN12 e transações), `domain/` (entidades, receitas, estados, transições, valores), `persistence/` (repositories e acesso ao banco).
- Regras de negócio nunca ficam em controllers nem em SQL/repositories.
- Dinheiro em centavos inteiros internamente; reais com duas casas no JSON (`docs/adr/0005-representacao-monetaria.md`). Relógio injetável; testes sem `sleep`.
- Operações que alteram crédito, estoque, pedido e estado são atômicas (uma transação), com as fronteiras do `docs/adr/0002-persistencia-e-atomicidade.md`. Repositories não fazem commit.
- Erros no envelope `{"erro", "mensagem"}` e mapeamento HTTP do `docs/adr/0003-modelo-de-erros.md`; serviços lançam exceções de domínio, só `api/` conhece HTTP.
- Operador autenticado por JWT de 1 hora (`docs/adr/0004-autenticacao-operador-jwt.md`).
- Decisões de interpretação do PDF (D-4a a D-4f) em `docs/requisitos.md` valem como requisito.
- Padrões de projeto só com problema real, justificados em ADR e no documento de projeto.
- Mudança de stack, banco ou arquitetura exige ADR com status Proposto e confirmação do responsável antes de implementar.

## Regras de documentação (obrigatórias em toda mudança)
1. `README.md`: setup, execução, testes, análise estática, tabela de endpoints, regras resumidas, stack, status, como contribuir.
2. `docs/CONTEXT.md`: atualizar "Estado atual", "Próximos passos", "Decisões" e "Bloqueios" ao fim de cada sessão.
3. `docs/plano-de-projeto.md`: fases, milestones, backlog, Definition of Done; `docs/rastreabilidade.md`: requisito → issue → implementação → teste → documentação.
4. `CHANGELOG.md` (Keep a Changelog): toda mudança visível ou arquitetural entra em `[Unreleased]` (Added/Changed/Deprecated/Removed/Fixed/Security).
5. `docs/adr/NNNN-titulo.md`: uma por decisão significativa (Contexto, Decisão, Consequências, Alternativas); atualizar `docs/adr/README.md`.
6. Documentação da API (OpenAPI gerado pelo FastAPI e exportado em `docs/api/`, coleção Postman) sincronizada com cada endpoint, com exemplos e códigos de erro.
7. Testes automatizados (unitários e de integração) para todo comportamento novo; atualizar cobertura em `docs/quality-report.md`.
8. Diagrama de classes/componentes (Mermaid, até uma página) em `docs/arquitetura.md`, coerente com o código.
9. `docs/quality-report.md`: cobertura, análise estática e code smells por milestone, apenas com números medidos.
10. `docs/contributions.md`: uma linha por PR/mudança relevante, com autor dos commits e quem solicitou.

Sempre atualizar a documentação junto com a mudança, no mesmo PR. Não declarar como implementado, testado ou medido o que não foi.

## Branches, commits e PRs
- `main` é a única branch de longa duração; nunca commitar direto nela (proteção no GitHub: issue #27). Não existe `develop` (arquivada como tag `archive/develop`).
- Branches partem de `main`: `feature/<issue>-<resumo>`, `fix/<issue>-<resumo>`, `docs/<resumo>`, `test/<issue>-<resumo>`. PR sempre para `main`.
- Milestones M1–M5 são fixos: re-escopo exige issue nova, nunca mover issues de milestone silenciosamente.
- Conventional Commits em português, sem acentos no assunto: `feat(credito): validar denominacoes aceitas`, rodapé `Refs #7`. Tipos: feat, fix, docs, test, refactor, chore, ci.
- Commits pequenos e atômicos. Um PR por issue quando possível, usando `.github/PULL_REQUEST_TEMPLATE.md`.
- PR revisado por outro integrante e com CI verde antes do merge.

## Specs
Cada funcionalidade ou refatoração tem spec em `.kiro/specs/<issue>-<resumo>/` com `requirements.md` (histórias e critérios EARS citando RNxx e a issue), `design.md` (camadas, modelos, erros, testes) e `tasks.md` (tarefas com referência aos requisitos). A spec é versionada no mesmo PR da implementação.

## Definition of Done
- Código nas camadas corretas; regras RNxx rastreáveis até teste.
- Testes automatizados passam; cobertura global ≥ 75% sem exclusões artificiais.
- `ruff check` e `ruff format --check` sem erros; nenhum problema crítico novo no Radon.
- OpenAPI/Postman atualizados quando a API muda.
- README, CONTEXT, CHANGELOG, ADR (se aplicável), matriz de rastreabilidade e contribuições atualizados.
- PR aberto com descrição clara e vínculo com a issue.

## Hooks do Kiro
`.kiro/hooks/` executa `scripts/kiro/quality_check.py` (lint, formatação e testes) e `scripts/kiro/docs_guard.py` (exige CHANGELOG e CONTEXT quando `src/` ou `tests/` mudam). Os comandos supõem a raiz do repositório como diretório de trabalho.

A ativação dos hooks não foi verificada (ver `docs/CONTEXT.md`, Bloqueios). Até lá, antes de encerrar uma mudança, executar à mão `python scripts/kiro/docs_guard.py` e `python scripts/kiro/quality_check.py` na raiz do repositório, e tratar a CI como verificação obrigatória.
