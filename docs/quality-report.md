# Relatório de qualidade

Entrega E03 (1–2 páginas na versão final). Issue [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20). Atualizar a cada milestone com números medidos pela CI ou por comando reproduzível. Nunca registrar valor estimado como medido.

**Situação em 27/11/2026:** primeira medição real, na CI do [PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29) (#2, #3). O código medido é só a aplicação base: configuração e fábrica da aplicação, sem regras de negócio. A cobertura de 100% reflete esse código pequeno, não a qualidade das regras RN01–RN12, que ainda não existem.

## Como medir
Mesmos comandos da CI ([workflow](../.github/workflows/ci.yml), job `testes-e-analise`, Python 3.12). Limites no [ADR 0006](adr/0006-estrategia-de-testes.md).

| Métrica | Comando | Meta / limite |
|---|---|---|
| Cobertura de linhas e ramos | `python -m pytest --cov=maquina_cafe --cov-branch --cov-report=term-missing --cov-fail-under=75` | ≥ 75% global, sem excluir módulos (falha abaixo) |
| Lint | `ruff check .` | 0 erros (falha) |
| Formatação | `ruff format --check .` | 0 arquivos a formatar (falha) |
| Complexidade ciclomática | `python scripts/ci/radon_gate.py src` (`radon cc src -s -a`) | aviso em classe C (11–20); falha em classe D ou pior (≥ 21) |
| Índice de manutenibilidade | idem (`radon mi src -s`) | falha abaixo da classe A |
| Camadas | `tests/unit/test_architecture.py` | 0 imports proibidos (falha) |
| Inicialização | `python scripts/ci/smoke.py` | 200 em `/openapi.json` em até 15 s (falha) |

## Histórico por milestone
| Data | Milestone / PR | Testes (unit / integração) | Cobertura | Ruff | Radon | Observações |
|---|---|---|---|---|---|---|
| 25/11/2026 | Estado inicial | 0 / 0 | não medida | não configurado | não medido | Apenas documentação |
| 27/11/2026 | M1 / PR #29, run [46014939322](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46014939322) | 41 / 5 (46 passaram, 0 falharam, 0 ignorados) | 100% total; linhas 33/33; ramos 4/4 | lint 0 erros; formatação: 48 arquivos já formatados | CC média A (2,2) em 5 blocos; maior: `_read` A (3); 0 avisos C; 0 falhas. MI: todos os 7 módulos A (menor: `config.py` 88,24) | 1 aviso de depreciação do Starlette (ver abaixo). Duração do pytest: 1,43 s |

Prova de que a CI falha: run [46015179174](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46015179174), com um teste propositalmente quebrado (commit 06e588f, revertido em 044fba8). A etapa de testes falhou (1 falha, 46 passaram) e as demais etapas rodaram mesmo assim; o job terminou vermelho. O run seguinte, [46015286528](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46015286528), voltou a verde.

Versões resolvidas na CI em 27/11 (artefato `pip-freeze.txt`): Python 3.12.16, fastapi 0.165.0, starlette 1.10.0, pydantic 2.14.4, pydantic_core 2.50.5, uvicorn 0.54.0, pytest 9.2.0, pytest-cov 7.1.0, coverage 7.17.5, httpx 0.29.0, ruff 0.17.6, radon 6.0.1.

## Code smells e dívida técnica
| Data | Local | Problema | Ação | Issue |
|---|---|---|---|---|
| 27/11/2026 | testes de integração (`fastapi.testclient`) | `StarletteDeprecationWarning`: o Starlette 1.10 pede `httpx2` em vez de `httpx` no `TestClient`. Não falha hoje; uma versão futura do Starlette pode quebrar os testes de integração | Avaliar a troca para `httpx2` | [#30](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/30) |

## Critérios de teste funcional (caixa-preta)
Partições de equivalência, valores-limite e transições de estado por regra, rastreados em [rastreabilidade](rastreabilidade.md). Exemplos previstos no [plano](plano-de-projeto.md#testes-e-rastreabilidade). Na #2: partições de configuração (variável ausente, válida, vazia, só espaços).

## Conclusão
Preencher na entrega final: cobertura obtida, resultado da análise estática, principais smells corrigidos e limitações conhecidas.
