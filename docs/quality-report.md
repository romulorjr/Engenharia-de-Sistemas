# Relatório de qualidade

Entrega E03 (1–2 páginas na versão final). Issue [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20). Atualizar a cada milestone com números medidos pela CI ou por comando reproduzível. Nunca registrar valor estimado como medido.

**Situação em 25/11/2026: não há código de aplicação nem testes. Nenhuma métrica foi medida.**

## Como medir
Comandos planejados pela [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3); só valem depois que o `pyproject.toml` e a CI existirem.

| Métrica | Comando | Meta |
|---|---|---|
| Cobertura de linhas e ramos | `python -m pytest --cov=maquina_cafe --cov-branch --cov-report=term-missing --cov-fail-under=75` | ≥ 75% global, sem excluir módulos |
| Lint | `ruff check .` | 0 erros |
| Formatação | `ruff format --check .` | 0 arquivos a formatar |
| Complexidade ciclomática | `radon cc src -s -a` | média A/B; nenhuma função acima de C |
| Índice de manutenibilidade | `radon mi src -s` | todos os módulos A |

## Histórico por milestone
| Data | Milestone / PR | Testes (unit / integração) | Cobertura | Ruff | Radon CC médio | Observações |
|---|---|---|---|---|---|---|
| 25/11/2026 | Estado inicial | 0 / 0 | não medida | não configurado | não medido | Apenas documentação |

## Code smells e dívida técnica
| Data | Local | Problema | Ação | Issue |
|---|---|---|---|---|
| — | — | Nenhum código para analisar | — | — |

## Critérios de teste funcional (caixa-preta)
Partições de equivalência, valores-limite e transições de estado por regra, rastreados em [rastreabilidade](rastreabilidade.md). Exemplos previstos no [plano](plano-de-projeto.md#testes-e-rastreabilidade).

## Conclusão
Preencher na entrega final: cobertura obtida, resultado da análise estática, principais smells corrigidos e limitações conhecidas.
