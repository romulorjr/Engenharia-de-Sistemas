# Contexto do projeto

Arquivo vivo. Atualizar "Estado atual", "Próximos passos", "Decisões" e "Bloqueios" ao fim de cada sessão de trabalho. Última atualização: 25/11/2026.

Fonte normativa: [ESI - projeto maquina-cafe.pdf](../ESI%20-%20projeto%20maquina-cafe.pdf). Este documento registra estado e decisões; não substitui a especificação. Regras de trabalho do agente e da equipe: [.kiro/steering/project.md](../.kiro/steering/project.md).

## Escopo confirmado
Back-end de uma máquina de café, preferencialmente API REST; sem interface gráfica ou hardware. Cinco bebidas, seis reservatórios, crédito, pedidos, quatro estados, operador e relatórios. RN01–RN12, banco persistente, testes unitários e de integração, cobertura mínima de 75%, análise estática, documentação e sete artefatos finais. O PDF permite selecionar as regras viáveis no prazo e, se HTTP não for viável, uma classe de entrada local.

## Equipe (ordem alfabética)
Bruno de Andrade Gama Kraker, Pedro Henryk Bezerra Souza, Rodrigo Franco de Moraes, Rômulo Maurício Fonseca Júnior, Thales Iamamura. Contas GitHub prováveis e papéis em [contribuições](contributions.md), ainda a confirmar.

## Estado atual (25/11/2026)
Relatório de estado produzido nesta data e atualizado depois das decisões do responsável.

