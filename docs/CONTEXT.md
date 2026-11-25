# Contexto do projeto

Arquivo vivo. Atualizar "Estado atual", "Próximos passos", "Decisões" e "Bloqueios" ao fim de cada sessão de trabalho. Última atualização: 25/11/2026.

Fonte normativa: [ESI - projeto maquina-cafe.pdf](../ESI%20-%20projeto%20maquina-cafe.pdf). Este documento registra estado e decisões; não substitui a especificação. Regras de trabalho do agente e da equipe: [.kiro/steering/project.md](../.kiro/steering/project.md).

## Escopo confirmado
Back-end de uma máquina de café, preferencialmente API REST; sem interface gráfica ou hardware. Cinco bebidas, seis reservatórios, crédito, pedidos, quatro estados, operador e relatórios. RN01–RN12, banco persistente, testes unitários e de integração, cobertura mínima de 75%, análise estática, documentação e sete artefatos finais. O PDF permite selecionar as regras viáveis no prazo e, se HTTP não for viável, uma classe de entrada local.

## Equipe (ordem alfabética)
Bruno de Andrade Gama Kraker, Pedro Henryk Bezerra Souza, Rodrigo Franco de Moraes, Rômulo Maurício Fonseca Júnior, Thales Iamamura. Contas GitHub prováveis e papéis em [contribuições](contributions.md), ainda a confirmar.

## Estado atual (25/11/2026)
Relatório de estado produzido nesta data.

