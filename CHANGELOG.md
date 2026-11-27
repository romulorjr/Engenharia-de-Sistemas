# Changelog

Todas as mudanças relevantes deste projeto são registradas aqui.

O formato segue [Keep a Changelog 1.1.0](https://keepachangelog.com/pt-BR/1.1.0/) e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/). Cada PR adiciona suas entradas em `[Unreleased]`, nas seções Added, Changed, Deprecated, Removed, Fixed ou Security, citando a issue. Na entrega, `[Unreleased]` vira uma versão com data.

## [Unreleased]

### Added
- Seção "Nomenclatura (Naming)" no steering e no CONTEXT: domínio em português; termos técnicos, módulos, testes e commits em inglês (#2).
- Specs da #2 (`.kiro/specs/2-aplicacao-base/`) e da #3 (`.kiro/specs/3-ci-qualidade/`) com requisitos, design e tarefas, aguardando aprovação; nenhum código implementado (#2, #3).
- ADR 0006 (estratégia de testes e medição de cobertura), proposto na spec da #3 e aceito em 27/11/2026 com fixação só das dependências diretas, teste de camadas obrigatório e limites do Radon com aviso em classe C (#3, #20).
- Steering do Kiro em `.kiro/steering/project.md` com propósito, fontes da verdade, arquitetura, regras de documentação, convenções de branch/commit, specs e Definition of Done (#1).
- Hooks do Kiro em `.kiro/hooks/`: `docs-guard` (Stop) exige `CHANGELOG.md` e `docs/CONTEXT.md` quando `src/` ou `tests/` mudam; `quality-on-save` (PostFileSave) executa Ruff; `quality-on-stop` (Stop) executa Ruff e pytest quando há código alterado (#1).
- Scripts multiplataforma `scripts/kiro/docs_guard.py` e `scripts/kiro/quality_check.py`, usados pelos hooks e executáveis manualmente (#1).
- Este `CHANGELOG.md` (#1).
- Índice e modelo de ADR em `docs/adr/README.md` e `docs/adr/0000-modelo.md`, com a lista de decisões que ainda precisam de ADR (#1).
- Esqueleto do relatório de qualidade em `docs/quality-report.md`, sem métricas medidas (#20).
- Registro de contribuições e declarações individuais em `docs/contributions.md`, com contas GitHub a confirmar (#23).
- Relatório de estado de 25/11/2026 em `docs/CONTEXT.md` e replanejamento M1–M5 em `docs/plano-de-projeto.md` (#1).
- Licença MIT em `LICENSE`; o PDF da disciplina não é coberto (#1).
- ADR 0002 (persistência e atomicidade, proposto: aguarda opção A ou B), ADR 0003 (modelo de erros e mapeamento HTTP), ADR 0004 (JWT do operador) e ADR 0005 (representação monetária) (#4, #12, #18).
- Seção "Decisões de interpretação (25/11/2026)" em `docs/requisitos.md` com D-4a a D-4f e novas questões Q6–Q8 (#7, #11, #12, #17, #18).
- README: seções "Códigos de erro" e "Branching"; tabela de milestones M1–M5 (#1).
- Configuração de proteção de `main` em `.github/branch-protection-main.json`, a aplicar por administrador (#27).
- Milestones M1–M5 no GitHub com as issues vinculadas; issue #27 para a proteção de `main` (#1).
- Contrato OpenAPI parcial e planejado em `docs/api/openapi.yaml`: `GET /produtos` (definição de disponibilidade D-Q3) e `GET /operador/relatorio` (`from`/`to` com e sem fuso, exemplos), envelope de erro, dinheiro e JWT (#5, #17, #21).
- Decisões D-Q3 (disponibilidade), D-Q6 (fuso e validação do período), D-Q7 (`LIMITE_CREDITO_EXCEDIDO`) e D-Q8 (`PEDIDO_NAO_CANCELAVEL`) em `docs/requisitos.md` (#5, #7, #11, #17).
- Registro do checkpoint de 18/11 em `docs/checkpoint-18-11.md` (#22).
- Seção "Como executar" em `docs/configuracao-github.md`, com pré-requisitos (GitHub CLI com papel Admin, PowerShell 7) e comandos (#27).

### Changed
- Mensagens de commit passam a ser em inglês a partir de 27/11/2026 (steering, plano, README) (#2).
- Specs de #2 e #3 aprovadas; exceção de configuração renomeada de `ConfiguracaoInvalida` para `InvalidSettingsError` na spec da #2, pela convenção de nomes e pela regra N818 do Ruff (#2).
- `docs/CONTEXT.md` reorganizado nas seções Estado atual, Próximos passos, Decisões e Bloqueios (#1).
- `docs/rastreabilidade.md` passa a ter as colunas Implementação e Documentação (#1).
- `docs/requisitos.md` recebe opções e propostas para as questões em aberto, incluindo a nova questão 5 sobre códigos HTTP de operações do operador no estado errado (#1).
- Definition of Done de `docs/plano-de-projeto.md` inclui spec, camadas, CHANGELOG, CONTEXT, relatório de qualidade e contribuições (#1).
- Template de PR inclui spec, OpenAPI/Postman, CHANGELOG, CONTEXT, relatório de qualidade e contribuições (#1).
- README atualizado com estrutura, documentação obrigatória, hooks e status de 25/11/2026 (#1).
- Fluxo de branches: trabalho em `feature/`, `fix/`, `docs/` e `test/` a partir de `main`, com PR revisado para `main`; regra de re-escopo de milestone por issue nova (plano, steering, README) (#1).
- `.github/repository-setup.json` e `scripts/configure-github.ps1` passam a usar M1–M5 e a proteger só `main` (#1).
- `docs/configuracao-github.md` reescrito com o estado aplicado em 25/11 e o comando de proteção (#27).
- Matriz de rastreabilidade liga requisitos às decisões e ADRs e inclui os testes de rollback de #9 e #11 (#1).
- ADR 0002 aceito com a opção A (SQLAlchemy 2.x + Alembic); opção B (`sqlite3`) registrada como rejeitada (#4).
- ADR 0003 totalmente aceito: `LIMITE_CREDITO_EXCEDIDO` (400) e `PEDIDO_NAO_CANCELAVEL` (409) confirmados; códigos de crédito por estado (D-4a) confirmados (#7, #11, #18).
- Questões de requisitos Q1–Q8 todas resolvidas (#1).
- Contas GitHub dos integrantes confirmadas no README e em `docs/contributions.md` (#23).
- README, steering e CONTEXT informam que a ativação dos hooks do Kiro não foi verificada e que testes e análise estática devem ser executados à mão até a verificação (#1).
- Critérios de aceite de #4, #5, #7, #11, #17, #21 e #22 atualizados no plano (#1).

### Removed
- Branch `develop`, abandonada; preservada como a tag `archive/develop` (ce5eca4, já contida em `main`) (#1).

## [0.0.0] - 2026-10-14
Base de planejamento (commit d1d8c44, sem tag Git). Nenhuma funcionalidade implementada.

### Added
- Especificação em PDF, README, contexto, requisitos, plano de projeto, matriz de rastreabilidade, arquitetura planejada e ADR 0001 da stack (PR #25, #1).
- Templates de issue e PR, `repository-setup.json`, script `scripts/configure-github.ps1` e estrutura de pastas `src/` e `tests/` (PR #25, #1).

[Unreleased]: https://github.com/romulorjr/Engenharia-de-Sistemas/compare/d1d8c44...HEAD
[0.0.0]: https://github.com/romulorjr/Engenharia-de-Sistemas/commit/d1d8c44
