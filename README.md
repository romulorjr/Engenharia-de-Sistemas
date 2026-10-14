# Máquina de Café — ESI

Back-end de uma máquina de café automática para a disciplina Engenharia de Sistemas de Informação. O objetivo é entregar software funcional, testado e documentado, com evidências de participação de todos os integrantes.

**Status: planejamento e estrutura inicial. A API ainda não está implementada.** A especificação oficial é [ESI - projeto maquina-cafe.pdf](ESI%20-%20projeto%20maquina-cafe.pdf). Sem interface gráfica ou hardware no escopo.

## Equipe
| Integrante (ordem alfabética) | Papel | GitHub |
|---|---|---|
| Bruno de Andrade Gama Kraker | A definir | A informar |
| Pedro Henryk Bezerra Souza | A definir | A informar |
| Rodrigo Franco de Moraes | A definir | A informar |
| Rômulo Maurício Fonseca Júnior | A definir | A informar |
| Thales Iamamura | A definir | A informar |

## Escopo
Cinco bebidas com receitas, preços e preparo simulado; estoque e alertas; crédito e troco; pedidos e cancelamento; operador autenticado, limpeza, reposição e relatórios. Estados: PRONTA, PREPARANDO, AGUARDANDO_LIMPEZA e MANUTENCAO. Banco preserva estoque, crédito, estado e pedidos após reiniciar.

## Stack e arquitetura
Stack de referência: Python 3.12, FastAPI, Pydantic, Uvicorn, SQLAlchemy 2.x, Alembic e SQLite. Testes: pytest/pytest-cov e HTTPX. Qualidade: Ruff e Radon. As versões exatas serão fixadas e verificadas na infraestrutura; a escolha está no [ADR 0001](docs/adr/0001-escolha-da-stack.md).

Controllers recebem entradas e produzem respostas; serviços/domínio coordenam regras; persistência consulta e grava em transações. Ver [arquitetura](docs/arquitetura.md). Repository e State serão avaliados por necessidade real; o documento final justificará o padrão aplicado ou uma alternativa simples.

## Estrutura
```text
src/maquina_cafe/
  api/
  services/
  domain/
  persistence/
tests/
  unit/
  integration/
docs/
  CONTEXT.md
  plano-de-projeto.md
  requisitos.md
  rastreabilidade.md
  arquitetura.md
  configuracao-github.md
  adr/0001-escolha-da-stack.md
.github/
  ISSUE_TEMPLATE/
  PULL_REQUEST_TEMPLATE.md
  repository-setup.json
scripts/
  configure-github.ps1
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

## Contribuir
Leia [contexto](docs/CONTEXT.md) e [plano](docs/plano-de-projeto.md). Trabalhe em branch vinculada à issue, com Conventional Commits e PR revisado por outro integrante. main é a versão revisada; develop integra trabalho; feature/*, docs/*, fix/* e hotfix/* seguem o plano. Vincule requisito → issue → teste. Testes, cobertura e análise estática serão executados a cada PR de código após configuração da CI.

[Configuração do GitHub](docs/configuracao-github.md): labels, milestones e proteção planejados; script separado para aplicação administrativa. Não considerar proteções ativas antes da verificação.

## Licença
Ainda não definida pelo grupo. Nenhum arquivo LICENSE foi adicionado; repositório público não implica concessão de licença de uso.
