# Máquina de Café — ESI

Back-end de uma máquina de café automática para a disciplina Engenharia de Sistemas de Informação. O objetivo é entregar software funcional, testado e documentado, com evidências de participação de todos os integrantes.

**Status em 26/11/2026: planejamento, governança e estrutura inicial. A API ainda não está implementada.** Situação detalhada em [CONTEXT](docs/CONTEXT.md#estado-atual) e mudanças no [CHANGELOG](CHANGELOG.md). A especificação oficial é [ESI - projeto maquina-cafe.pdf](ESI%20-%20projeto%20maquina-cafe.pdf). Sem interface gráfica ou hardware no escopo.

## Equipe
| Integrante (ordem alfabética) | Papel | GitHub |
|---|---|---|
| Bruno de Andrade Gama Kraker | A definir | BrunoKraker |
| Pedro Henryk Bezerra Souza | A definir | pedro-henryk |
| Rodrigo Franco de Moraes | A definir | rodr1gofm |
| Rômulo Maurício Fonseca Júnior | A definir | romulorjr |
| Thales Iamamura | A definir | t-iamamura |

Contas confirmadas em 26/11/2026. Histórico e declarações individuais em [contribuições](docs/contributions.md).

## Escopo
Cinco bebidas com receitas, preços e preparo simulado; estoque e alertas; crédito e troco; pedidos e cancelamento; operador autenticado, limpeza, reposição e relatórios. Estados: PRONTA, PREPARANDO, AGUARDANDO_LIMPEZA e MANUTENCAO. Banco preserva estoque, crédito, estado e pedidos após reiniciar.

## Stack e arquitetura
Stack de referência: Python 3.12, FastAPI, Pydantic, Uvicorn, SQLAlchemy 2.x, Alembic e SQLite. Testes: pytest/pytest-cov e HTTPX. Qualidade: Ruff e Radon. Autenticação do operador: JWT com PyJWT ([ADR 0004](docs/adr/0004-autenticacao-operador-jwt.md)). As versões exatas serão fixadas e verificadas na infraestrutura; a escolha está no [ADR 0001](docs/adr/0001-escolha-da-stack.md). SQLAlchemy + Alembic confirmados em 26/11/2026 no [ADR 0002](docs/adr/0002-persistencia-e-atomicidade.md), com transações `BEGIN IMMEDIATE` abertas e fechadas pelos serviços.

Convenções da API, decididas em 25 e 26/11/2026:
- Dinheiro: reais com duas casas no JSON (`4.50`), centavos inteiros internamente ([ADR 0005](docs/adr/0005-representacao-monetaria.md)).
- Erros: `{"erro": "CODIGO", "mensagem": "..."}` com o mapeamento HTTP da seção [Códigos de erro](#códigos-de-erro) ([ADR 0003](docs/adr/0003-modelo-de-erros.md)).
- Operações que alteram crédito, estoque, pedido e estado são atômicas, com as fronteiras de transação do [ADR 0002](docs/adr/0002-persistencia-e-atomicidade.md).

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
  checkpoint-18-11.md   registro do checkpoint com o docente
  api/openapi.yaml      contrato OpenAPI parcial planejado (até a #21)
  adr/                  README (índice), 0000-modelo, 0001–0005
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
LICENSE                 MIT
```

## Executar localmente
Ainda não há aplicação nem manifesto de dependências; não é possível iniciar a API nesta revisão. A [issue #2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) entregará ambiente reproduzível, instalação e comando validado de inicialização; #4 entregará migrações e inicialização do banco. Não versionar credenciais nem o banco local.

## Testes
Ainda não existem testes executáveis. A #3 configurará a execução; a meta é cobertura mínima de 75% do código da aplicação, com testes unitários, integração e critérios de caixa-preta. Comando **planejado, não disponível nesta revisão**: `python -m pytest --cov=maquina_cafe --cov-report=term-missing --cov-report=xml --cov-fail-under=75`. Ver [matriz](docs/rastreabilidade.md).

## Análise estática
Configurada na #3, consolidada na #20. Comandos **planejados, ainda não disponíveis**: `ruff check .`, `ruff format --check .` e `radon cc src -s -a`. O relatório final de 1–2 páginas reunirá cobertura, resultados da análise e métricas reais.

## Endpoints principais planejados
Rotas sugeridas pelo PDF; nenhuma está implementada. O contrato parcial de `GET /produtos` e `GET /operador/relatorio`, com descrições e exemplos, está em [docs/api/openapi.yaml](docs/api/openapi.yaml). Operações `/operador/*` exigem `Authorization: Bearer <token>`, exceto login, que recebe as credenciais e devolve um JWT válido por 1 hora. Valores monetários em reais com duas casas. OpenAPI será publicado com a aplicação.

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/produtos` | Cardápio, preço, tempo e disponibilidade (estoque para uma unidade e 1 copo; crédito e estado não contam) |
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
| GET | `/operador/relatorio?from=...&to=...` | Vendas e faturamento por período; `from` e `to` obrigatórios, ISO 8601 (`2026-11-01T00:00:00`), inclusivos; sem fuso = UTC−03:00, `Z` e deslocamentos aceitos |

## Regras de negócio
| Regra | Resumo |
|---|---|
| RN01 | Crédito com denominações aceitas, só em PRONTA; saldo máximo de R$ 50, inserção que excede é rejeitada inteira |
| RN02 | Pedido somente PRONTA, com crédito e insumos suficientes |
| RN03 | Debitar preço e insumos na aceitação; conservar saldo restante |
| RN04 | Preparar pelo tempo da receita; concluir e atualizar estado |
| RN05 | Cancelar apenas em preparo; devolver valor, sem repor ingredientes |
| RN06 | Devolver todo crédito restante como troco, a qualquer momento |
| RN07 | Exigir limpeza após 30 preparos concluídos |
| RN08 | Controlar entrada/saída de manutenção e limpeza pendente |
| RN09 | Reabastecer apenas em manutenção, respeitando capacidades |
| RN10 | Alterar preço positivo; informar disponibilidade no cardápio |
| RN11 | Autenticar operador por JWT de 1 hora, com credenciais e segredo em ambiente |
| RN12 | Relatório por período (`from`/`to` inclusivos), total e por bebida; excluir cancelados |

Tabelas de receitas, capacidades, [decisões de interpretação](docs/requisitos.md#decisões-de-interpretação-25112026) e questões em aberto: [requisitos](docs/requisitos.md).

## Códigos de erro
Contrato planejado ([ADR 0003](docs/adr/0003-modelo-de-erros.md)); será implementado na #18 e documentado por rota no OpenAPI. Todo erro tem o corpo `{"erro": "CODIGO", "mensagem": "..."}`. 503 é usado só para chamadas do cliente com a máquina indisponível; o operador no estado errado recebe 409.

| HTTP | `erro` | Quando |
|---|---|---|
| 400 | `DADOS_INVALIDOS` | Açúcar fora de 0–3, valor de crédito não aceito, mais de duas casas decimais, preço ≤ 0, campo ausente, `from`/`to` ausente ou inválido |
| 400 | `LIMITE_CREDITO_EXCEDIDO` | Inserção levaria o crédito acima de R$ 50,00; rejeitada inteira, saldo inalterado |
| 401 | `NAO_AUTORIZADO` | Token do operador ausente, inválido ou expirado |
| 401 | `CREDENCIAIS_INVALIDAS` | Login com usuário ou senha errados |
| 402 | `CREDITO_INSUFICIENTE` | Crédito não cobre o preço |
| 404 | `PRODUTO_NAO_ENCONTRADO` / `PEDIDO_NAO_ENCONTRADO` | Bebida ou pedido inexistente |
| 409 | `MAQUINA_OCUPADA` | Pedido ou crédito com a máquina PREPARANDO |
| 409 | `ESTOQUE_INSUFICIENTE` | Falta ingrediente, açúcar ou copo |
| 409 | `ESTADO_INVALIDO` | Operador: reabastecer ou limpar fora de MANUTENCAO; entrar em manutenção fora de PRONTA/AGUARDANDO_LIMPEZA; sair sem estar em MANUTENCAO |
| 409 | `PEDIDO_NAO_CANCELAVEL` | Cancelar pedido CONCLUIDO ou CANCELADO |
| 422 | `CAPACIDADE_EXCEDIDA` | Reabastecimento acima da capacidade |
| 503 | `MAQUINA_EM_MANUTENCAO` / `LIMPEZA_PENDENTE` | Pedido ou crédito com a máquina em MANUTENCAO ou AGUARDANDO_LIMPEZA |

## Cronograma e entregas
Replanejamento aprovado em 25/11/2026; milestones no GitHub. As Fases 1–6 de outubro ficam como registro histórico no [plano](docs/plano-de-projeto.md).

| Milestone | Vencimento | Issues | Resultado |
|---|---|---|---|
| M1 – Base técnica | 27/11/2026 | #1, #2, #3, #4, #18, #27 | Aplicação inicia; CI com testes, cobertura, Ruff e Radon; banco inicializado; contrato de erro |
| M2 – Fluxo do cliente | 01/12/2026 | #5, #7, #8, #9, #10, #11 | Exemplo do PDF (cappuccino, R$ 10,00, troco R$ 3,50) em teste e no Swagger |
| M3 – Operador e manutenção | 03/12/2026 | #6, #12, #13, #14, #15, #16, #17, #19 | Rotas do operador com JWT, limpeza, reposição, relatório, recuperação após reinício; congelamento de funcionalidades |
| M4 – Qualidade e documentação | 06/12/2026 | #20, #21 | Relatório de qualidade, documento de projeto, OpenAPI e Postman |
| M5 – Entrega | 09/12/2026 | #23, #24 | Declarações, vídeo, ensaio em ambiente limpo e release |

**Checkpoint: realizado em 18/11/2026 ([registro](docs/checkpoint-18-11.md)). Entrega final: 09/12/2026.** O [plano](docs/plano-de-projeto.md) detalha backlog, critérios de aceite, linha de corte, riscos e as sete entregas: repositório, API, relatório de qualidade, documento de projeto, histórico de contribuições, declarações individuais e vídeo. Re-escopo de milestone exige uma issue nova.

## Contribuir
Leia [contexto](docs/CONTEXT.md) e [plano](docs/plano-de-projeto.md). Trabalhe em branch vinculada à issue, com Conventional Commits e PR revisado por outro integrante. Vincule requisito → issue → teste. Testes, cobertura e análise estática serão executados a cada PR de código após configuração da CI (#3).

### Branching
- `main` é a única branch de longa duração. Não há `develop` (arquivada em 25/11/2026 como a tag `archive/develop`).
- Crie a branch a partir de `main` atualizada: `feature/<issue>-<resumo>`, `fix/<issue>-<resumo>`, `docs/<resumo>` ou `test/<issue>-<resumo>`. Exemplo: `git switch main && git pull && git switch -c feature/7-inserir-credito`.
- Abra PR para `main` usando o template. Regras de `main`: sem push direto, PR com 1 aprovação de outro integrante, conversas resolvidas, sem force push; CI verde obrigatória quando o workflow da #3 existir. A proteção no GitHub ainda precisa ser aplicada por um administrador ([#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27)); até lá, vale por acordo.
- Commits no padrão Conventional Commits, com `Refs #n` no rodapé.

[Configuração do GitHub](docs/configuracao-github.md): milestones M1–M5 aplicados em 25/11/2026; proteção de `main` pendente (#27); labels ainda não aplicadas.

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

**Ativação não verificada (26/11/2026).** Não há evidência de que algum desses hooks tenha sido carregado: o Kiro lê os hooks ao iniciar a sessão e eles foram criados durante uma sessão já aberta. No Kiro Web o repositório fica em uma subpasta do workspace; executados a partir da raiz do workspace, os comandos acima não encontram os scripts e terminam com código 2, que não tem efeito em gatilhos Stop. Até a verificação ([CONTEXT, Bloqueios](docs/CONTEXT.md#bloqueios)), execute testes, lint e análise estática à mão e confie na CI (#3).

## Licença
[MIT](LICENSE), © 2026 os cinco integrantes do grupo. A licença cobre o código e a documentação produzidos pelo grupo. O arquivo `ESI - projeto maquina-cafe.pdf` é material da disciplina, de autoria dos docentes, e não é licenciado pelo grupo.
