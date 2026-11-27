# Contexto do projeto

Arquivo vivo. Atualizar "Estado atual", "Próximos passos", "Decisões" e "Bloqueios" ao fim de cada sessão de trabalho. Última atualização: 27/11/2026.

Fonte normativa: [ESI - projeto maquina-cafe.pdf](../ESI%20-%20projeto%20maquina-cafe.pdf). Este documento registra estado e decisões; não substitui a especificação. Regras de trabalho do agente e da equipe: [.kiro/steering/project.md](../.kiro/steering/project.md).

## Escopo confirmado
Back-end de uma máquina de café, preferencialmente API REST; sem interface gráfica ou hardware. Cinco bebidas, seis reservatórios, crédito, pedidos, quatro estados, operador e relatórios. RN01–RN12, banco persistente, testes unitários e de integração, cobertura mínima de 75%, análise estática, documentação e sete artefatos finais. O PDF permite selecionar as regras viáveis no prazo e, se HTTP não for viável, uma classe de entrada local.

## Equipe (ordem alfabética)
Bruno de Andrade Gama Kraker, Pedro Henryk Bezerra Souza, Rodrigo Franco de Moraes, Rômulo Maurício Fonseca Júnior, Thales Iamamura. Contas GitHub confirmadas em 25/11/2026 em [contribuições](contributions.md); papéis a definir.

