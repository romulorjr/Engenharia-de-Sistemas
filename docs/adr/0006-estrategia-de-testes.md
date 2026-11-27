# ADR 0006 — Estratégia de testes e medição de cobertura

Data: 26/11/2026 (proposto). Status: **Aceito** em 27/11/2026 pelo responsável, com a aprovação das specs de #2 e #3.
Requisitos: ENG-QUAL, E03. Issues: #3, #20; vale para todas as issues de código.

## Contexto
O PDF exige testes unitários e de integração, cobertura mínima de 75% de código e critérios de teste funcional ou caixa-preta. As regras dependem de tempo (preparo de 5 a 12 s), de transações (ADR 0002) e de concorrência (dois pedidos simultâneos). O ambiente do agente não instala dependências do PyPI; a CI (#3) é a execução de referência.

## Decisão
**Níveis**
| Nível | Pasta | O que cobre | Infraestrutura |
|---|---|---|---|
| Unitário | `tests/unit/` | domínio (receitas, dinheiro, transições de estado), serviços com regras puras, configuração, scripts de CI, teste de camadas | sem banco e sem HTTP; relógio falso |
| Integração | `tests/integration/` | rotas via `TestClient` do FastAPI; persistência, transações e recuperação após reinício | SQLite em arquivo temporário (`tmp_path`) com migrações aplicadas; conexões independentes para concorrência |

**Critérios de caixa-preta.** Cada regra RNxx e cada decisão D-xx tem casos derivados por:
- partição de equivalência (ex.: denominação aceita/não aceita);
- valores-limite (ex.: crédito 49,50 + 0,50 aceito e 50,00 + 0,50 rejeitado; açúcar −1/0/3/4; alerta exatamente no limiar; 29ª e 30ª conclusão);
- transições de estado (todas as transições válidas e as inválidas mais prováveis).

Cada linha da tabela de erros do [ADR 0003](0003-modelo-de-erros.md) tem ao menos um teste de integração (`test_error_contract`, #18). A docstring do teste cita a regra (`"""RN01, D-Q7: ..."""`) e o nome entra na [matriz de rastreabilidade](../rastreabilidade.md).

**Tempo.** O tempo vem de uma interface de relógio injetável; os testes usam um relógio falso que avança sob controle. Proibido `time.sleep` nos testes.

**Banco nos testes.** Banco real em arquivo temporário, um por teste. Não usar `:memory:` (não permite conexões independentes) nem simular repositories nos testes de transação, que precisam provar o rollback real (ADR 0002).

**Cobertura.**
- Linhas e ramos do pacote `maquina_cafe`, medidos na CI com `--cov-fail-under=75`.
- Nenhum módulo da aplicação omitido; só `if TYPE_CHECKING:` é excluído.
- O número que vale para o relatório (E03) é o da CI, com link para o run.

**Teste de camadas.** `tests/unit/test_architecture.py` falha quando uma camada importa o que o steering proíbe (ex.: `fastapi` fora de `api`, `sqlalchemy` fora de `persistence`). É a prova mais barata de que a separação de responsabilidades exigida pelo PDF é respeitada. Falha nesse teste é regressão real: corrige-se o código, não a lista de proibições. Mudar a lista exige decisão registrada.

**Análise estática.** Ruff (`ruff check`, `ruff format --check`) e Radon na CI, com estes limites:
| Métrica | Aviso (não falha) | Falha |
|---|---|---|
| Complexidade ciclomática por bloco (função, método, classe) | classe C (CC 11–20) | classe D ou pior (CC ≥ 21) |
| Índice de manutenibilidade por módulo | — | abaixo da classe A (MI < 20) |

O aviso de classe C mostra a tendência antes de o código chegar a D. Se a CI falhar só por esses limites, a resposta é listar e corrigir as funções ou módulos apontados; os limites não são reduzidos para fazer a CI passar.

**Teste de fumaça.** A CI inicia `uvicorn` com `create_app` e exige 200 em `/openapi.json`.

**Execução.** A CI roda a suíte a cada PR e push em `main`, em Python 3.12 fixo; o check `testes-e-analise` será obrigatório na proteção de `main` (#27). Localmente, os comandos do README.

**Dependências.** Versões das dependências diretas fixadas com `==` no `pyproject.toml`; as indiretas são resolvidas pelo pip, e o `pip freeze` de cada execução da CI fica como artefato. Reprodutibilidade completa com arquivo de lock ou hashes está fora do escopo; reavaliar só se aparecer divergência de ambiente entre a CI e as máquinas do grupo.

## Consequências
- Testes de integração um pouco mais lentos (arquivo SQLite por teste), em troca de provar transações e recuperação de verdade.
- O domínio precisa receber o relógio por parâmetro ou injeção, nunca chamar `datetime.now()` diretamente.
- Revisores conferem se o PR traz casos de limite e de erro, não só o caminho feliz.

## Alternativas consideradas
| Alternativa | Motivo da rejeição |
|---|---|
| Só testes ponta a ponta com servidor real | Lentos e difíceis de controlar no tempo; não isolam regras |
| Repositories simulados em todos os testes | Não provam atomicidade nem recuperação após reinício |
| SQLite `:memory:` | Não permite conexões independentes para os testes de concorrência |
| Meta de cobertura acima de 75% imposta na CI | O PDF pede 75%; uma meta maior pode ser buscada sem bloquear merges |
| Testes de mutação | Úteis, mas fora do prazo de 09/12 |

## Referências
- [pytest](https://docs.pytest.org/), [pytest-cov](https://pytest-cov.readthedocs.io/), [coverage.py: medição de ramos](https://coverage.readthedocs.io/en/latest/branch.html)
- [FastAPI: testes](https://fastapi.tiangolo.com/tutorial/testing/)
