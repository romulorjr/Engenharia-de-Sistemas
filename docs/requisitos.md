# Requisitos e contrato de referência

Fonte: [PDF](../ESI%20-%20projeto%20maquina-cafe.pdf), páginas 1–7. RNxx são identificadores originais; CAT01, EST01, ENG-*, E01–E07 e CHECKPOINT são identificadores de rastreabilidade deste planejamento. Rotas e códigos HTTP são sugestões do PDF e serão consolidados no OpenAPI.

## CAT01 — Cardápio
| Bebida | Água ml | Café g | Leite ml | Chocolate g | Preparo s | Preço R$ |
|---|---:|---:|---:|---:|---:|---:|
| Café expresso | 40 | 8 | 0 | 0 | 5 | 4,00 |
| Café longo | 120 | 8 | 0 | 0 | 8 | 4,50 |
| Café com leite | 40 | 8 | 150 | 0 | 10 | 6,00 |
| Cappuccino | 40 | 8 | 100 | 5 | 12 | 6,50 |
| Chocolate quente | 50 | 0 | 120 | 30 | 12 | 7,00 |

Toda bebida consome um copo; açúcar opcional de 0 a 3 porções de 5 g, sem custo adicional.

## EST01 — Estoque
| Item | Capacidade | Alerta estritamente abaixo de |
|---|---:|---:|
| Água | 2000 ml | 400 ml |
| Café | 500 g | 100 g |
| Leite | 1000 ml | 200 ml |
| Chocolate | 400 g | 80 g |
| Açúcar | 300 g | 60 g |
| Copos | 50 un. | 10 un. |

Reservatórios cheios apenas na primeira inicialização.

## Regras de negócio
| Regra | Resumo fiel ao PDF |
|---|---|
| RN01 | Inserções de R$ 0,50; 1; 2; 5; 10; 20. Crédito acumulado até R$ 50. |
| RN02 | Pedido exige PRONTA, crédito suficiente e todos os insumos, açúcar escolhido e copo. |
| RN03 | Aceitação debita preço e insumos; crédito restante permanece disponível. |
| RN04 | Pedido EM_PREPARO e máquina PREPARANDO; conclusão ao fim da duração. Retorna a PRONTA, observada RN07. |
| RN05 | Cancelamento apenas EM_PREPARO; restitui preço ao crédito, sem devolver insumos; máquina PRONTA. |
| RN06 | Troco devolve todo o saldo e o zera a qualquer momento. |
| RN07 | A cada 30 preparos concluídos desde a limpeza, AGUARDANDO_LIMPEZA; operador entra em manutenção, limpa e sai. |
| RN08 | Entra em manutenção a partir de PRONTA ou AGUARDANDO_LIMPEZA; sai para PRONTA ou mantém limpeza pendente. |
| RN09 | Reabastecimento apenas em MANUTENCAO e sem exceder capacidades. |
| RN10 | Operador altera preço para valor positivo; cardápio informa disponibilidade por estoque. |
| RN11 | Operações do operador autenticadas por token; credenciais fixas em ambiente são suficientes. |
| RN12 | Quantidade vendida e faturamento total e por bebida, por período; cancelados excluídos. |

Estados: PRONTA, PREPARANDO, AGUARDANDO_LIMPEZA, MANUTENCAO. Apenas pedidos concluídos incrementam contador de limpeza.

## Engenharia
- ENG-INFRA: aplicação reproduzível e versionada.
- ENG-PERSIST: estoque, crédito, estado e pedidos persistem entre reinicializações.
- ENG-API: validação e erros consistentes; exemplos: 404 inexistente, 400 dados inválidos, 402 crédito insuficiente, 409 estoque insuficiente/ocupada, 503 manutenção/limpeza, 401 token inválido, 422 excesso de reposição.
- ENG-QUAL: testes unitários e de integração; cobertura mínima de 75%; critérios de caixa-preta; análise estática e métricas.
- ENG-DOC: API documentada; separação de responsabilidades; decisão sobre padrão e diagrama de até uma página.

## Questões a resolver antes das respectivas implementações
Não são requisitos adicionais confirmados:
1. RN01 não explicita inserção de crédito fora de PRONTA, enquanto a descrição de PRONTA associa esse estado à aceitação de crédito. Definir antes de #7/#11, inclusive interação entre restituição e limite de R$ 50.
2. RN12 não especifica limites inclusivos/exclusivos do período, fuso, data de referência ou vendas em preparo. Definir antes de #17; proposta: contar concluídos pelo instante de conclusão e preço cobrado.
3. Disponibilidade no cardápio não recebe açúcar escolhido; proposta: receita base e copo, com validação completa do açúcar no pedido (#5/#9).
4. Definir expiração do token (#12), precisão monetária e representação JSON (#16/#18), sem tratar propostas como exigências do PDF.

## Entregas
E01 repositório e README; E02 API executável/documentada; E03 relatório de qualidade de 1–2 páginas; E04 documento de projeto e diagrama de até uma página; E05 histórico de contribuições; E06 declarações individuais; E07 vídeo (10–15 min sugeridos). Datas confirmadas: checkpoint 18/11/2026 e final 09/12/2026.