## Nomenclatura (Naming)
Decidida pelo responsável em 27/11/2026; regra completa no [steering](../.kiro/steering/project.md#nomenclatura-naming).
- Português para nomes do domínio do PDF (bebida, pedido, credito, estoque, estado, receita, reservatorio).
- Inglês para termos técnicos (Repository, Service, Controller, Settings, app factory), nomes de arquivos e módulos de código, nomes de testes e mensagens de commit.
- Documentação, docstrings, comentários e mensagens ao usuário continuam em português.

## Estado atual
Relatório de estado produzido em 25/11/2026 e atualizado em 27/11/2026, depois da implementação de #2 e #3.

**Feito**
- Planejamento de 14/10 (PR #25).
- [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26), mesclado em `main` em 26/11 às 16:47 (Brasília) pelo responsável, **sem revisão de outro integrante**: governança, steering e hooks do Kiro, CHANGELOG, ADRs 0001–0005, decisões D-4a a D-4f e D-Q3/Q6/Q7/Q8, contrato OpenAPI parcial, registro do checkpoint, licença MIT.
- [PR #28](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/28) (specs de #2 e #3, ADR 0006), mesclado em 26/11 às 16:49, também sem revisão, na branch `docs/governanca-documentacao-kiro`, que já tinha sido mesclada em `main`. Por isso as specs **não chegaram a `main`**; elas entram pelo PR #29.
- [PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29), branch `feature/2-3-app-base-ci`, criada a partir de `main` porque o PR #28 já estava fechado:
  - #2: `pyproject.toml` com dependências diretas fixadas, pacote `maquina_cafe` em camadas, `Settings`/`InvalidSettingsError`, `create_app`, `.env.example`;
  - #3: workflow `.github/workflows/ci.yml` (job `testes-e-analise`), configuração de pytest, coverage e Ruff, `scripts/ci/` (Radon com aviso em C e falha em D+/MI < A, fumaça com uvicorn, resumo), teste de camadas;
  - specs de #2 e #3 aprovadas e ADR 0006 aceito;
  - CI verde, mas o PR continua como rascunho: marcar como pronto para revisão só existe na API GraphQL, que a integração do agente não alcança (HTTP 400). O responsável clica em "Ready for review".
- CI do PR #29: run verde [46014939322](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46014939322) com 46 testes, cobertura 100% (linhas 33/33, ramos 4/4), Ruff sem erros, Radon CC média A (2,2) sem avisos e MI A em todos os módulos, fumaça OK. Run vermelho provocado [46015179174](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46015179174) prova que um teste quebrado falha o job.
- No GitHub: milestones M1–M5 e vínculos; `develop` arquivada; #22 fechada; [#30](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/30) aberta (aviso de depreciação do Starlette, sem milestone).

**Não existe ainda**
- Regras RN01–RN12, endpoints do PDF, banco e migrações (#4), contrato de erro (#18), coleção Postman.
- Proteção efetiva de `main`: o ruleset "Proteção da Main" do responsável não se aplica a nenhuma branch, e o agente não pode editá-lo (#27).
- Labels do plano. Histórico do Git com um único autor humano (romulorjr) e nenhuma revisão de PR registrada.

**Situação frente à especificação**
| Item do PDF | Situação |
|---|---|
| RN01–RN12 | Nenhuma implementada; interpretações decididas |
| 14 endpoints mínimos | 0 implementados; 2 descritos no contrato parcial |
| Estados PRONTA / PREPARANDO / AGUARDANDO_LIMPEZA / MANUTENCAO | Não implementados |
| Persistência | Não implementada; SQLAlchemy + Alembic decididos (ADR 0002); `Settings.database_url` pronto para a #4 |
| Validação e erros padronizados | Não implementados; contrato decidido (ADR 0003) |
| Swagger/OpenAPI ou Postman | Swagger da aplicação base em `/docs`; contrato parcial planejado em `docs/api/openapi.yaml` |
| Testes e cobertura ≥ 75% | 46 testes na CI, cobertura 100% do código atual (aplicação base) |
| Análise estática com métricas | Ruff e Radon na CI com limites; relatório em [quality-report.md](quality-report.md) |
| Padrões de projeto e diagrama | Repository e unidade de trabalho decididos (ADR 0002); diagrama do implementado em [arquitetura](arquitetura.md); State a decidir em #10 |
| E01 README | Instruções de execução, testes e análise estática; comandos de Windows não executados por um integrante |
| E02 API + documentação | Aplicação base com Swagger; sem endpoints do PDF |
| E03 relatório de qualidade | Primeira medição real em [quality-report.md](quality-report.md) |
| E04 documento de projeto | Ausente |
| E05 histórico de contribuições | Um autor humano; nenhuma revisão |
| E06 declarações | Esqueleto em [contributions.md](contributions.md) |
| E07 vídeo | Ausente |

**Prazos:** em 27/11 faltam 12 dias para 09/12. M1 vence hoje: #2 e #3 estão prontas para revisão no PR #29; #4 e #18 não começaram; #27 depende do administrador; #1 pode ser fechada (PR #26 mesclado). M1 não fecha hoje.

## Próximos passos
1. Responsável: marcar o [PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29) como "Ready for review". Outro integrante: revisar e aprovar; mesclar só depois da aprovação. Revisar também, mesmo depois do merge, os PRs #26 e #28, para que a revisão fique registrada (E05).
2. Responsável: aplicar `.github/ruleset-main.json` ao ruleset existente ([#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27); comando em [configuração do GitHub](configuracao-github.md#como-executar)); decidir se mantém o bypass da integração.
3. Responsável: executar `scripts/configure-github.ps1 -Apply` (labels) e registrar o resultado.
4. Integrante com Windows: executar os comandos de PowerShell do README e registrar o resultado no PR #29.
5. Agente, com autorização: spec e implementação de #4 (banco, migrações, inicialização idempotente) e do contrato de erro da #18, que completam M1.
6. Grupo: preencher [checkpoint-18-11.md](checkpoint-18-11.md); distribuir as issues de M2 (#5, #7, #8, #9, #10, #11); decidir o milestone da #30.
7. Verificar a ativação dos hooks do Kiro em uma sessão nova (ver Bloqueios).

## Decisões
| Data | Decisão | Registro |
|---|---|---|
| 14/10/2026 | Stack Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, SQLite, pytest, Ruff, Radon | [ADR 0001](adr/0001-escolha-da-stack.md) |
| 14/10/2026 | Checkpoint 18/11/2026 e entrega 09/12/2026; fuso America/Sao_Paulo | Este arquivo |
| 25/11/2026 | Documentação obrigatória em todo PR: README, CONTEXT, plano, CHANGELOG, ADR, OpenAPI/Postman, testes, diagrama, relatório de qualidade e contribuições | [steering](../.kiro/steering/project.md) |
| 25/11/2026 | Hooks do Kiro versionados em `.kiro/hooks/`, com scripts Python multiplataforma em `scripts/kiro/` | [CHANGELOG](../CHANGELOG.md) |
| 25/11/2026 | Commits gerados pelo agente aparecem com autor `Kiro Agent` e são registrados com quem os solicitou | [contribuições](contributions.md) |
| 25/11/2026 | Replanejamento M1–M5 aprovado; re-escopo de milestone exige issue nova; #1, #18, #27 em M1, #23 em M5, #22 sem milestone | [plano](plano-de-projeto.md#replanejamento-aprovado-em-25112026) |
| 25/11/2026 | `develop` abandonada (tag `archive/develop`); branches `feature/`, `fix/`, `docs/`, `test/` a partir de `main`; PR revisado para `main`; `main` protegida com CI obrigatória | [plano](plano-de-projeto.md#branches-commits-e-prs), README "Branching", #27 |
| 26/11/2026 | Persistência: opção A, SQLAlchemy 2.x + Alembic; opção B (`sqlite3`) rejeitada; transações `BEGIN IMMEDIATE` na camada de serviços | [ADR 0002](adr/0002-persistencia-e-atomicidade.md) |
| 25/11/2026 | D-4a: crédito só em PRONTA (409 `MAQUINA_OCUPADA` em PREPARANDO, 503 em MANUTENCAO/AGUARDANDO_LIMPEZA); troco em qualquer estado. Códigos confirmados em 26/11 | [requisitos](requisitos.md#decisões-de-interpretação-25112026), [ADR 0003](adr/0003-modelo-de-erros.md) |
| 25/11/2026 | D-4b: saldo nunca passa de R$ 50; inserção excedente rejeitada inteira | requisitos, ADR 0003 |
| 25/11/2026 | D-4c: relatório com `from`/`to` ISO 8601, obrigatórios e inclusivos; 400 se ausente ou inválido | requisitos |
| 25/11/2026 | D-4d: JWT HS256 de 1 hora; credenciais e segredo por ambiente; 401 sem token válido | [ADR 0004](adr/0004-autenticacao-operador-jwt.md) |
| 25/11/2026 | D-4e: reais com duas casas no JSON; centavos internamente | [ADR 0005](adr/0005-representacao-monetaria.md) |
| 25/11/2026 | D-4f: 409 `ESTADO_INVALIDO` para operador no estado errado; 503 só para o cliente | ADR 0003 |
| 26/11/2026 | D-Q3: `disponivel` = estoque para uma unidade (receita, açúcar da receita = 0 g) e 1 copo; crédito e estado fora do cálculo | requisitos, [openapi.yaml](api/openapi.yaml) |
| 26/11/2026 | D-Q6: `from`/`to` com ou sem fuso; sem fuso = UTC−03:00; `Z` e deslocamentos aceitos; data sem hora e `from` > `to` → 400; só CONCLUIDO pelo instante de conclusão | requisitos, openapi.yaml |
| 26/11/2026 | D-Q7: 400 `LIMITE_CREDITO_EXCEDIDO`, inserção inteira rejeitada | requisitos, ADR 0003 |
| 26/11/2026 | D-Q8: 409 `PEDIDO_NAO_CANCELAVEL` para pedido CONCLUIDO ou CANCELADO | requisitos, ADR 0003 |
| 25/11/2026 | Licença MIT para os cinco integrantes; PDF da disciplina não coberto (confirmado em 26/11) | [LICENSE](../LICENSE) |
| 26/11/2026 | Contas GitHub confirmadas; arquivo mantém o nome `docs/contributions.md` | [contribuições](contributions.md) |
| 26/11/2026 | Checkpoint de 18/11 realizado; #22 fechada com registro | [checkpoint-18-11.md](checkpoint-18-11.md) |
| 26/11/2026 | Contrato OpenAPI parcial escrito à mão em `docs/api/openapi.yaml` até a #21, que o substitui pelo OpenAPI gerado | openapi.yaml |
| 27/11/2026 | Specs de #2 e #3 aprovadas; #2 e #3 implementadas juntas em um PR, por causa da limitação do ambiente do agente | [spec #2](../.kiro/specs/2-aplicacao-base/requirements.md), [spec #3](../.kiro/specs/3-ci-qualidade/requirements.md) |
| 27/11/2026 | Nomenclatura: domínio em português; termos técnicos, arquivos e módulos de código, testes e commits em inglês | [Nomenclatura](#nomenclatura-naming), steering |
| 27/11/2026 | Dependências diretas fixadas com `==`; indiretas pelo pip; Python 3.12 fixo na CI; lock com hashes fora do escopo | [ADR 0006](adr/0006-estrategia-de-testes.md) |
| 27/11/2026 | Teste de camadas mantido; falha é regressão real | ADR 0006 |
| 27/11/2026 | Radon: falha em CC classe D+ e MI abaixo de A; aviso em CC classe C; limites não são reduzidos para a CI passar | ADR 0006 |
| 27/11/2026 | ADR 0006 (estratégia de testes) aceito | ADR 0006 |
| 27/11/2026 | Implementação de #2 e #3 em branch nova (`feature/2-3-app-base-ci`, PR #29), porque o PR #28 já estava fechado; as specs entram em `main` por esse PR | PR #29 |
| 27/11/2026 | Proteção de `main` pelo ruleset existente, com PR obrigatório, check `testes-e-analise` fixado no app GitHub Actions e sem bypass (proposta do agente, a aplicar pelo responsável) | [configuração do GitHub](configuracao-github.md#proteção-de-main), `.github/ruleset-main.json` |

**Decisões pendentes (aguardando o responsável)**
1. Bypass do ruleset: remover (recomendado) ou trocar para "pull_request".
2. Distribuição das issues entre os cinco integrantes.
3. Conteúdo do registro do checkpoint: o que foi apresentado e o retorno do docente.
4. Milestone da [#30](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/30) (httpx2): entrar em M4 ou ficar fora do prazo.
5. Nome das exceções de domínio (português com sufixo `Error` ou desligar a regra N818 do Ruff), a decidir na #18.

## Bloqueios
| Bloqueio | Efeito | Mitigação |
|---|---|---|
| **Hooks do Kiro não estão ativos (não verificados)** | Nenhuma evidência de carregamento até 27/11: nenhuma saída de hook apareceu nesta sessão. O Kiro lê os hooks ao iniciar a sessão, e os de `.kiro/hooks/` foram criados durante uma sessão aberta. No Kiro Web o workspace é `/projects/sandbox` e o repositório fica na subpasta `Engenharia-de-Sistemas/`: executados a partir da raiz do workspace, `python scripts/kiro/docs_guard.py` e `python scripts/kiro/quality_check.py` não encontram os arquivos e terminam com código 2, sem efeito em gatilhos Stop (testado em 26/11). | **Até corrigir, testes e análise estática devem ser executados à mão** na raiz do repositório (comandos do README) e a CI (`testes-e-analise`) é a verificação obrigatória. Verificar em sessão nova: no Kiro IDE, abrir a pasta do repositório como raiz e conferir os hooks no painel do Kiro; no Kiro Web, conferir se uma alteração em `src/` sem CHANGELOG faz o `docs-guard` manter o agente trabalhando. Se não carregarem, ajustar o diretório dos comandos e registrar aqui |
| Proteção de `main` exige administrador | O agente recebe HTTP 403 ao editar rulesets e proteção clássica, mesmo com o bypass do ruleset; o ruleset atual não se aplica a nenhuma branch | Responsável aplica `.github/ruleset-main.json` (#27). Até lá, a regra "sem merge sem revisão" vale só por acordo, e os PRs #26 e #28 foram mesclados sem revisão |
| Ambiente do agente (Kiro Web) sem acesso ao PyPI | O agente não instala FastAPI, Radon nem pytest-cov; roda localmente só Ruff e os testes unitários que não dependem de FastAPI | CI do GitHub Actions, cujos logs e artefatos o agente lê pela API. A stack não muda por causa disso (ADR 0002) |
| API GraphQL indisponível para o agente | O agente não marca PRs como prontos para revisão (`gh pr ready` e `markPullRequestReadyForReview` retornam HTTP 400) | Responsável marca pela interface |
| PowerShell indisponível no ambiente do agente | `scripts/configure-github.ps1` alterado e não executado | Responsável executa localmente ([Como executar](configuracao-github.md#como-executar)) |
| Prazo de 12 dias, sem regra de negócio implementada | Risco de não cobrir RN01–RN12 com testes | Fluxo vertical primeiro; linha de corte no plano |
| Participação concentrada em uma conta e sem revisões | Risco para E05/E06 | Revisões dos PRs #26, #28 e #29 por outros integrantes; distribuir as issues de M2 |

## Trabalho contínuo
Ler este arquivo, o [plano](plano-de-projeto.md) e o [steering](../.kiro/steering/project.md) antes de mudanças. Conventional Commits e rastreabilidade requisito → issue → implementação → teste → documentação. Alterações funcionais atualizam testes e documentação no mesmo PR. Não modificar referências sincronizadas sob `sources/` no ambiente do projeto (instrução registrada em 14/10).
