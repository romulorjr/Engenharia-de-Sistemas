# Contexto do projeto

Arquivo vivo. Atualizar "Estado atual", "Próximos passos", "Decisões" e "Bloqueios" ao fim de cada sessão de trabalho. Última atualização: 26/11/2026.

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
Relatório de estado produzido em 25/11/2026 e atualizado em 26/11/2026, depois das duas rodadas de decisões do responsável (25/11 e 26/11).

**Feito**
- Documentação de planejamento de 14/10 (PR #25): README, requisitos, plano, rastreabilidade, arquitetura planejada, ADR 0001, configuração GitHub, templates, `.gitignore` e pastas vazias em `src/` e `tests/`.
- [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26) (aberto, aguardando revisão), issue #1:
  - steering e hooks do Kiro, CHANGELOG, índice e modelo de ADR, esqueletos do relatório de qualidade e das contribuições, checklist de documentação no template de PR;
  - decisões registradas em `docs/requisitos.md` (D-4a a D-4f, D-Q3, D-Q6, D-Q7, D-Q8; nenhuma questão aberta) e ADRs 0002 a 0005, todos aceitos;
  - contrato OpenAPI parcial em `docs/api/openapi.yaml` (`GET /produtos`, `GET /operador/relatorio`);
  - registro do checkpoint em `docs/checkpoint-18-11.md`;
  - licença MIT; configuração de proteção de `main` em `.github/branch-protection-main.json`; seção "Como executar" em `docs/configuracao-github.md`.
- No GitHub, em 25 e 26/11:
  - milestones M1–M5 criados e issues vinculadas;
  - `develop` arquivada como tag `archive/develop` e removida;
  - [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) aberta para a proteção de `main` (aguardando execução pelo administrador);
  - #22 fechada com referência ao registro do checkpoint;
  - comentários com critérios de aceite em #3, #4 (atualizado: ADR 0002 aceito), #5, #7, #9, #11–#18 e #21.
- Specs de #2 e #3 em `.kiro/specs/2-aplicacao-base/` e `.kiro/specs/3-ci-qualidade/`, com o ADR 0006 (proposto), no [PR #28](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/28) (rascunho, base: branch do PR #26), aguardando aprovação.

**Não existe ainda**
- Código de aplicação, `pyproject.toml`/dependências, banco e migrações, testes, CI, configuração de Ruff/Radon, OpenAPI gerado ou coleção Postman.
- Proteção de `main` (#27) e labels do plano (o responsável executará).
- Histórico do Git com um único autor humano (romulorjr).

**Situação frente à especificação**
| Item do PDF | Situação |
|---|---|
| RN01–RN12 | Nenhuma implementada; interpretações de RN01, RN05, RN08, RN09, RN10, RN11 e RN12 decididas |
| 14 endpoints mínimos | 0 implementados; 2 descritos no contrato parcial |
| Estados PRONTA / PREPARANDO / AGUARDANDO_LIMPEZA / MANUTENCAO | Não implementados |
| Persistência (estoque, crédito, estado, pedidos) | Não implementada; SQLAlchemy + Alembic e fronteiras de transação decididos (ADR 0002) |
| Validação e erros padronizados | Não implementados; contrato decidido (ADR 0003) |
| Swagger/OpenAPI ou Postman | Contrato parcial planejado em `docs/api/openapi.yaml` |
| Testes e cobertura ≥ 75% | 0 testes; cobertura não medida |
| Análise estática com métricas | Não configurada; especificada na spec de #3 |
| Padrões de projeto e diagrama | Repository e unidade de trabalho decididos no ADR 0002; State a decidir em #10 |
| E01 README | Parcial: sem instruções executáveis; licença definida |
| E02 API + documentação | Ausente |
| E03 relatório de qualidade | Esqueleto em [quality-report.md](quality-report.md) |
| E04 documento de projeto | Ausente |
| E05 histórico de contribuições | Um autor humano |
| E06 declarações | Esqueleto em [contributions.md](contributions.md) |
| E07 vídeo | Ausente |

**Prazos:** em 26/11 faltam 13 dias para 09/12. M1 vence amanhã, 27/11; a implementação de #2 e #3 depende da aprovação das specs.

## Próximos passos
1. Responsável: revisar as specs de #2 e #3 no [PR #28](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/28), responder às cinco questões do PR e autorizar a implementação.
2. Responsável: aplicar a proteção de `main` ([#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27), passo a) e executar `scripts/configure-github.ps1 -Apply`; registrar o resultado em `docs/configuracao-github.md`.
3. Outro integrante: revisar e aprovar o [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26).
4. Grupo: preencher "Apresentado" e "Retorno do docente" em [checkpoint-18-11.md](checkpoint-18-11.md).
5. Agente, depois do item 1: implementar #2 e #3 conforme as specs, validar pela CI e, com a CI verde, preparar o passo (b) da #27. Em seguida #4 e o contrato de erro da #18 (M1).
6. Grupo: distribuir as issues de M2 (#5, #7, #8, #9, #10, #11) entre os integrantes.
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

**Decisões pendentes (aguardando o responsável)**
2. Distribuição das issues entre os cinco integrantes.
3. Conteúdo do registro do checkpoint: o que foi apresentado e o retorno do docente.

## Bloqueios
| Bloqueio | Efeito | Mitigação |
|---|---|---|
| **Hooks do Kiro não estão ativos (não verificados)** | Nenhuma evidência de carregamento: o Kiro lê os hooks ao iniciar a sessão, e os de `.kiro/hooks/` foram criados durante uma sessão aberta; nenhuma saída de hook apareceu nos turnos seguintes. No Kiro Web o workspace é `/projects/sandbox` e o repositório fica na subpasta `Engenharia-de-Sistemas/`: executados a partir da raiz do workspace, `python scripts/kiro/docs_guard.py` e `python scripts/kiro/quality_check.py` não encontram os arquivos e terminam com código 2, sem efeito em gatilhos Stop (testado em 26/11). | **Até corrigir, testes e análise estática devem ser executados à mão** na raiz do repositório (`python scripts/kiro/docs_guard.py`, `python scripts/kiro/quality_check.py`, e os comandos do README) e a CI da #3 é a verificação obrigatória. Verificar em sessão nova: no Kiro IDE, abrir a pasta do repositório como raiz e conferir os hooks no painel do Kiro; no Kiro Web, conferir se uma alteração em `src/` sem CHANGELOG faz o `docs-guard` manter o agente trabalhando. Se não carregarem, ajustar o diretório dos comandos e registrar aqui |
| Proteção de `main` exige administrador | Integração do agente recebe HTTP 403 | Responsável executa o comando da #27 (aguardando) |
| Ambiente do agente (Kiro Web) sem acesso ao PyPI | O agente não consegue instalar FastAPI, SQLAlchemy, pytest-cov nem Radon; só `pytest` e `ruff` estão disponíveis localmente | Validar pela CI do GitHub Actions (#3), cujos logs o agente lê; os integrantes executam localmente. A stack não muda por causa disso (ADR 0002) |
| PowerShell indisponível no ambiente do agente | `scripts/configure-github.ps1` alterado e não executado | Responsável executa localmente (ver `docs/configuracao-github.md`, "Como executar") |
| Prazo de 13 dias sem código | Risco de não cobrir RN01–RN12 com testes | Fluxo vertical primeiro; linha de corte no plano |
| Participação concentrada em uma conta | Risco para E05/E06; com a proteção, cada PR precisa de outro integrante | Distribuir issues e revisões imediatamente |

## Trabalho contínuo
Ler este arquivo, o [plano](plano-de-projeto.md) e o [steering](../.kiro/steering/project.md) antes de mudanças. Conventional Commits e rastreabilidade requisito → issue → implementação → teste → documentação. Alterações funcionais atualizam testes e documentação no mesmo PR. Não modificar referências sincronizadas sob `sources/` no ambiente do projeto (instrução registrada em 14/10).
