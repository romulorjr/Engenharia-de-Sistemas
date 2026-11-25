# Máquina de Café — ESI

Back-end de uma máquina de café automática para a disciplina Engenharia de Sistemas de Informação. O objetivo é entregar software funcional, testado e documentado, com evidências de participação de todos os integrantes.

**Status em 25/11/2026: planejamento, governança e estrutura inicial. A API ainda não está implementada.** Situação detalhada em [CONTEXT](docs/CONTEXT.md#estado-atual-25112026) e mudanças no [CHANGELOG](CHANGELOG.md). A especificação oficial é [ESI - projeto maquina-cafe.pdf](ESI%20-%20projeto%20maquina-cafe.pdf). Sem interface gráfica ou hardware no escopo.

## Equipe
| Integrante (ordem alfabética) | Papel | GitHub (a confirmar) |
|---|---|---|
| Bruno de Andrade Gama Kraker | A definir | BrunoKraker |
| Pedro Henryk Bezerra Souza | A definir | pedro-henryk |
| Rodrigo Franco de Moraes | A definir | rodr1gofm |
| Rômulo Maurício Fonseca Júnior | A definir | romulorjr |
| Thales Iamamura | A definir | t-iamamura |

As contas são as colaboradoras do repositório; a correspondência com os nomes foi inferida e cada integrante deve confirmá-la em [contribuições](docs/contributions.md).

## Escopo
Cinco bebidas com receitas, preços e preparo simulado; estoque e alertas; crédito e troco; pedidos e cancelamento; operador autenticado, limpeza, reposição e relatórios. Estados: PRONTA, PREPARANDO, AGUARDANDO_LIMPEZA e MANUTENCAO. Banco preserva estoque, crédito, estado e pedidos após reiniciar.

## Stack e arquitetura
Stack de referência: Python 3.12, FastAPI, Pydantic, Uvicorn, SQLAlchemy 2.x, Alembic e SQLite. Testes: pytest/pytest-cov e HTTPX. Qualidade: Ruff e Radon. As versões exatas serão fixadas e verificadas na infraestrutura; a escolha está no [ADR 0001](docs/adr/0001-escolha-da-stack.md).

Controllers recebem entradas e produzem respostas; serviços/domínio coordenam regras; persistência consulta e grava em transações. Ver [arquitetura](docs/arquitetura.md). Repository e State serão avaliados por necessidade real; o documento final justificará o padrão aplicado ou uma alternativa simples.

## Estrutura
```text
src/maquina_cafe/
  api/                  controllers HTTP (vazio)
  services/             regras de negócio e transações (vazio)
  domain/               entidades, receitas, estados (vazio)
  persistence/          repositories e banco (vazio)
tests/
  unit/
  integration/
docs/
  CONTEXT.md            estado atual, próximos passos, decisões, bloqueios
  plano-de-projeto.md   milestones, backlog, Definition of Done
  requisitos.md         transcrição do PDF e questões em aberto
  rastreabilidade.md    requisito → issue → implementação → teste → documentação
  arquitetura.md        diagrama de componentes (planejado)
  quality-report.md     cobertura, análise estática, code smells
  contributions.md      histórico de contribuições e declarações
  configuracao-github.md
  adr/                  README (índice), 0000-modelo, 0001-escolha-da-stack
.kiro/
  steering/project.md   regras do projeto para o Kiro e para a equipe
  hooks/                docs-guard, quality-on-save, quality-on-stop
.github/
  ISSUE_TEMPLATE/
  PULL_REQUEST_TEMPLATE.md
  repository-setup.json
scripts/
  configure-github.ps1
  kiro/                 docs_guard.py, quality_check.py
CHANGELOG.md
```

## Executar localmente
Ainda não há aplicação nem manifesto de dependências; não é possível iniciar a API nesta revisão. A [issue #2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) entregará ambiente reproduzível, instalação e comando validado de inicialização; #4 entregará migrações e inicialização do banco. Não versionar credenciais nem o banco local.

## Testes
Ainda não existem testes executáveis. A #3 configurará a execução; a meta é cobertura mínima de 75% do código da aplicação, com testes unitários, integração e critérios de caixa-preta. Comando **planejado, não disponível nesta revisão**: `python -m pytest --cov=maquina_cafe --cov-report=term-missing --cov-report=xml --cov-fail-under=75`. Ver [matriz](docs/rastreabilidade.md).

## Análise estática
Configurada na #3, consolidada na #20. Comandos **planejados, ainda não disponíveis**: `ruff check .`, `ruff format --check .` e `radon cc src -s -a`. O relatório final de 1–2 páginas reunirá cobertura, resultados da análise e métricas reais.

## Endpoints principais planejados
Rotas sugeridas pelo PDF; nenhuma está implementada. Operações /operador/* exigem token, exceto login, que recebe as credenciais. OpenAPI será publicado com a aplicação.

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/produtos` | Cardápio, preço, tempo e disponibilidade |
| GET | `/status` | Estado e crédito |
| POST | `/credito` | Inserir crédito |
| POST | `/troco` | Devolver saldo |
| POST | `/pedidos` | Criar pedido |
| GET | `/pedidos/{id}` | Consultar preparo |
| POST | `/pedidos/{id}/cancelar` | Cancelar em preparo |
| POST | `/operador/login` | Obter token |
| GET | `/operador/estoque` | Estoque e alertas |
| POST | `/operador/estoque/reabastecer` | Repor insumo em manutenção |
| PUT | `/operador/produtos/{id}/preco` | Alterar preço |
| POST | `/operador/manutencao` | Entrar/sair da manutenção |
| POST | `/operador/limpeza` | Registrar limpeza |
| GET | `/operador/relatorio` | Vendas e faturamento por período |

## Regras de negócio
| Regra | Resumo |
|---|---|
| RN01 | Crédito com denominações aceitas; saldo máximo de R$ 50 |
| RN02 | Pedido somente PRONTA, com crédito e insumos suficientes |
| RN03 | Debitar preço e insumos na aceitação; conservar saldo restante |
| RN04 | Preparar pelo tempo da receita; concluir e atualizar estado |
| RN05 | Cancelar apenas em preparo; devolver valor, sem repor ingredientes |
| RN06 | Devolver todo crédito restante como troco, a qualquer momento |
| RN07 | Exigir limpeza após 30 preparos concluídos |
| RN08 | Controlar entrada/saída de manutenção e limpeza pendente |
| RN09 | Reabastecer apenas em manutenção, respeitando capacidades |
| RN10 | Alterar preço positivo; informar disponibilidade no cardápio |
| RN11 | Autenticar operador por token, com credenciais em ambiente |
| RN12 | Relatório por período, total e por bebida; excluir cancelados |

Tabelas de receitas, capacidades, erros e questões em aberto: [requisitos](docs/requisitos.md).

## Cronograma e entregas
- **Fase 1 – Infra:** 19–25/10/2026 — Documentação, ambiente, CI e persistência inicial.
- **Fase 2 – Cardápio/Estoque/Crédito:** 26/10–01/11/2026 — Cardápio, estoque, crédito, troco e autenticação básica.
- **Fase 3 – Pedidos/Transações:** 02–18/11/2026 — Pedidos atômicos, preparo, cancelamento e checkpoint em 18/11.
- **Fase 4 – Operador/Manutenção:** 19–29/11/2026 — Limpeza, reposição, manutenção, preços e relatórios.
- **Fase 5 – Testes/Qualidade:** 30/11–02/12/2026 — Consolidação; testes são desenvolvidos desde a infraestrutura.
- **Fase 6 – Documentação/Vídeo:** 03/11–08/12/2026 — Documentação contínua, relatórios, declarações e vídeo.
- **Entrega Final:** 09/12/2026 — Entrega dos sete artefatos revisados.

**Checkpoint: 18/11/2026. Entrega final: 09/12/2026.** O [plano](docs/plano-de-projeto.md) detalha backlog, critérios de aceite, riscos e as sete entregas: repositório, API, relatório de qualidade, documento de projeto, histórico de contribuições, declarações individuais e vídeo.

Em 25/11/2026 as Fases 1–3 estão vencidas sem código. Um [replanejamento](docs/plano-de-projeto.md#replanejamento-proposto-em-25112026) com milestones M1–M5 até 09/12 aguarda confirmação do grupo.

## Contribuir
Leia [contexto](docs/CONTEXT.md) e [plano](docs/plano-de-projeto.md). Trabalhe em branch vinculada à issue, com Conventional Commits e PR revisado por outro integrante. main é a versão revisada; develop integra trabalho; feature/*, docs/*, fix/* e hotfix/* seguem o plano. Vincule requisito → issue → teste. Testes, cobertura e análise estática serão executados a cada PR de código após configuração da CI.

[Configuração do GitHub](docs/configuracao-github.md): labels, milestones e proteção planejados; script separado para aplicação administrativa. Não considerar proteções ativas antes da verificação.

### Documentação obrigatória em cada PR
Regras completas em [.kiro/steering/project.md](.kiro/steering/project.md). Todo PR atualiza, quando afetados: este README, [CONTEXT](docs/CONTEXT.md), [plano](docs/plano-de-projeto.md) e [matriz](docs/rastreabilidade.md), [CHANGELOG](CHANGELOG.md), [ADRs](docs/adr/README.md), OpenAPI/Postman, testes, [diagrama](docs/arquitetura.md), [relatório de qualidade](docs/quality-report.md) e [contribuições](docs/contributions.md). Funcionalidades e refatorações têm spec em `.kiro/specs/<issue>-<resumo>/` (requirements, design, tasks).

### Hooks do Kiro
Versionados em `.kiro/hooks/` e ativados ao abrir a pasta do repositório como raiz do workspace no Kiro. Os comandos rodam na raiz do repositório e também podem ser executados à mão:

| Hook | Gatilho | Comando | Efeito |
|---|---|---|---|
| docs-guard | fim do turno do agente (Stop) | `python scripts/kiro/docs_guard.py` | Falha se `src/` ou `tests/` mudaram na branch sem `CHANGELOG.md` e `docs/CONTEXT.md` |
| quality-on-save | arquivo `.py` salvo em `src/` ou `tests/` (Kiro IDE/CLI) | `python scripts/kiro/quality_check.py --lint-only` | Ruff check e format check |
| quality-on-stop | fim do turno do agente (Stop) | `python scripts/kiro/quality_check.py --if-changed` | Ruff e pytest se houver código alterado |

Enquanto não houver `pyproject.toml` (#2), `quality_check.py` não executa nada. Gatilhos de arquivo não rodam no Kiro Web; os gatilhos Stop rodam no IDE, CLI e Web.

## Licença
Ainda não definida pelo grupo. Nenhum arquivo LICENSE foi adicionado; repositório público não implica concessão de licença de uso.