**Feito**
- Documentação de planejamento de 14/10 (PR #25): README, requisitos, plano, rastreabilidade, arquitetura planejada, ADR 0001, configuração GitHub, templates, `.gitignore` e pastas vazias em `src/` e `tests/`.
- [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26) (aberto, aguardando revisão), issue #1:
  - steering e hooks do Kiro, CHANGELOG, índice e modelo de ADR, esqueletos do relatório de qualidade e das contribuições, checklist de documentação no template de PR;
  - decisões de 25/11 registradas: `docs/requisitos.md` (D-4a a D-4f) e ADRs 0002 (proposto), 0003, 0004 e 0005;
  - licença MIT (`LICENSE`);
  - configuração de proteção de `main` versionada em `.github/branch-protection-main.json`.
- No GitHub, em 25/11:
  - milestones M1–M5 criados (números 1–5) e issues vinculadas; #22 sem milestone;
  - `develop` arquivada como tag `archive/develop` e removida;
  - [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) aberta para a proteção de `main`, que o agente não conseguiu aplicar (HTTP 403);
  - comentários com os novos critérios de aceite em #3, #4, #7, #9, #11–#18 e #21.

**Não existe ainda**
- Código de aplicação, `pyproject.toml`/dependências, banco e migrações, testes, CI, configuração de Ruff/Radon, OpenAPI exportado ou coleção Postman.
- Proteção de `main` (#27) e labels do plano.
- Histórico do Git com um único autor humano (romulorjr).

**Situação frente à especificação**
| Item do PDF | Situação |
|---|---|
| RN01–RN12 | Nenhuma implementada; interpretações de RN01, RN05, RN08, RN09, RN11 e RN12 decididas |
| 14 endpoints mínimos | 0 implementados |
| Estados PRONTA / PREPARANDO / AGUARDANDO_LIMPEZA / MANUTENCAO | Não implementados |
| Persistência (estoque, crédito, estado, pedidos) | Não implementada; forma de acesso pendente (ADR 0002) |
| Validação e erros padronizados | Não implementados; contrato decidido (ADR 0003) |
| Swagger/OpenAPI ou Postman | Inexistente |
| Testes e cobertura ≥ 75% | 0 testes; cobertura não medida |
| Análise estática com métricas | Não configurada |
| Padrões de projeto e diagrama | Repository e unidade de trabalho propostos no ADR 0002; State a decidir em #10 |
| E01 README | Parcial: sem instruções executáveis; licença definida |
| E02 API + documentação | Ausente |
| E03 relatório de qualidade | Esqueleto em [quality-report.md](quality-report.md) |
| E04 documento de projeto | Ausente |
| E05 histórico de contribuições | Um autor humano |
| E06 declarações | Esqueleto em [contributions.md](contributions.md) |
| E07 vídeo | Ausente |

**Prazos:** faltam 14 dias para 09/12. M1 vence em 27/11 e depende da escolha de persistência para a #4.

## Próximos passos
1. Responsável: escolher a opção A ou B do [ADR 0002](adr/0002-persistencia-e-atomicidade.md). Bloqueia #4 e M1.
2. Responsável: aplicar a proteção de `main` pela [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) (comando pronto).
3. Outro integrante: revisar e aprovar o [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26).
4. Responsável: confirmar contas GitHub (decisão 5) e a situação do checkpoint (#22, decisão 6).
5. Agente, depois do item 1: spec e implementação de #2 → #3 → #4, com o contrato de erro da #18 (M1). Em seguida M2: #5, #7, #8, #9, #10, #11.
6. Antes das issues correspondentes: responder Q3 (#5), Q7 (#7), Q8 (#11) e Q6 (#17) de [requisitos](requisitos.md#questões-a-resolver-antes-das-respectivas-implementações).

## Decisões
| Data | Decisão | Registro |
|---|---|---|
| 14/10/2026 | Stack Python 3.12, FastAPI, SQLAlchemy 2.x, Alembic, SQLite, pytest, Ruff, Radon | [ADR 0001](adr/0001-escolha-da-stack.md) |
| 14/10/2026 | Checkpoint 18/11/2026 e entrega 09/12/2026; fuso America/Sao_Paulo | Este arquivo |
| 25/11/2026 | Documentação obrigatória em todo PR: README, CONTEXT, plano, CHANGELOG, ADR, OpenAPI/Postman, testes, diagrama, relatório de qualidade e contribuições | [steering](../.kiro/steering/project.md) |
| 25/11/2026 | Hooks do Kiro versionados em `.kiro/hooks/`, com scripts Python multiplataforma em `scripts/kiro/` | [CHANGELOG](../CHANGELOG.md) |
| 25/11/2026 | Commits gerados pelo agente aparecem com autor `Kiro Agent` e são registrados com quem os solicitou | [contribuições](contributions.md) |
| 25/11/2026 | Decisão 1: replanejamento M1–M5 aprovado; re-escopo de milestone exige issue nova | [plano](plano-de-projeto.md#replanejamento-aprovado-em-25112026) |
| 25/11/2026 | Decisão 2: `develop` abandonada (tag `archive/develop`); branches `feature/`, `fix/`, `docs/`, `test/` a partir de `main`; PR revisado para `main`; `main` protegida com CI obrigatória | [plano](plano-de-projeto.md#branches-commits-e-prs), README "Branching", #27 |
| 25/11/2026 | D-4a: crédito só em PRONTA (409 em PREPARANDO, 503 em MANUTENCAO/AGUARDANDO_LIMPEZA) | [requisitos](requisitos.md#decisões-de-interpretação-25112026), [ADR 0003](adr/0003-modelo-de-erros.md) |
| 25/11/2026 | D-4b: saldo nunca passa de R$ 50; inserção excedente rejeitada inteira | requisitos, ADR 0003 |
| 25/11/2026 | D-4c: relatório com `from`/`to` ISO 8601, obrigatórios e inclusivos; 400 se ausente ou inválido | requisitos |
| 25/11/2026 | D-4d: JWT HS256 de 1 hora; credenciais e segredo por ambiente; 401 sem token válido | [ADR 0004](adr/0004-autenticacao-operador-jwt.md) |
| 25/11/2026 | D-4e: reais com duas casas no JSON; centavos internamente | [ADR 0005](adr/0005-representacao-monetaria.md) |
| 25/11/2026 | D-4f: 409 `ESTADO_INVALIDO` para operador no estado errado; 503 só para o cliente | ADR 0003 |
| 25/11/2026 | Decisão 7: licença MIT | [LICENSE](../LICENSE) |
| 25/11/2026 | Escolha do agente dentro da D-4a: crédito usa os mesmos códigos de `POST /pedidos` por estado (reversível) | requisitos, ADR 0003 |

**Decisões pendentes (aguardando o responsável)**
1. Persistência: opção A (manter ADR 0001) ou B (`sqlite3`) do ADR 0002. A mensagem de 25/11 trouxe as duas opções sem escolha.
2. Contas GitHub: a mensagem de 25/11 trouxe o item 5 sem confirmar o mapeamento. `docs/contributions.md` continua "a confirmar".
3. Checkpoint de 18/11 (#22): a mensagem de 25/11 trouxe o item 6 sem informar se aconteceu. #22 continua aberta, sem milestone.
4. Códigos propostos Q7 (`LIMITE_CREDITO_EXCEDIDO`, 400) e Q8 (`PEDIDO_NAO_CANCELAVEL`, 409); detalhes do relatório Q6; disponibilidade Q3.
5. Distribuição das issues entre os cinco integrantes.

## Bloqueios
| Bloqueio | Efeito | Mitigação |
|---|---|---|
| Persistência indefinida (ADR 0002) | #4 não pode começar; M1 (27/11) em risco | Escolha do responsável até 26/11 |
| Proteção de `main` exige administrador | Integração do agente recebe HTTP 403 | Comando pronto na #27 para o responsável |
| Ambiente do agente (Kiro Web) sem acesso ao PyPI | O agente não consegue instalar FastAPI, SQLAlchemy, pytest-cov nem Radon; só `pytest` e `ruff` estão disponíveis localmente | Validar pela CI do GitHub Actions (#3), cujos logs o agente lê; os integrantes executam localmente. A stack não muda por causa disso |
| Prazo de 14 dias sem código | Risco de não cobrir RN01–RN12 com testes | Fluxo vertical primeiro; linha de corte no plano |
| Participação concentrada em uma conta | Risco para E05/E06; com a proteção, cada PR precisa de outro integrante | Distribuir issues e revisões imediatamente |

## Trabalho contínuo
Ler este arquivo, o [plano](plano-de-projeto.md) e o [steering](../.kiro/steering/project.md) antes de mudanças. Conventional Commits e rastreabilidade requisito → issue → implementação → teste → documentação. Alterações funcionais atualizam testes e documentação no mesmo PR. Não modificar referências sincronizadas sob `sources/` no ambiente do projeto (instrução registrada em 14/10).