**Feito**
- Documentação de planejamento: README, requisitos, plano, rastreabilidade, arquitetura planejada, ADR 0001 (stack), configuração GitHub, templates de issue/PR, `.gitignore` e pastas vazias em `src/` e `tests/`.
- Issues #1–#24 criadas em 14/10, todas abertas, sem responsável, label ou milestone. PR #25 (planejamento) mesclado em `main` em 14/10.
- Nesta sessão: steering e hooks do Kiro, CHANGELOG, índice e modelo de ADR, esqueletos de relatório de qualidade e contribuições, checklist de documentação no template de PR ([PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26), issue #1).

**Não existe ainda**
- Código de aplicação, `pyproject.toml`/dependências, banco e migrações, testes, CI, configuração de Ruff/Radon, OpenAPI exportado ou coleção Postman.
- Labels e milestones do plano (o repositório tem apenas as labels padrão do GitHub); proteção de branches; workflows do GitHub Actions.
- `develop` está atrás de `main`: não contém o PR #25.
- Histórico do Git com um único autor humano (romulorjr).

**Situação frente à especificação**
| Item do PDF | Situação |
|---|---|
| RN01–RN12 | Nenhuma implementada |
| 14 endpoints mínimos | 0 implementados |
| Estados PRONTA / PREPARANDO / AGUARDANDO_LIMPEZA / MANUTENCAO | Não implementados |
| Persistência (estoque, crédito, estado, pedidos) | Não implementada |
| Validação e erros padronizados | Não implementados |
| Swagger/OpenAPI ou Postman | Inexistente |
| Testes e cobertura ≥ 75% | 0 testes; cobertura não medida |
| Análise estática com métricas | Não configurada |
| Padrões de projeto e diagrama | Apenas proposta em [arquitetura](arquitetura.md) e ADR 0001 |
| E01 README | Parcial: sem instruções executáveis |
| E02 API + documentação | Ausente |
| E03 relatório de qualidade | Esqueleto em [quality-report.md](quality-report.md) |
| E04 documento de projeto | Ausente |
| E05 histórico de contribuições | Um autor humano |
| E06 declarações | Esqueleto em [contributions.md](contributions.md) |
| E07 vídeo | Ausente |

**Prazos:** o checkpoint de 18/11 já passou e a issue #22 continua aberta. Faltam 14 dias para a entrega de 09/12. Os milestones das Fases 1–3 (25/10, 01/11, 18/11) estão vencidos sem entregas de código.

## Próximos passos
Dependem da confirmação do responsável sobre o [replanejamento proposto](plano-de-projeto.md#replanejamento-proposto-em-25112026).
1. Revisar e mesclar o [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26) (#1), com aprovação de outro integrante.
2. Responder às questões de requisitos e às decisões pendentes listadas abaixo.
3. Base técnica: #2 (aplicação e dependências), #3 (CI, cobertura e Ruff/Radon), #4 (banco e inicialização idempotente), modelo de erros de #18.
4. Fluxo do cliente do exemplo do PDF: #5, #7, #8, #9, #10, #11.
5. Operador: #12, #6, #13, #15, #14, #16, #17 e recuperação após reinício (#19).
6. Qualidade e entregáveis: #20, #21, #23, #24.

## Decisões
| Data | Decisão | Registro |
|---|---|---|
| 14/10/2026 | Stack Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, SQLite, pytest, Ruff, Radon | [ADR 0001](adr/0001-escolha-da-stack.md) |
| 14/10/2026 | Checkpoint 18/11/2026 e entrega 09/12/2026; fuso America/Sao_Paulo | Este arquivo |
| 25/11/2026 | Documentação obrigatória em todo PR: README, CONTEXT, plano, CHANGELOG, ADR, OpenAPI/Postman, testes, diagrama, relatório de qualidade e contribuições | [steering](../.kiro/steering/project.md) |
| 25/11/2026 | Hooks do Kiro versionados em `.kiro/hooks/`, com scripts Python multiplataforma em `scripts/kiro/` | [CHANGELOG](../CHANGELOG.md) |
| 25/11/2026 | Commits gerados pelo agente aparecem com autor `Kiro Agent` e são registrados com quem os solicitou | [contribuições](contributions.md) |

**Decisões pendentes (aguardando o responsável)**
1. Aprovar o replanejamento e criar milestones novos com as datas propostas.
2. Fluxo de branches: sincronizar `develop` com `main` e manter GitFlow, ou usar apenas `feature/*` → `main` com PR revisado até a entrega.
3. Persistência: manter SQLAlchemy + Alembic (ADR 0001) ou usar `sqlite3` da biblioteca padrão com repositories e migrações SQL versionadas (exigiria ADR 0002).
4. Questões de requisitos 1–4 de [requisitos.md](requisitos.md#questões-a-resolver-antes-das-respectivas-implementações).
5. Confirmar contas GitHub e distribuição de issues entre os cinco integrantes.
6. Situação da issue #22: o checkpoint de 18/11 aconteceu? O que foi apresentado?
7. Licença do repositório (pendente desde 14/10; nenhum LICENSE adicionado).

## Bloqueios
| Bloqueio | Efeito | Mitigação |
|---|---|---|
| Ambiente do agente (Kiro Web) sem acesso ao PyPI | O agente não consegue instalar FastAPI, SQLAlchemy, pytest-cov nem Radon; só `pytest` e `ruff` estão disponíveis localmente | Validar pela CI do GitHub Actions (#3), cujos logs o agente lê; os integrantes executam localmente com acesso à internet |
| Prazo de 14 dias sem código | Risco de não cobrir RN01–RN12 com testes | Fluxo vertical primeiro; linha de corte proposta no plano |
| Participação concentrada em uma conta | Risco para E05/E06 | Distribuir issues e revisões imediatamente |
| Questões de requisitos abertas | Bloqueiam #7, #11, #12, #16, #17, #18 | Respostas do responsável antes de cada issue |

## Trabalho contínuo
Ler este arquivo, o [plano](plano-de-projeto.md) e o [steering](../.kiro/steering/project.md) antes de mudanças. Conventional Commits e rastreabilidade requisito → issue → implementação → teste → documentação. Alterações funcionais atualizam testes e documentação no mesmo PR. Não modificar referências sincronizadas sob `sources/` no ambiente do projeto (instrução registrada em 14/10).
