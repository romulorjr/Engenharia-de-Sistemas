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

## Decisões de interpretação (25/11/2026)
Decididas pelo responsável (romulorjr) em 25/11/2026. Complementam o PDF onde ele é omisso; não o substituem. Mapeamento HTTP completo no [ADR 0003](adr/0003-modelo-de-erros.md).

| Id | Tema | Decisão | Justificativa | Registro | Issues |
|---|---|---|---|---|---|
| D-4a | Crédito fora de PRONTA | Crédito só é aceito em PRONTA. Em PREPARANDO: 409 `MAQUINA_OCUPADA`. Em MANUTENCAO ou AGUARDANDO_LIMPEZA: 503 (`MAQUINA_EM_MANUTENCAO` / `LIMPEZA_PENDENTE`), os mesmos códigos de `POST /pedidos` no mesmo estado. O troco (RN06) continua permitido em qualquer estado. | "PRONTA: aceita crédito e pedidos" é o único estado que aceita crédito explicitamente; os demais recusam ou bloqueiam pedidos, e receber dinheiro sem poder servir prejudica o cliente. | ADR 0003 | #7 |
| D-4b | Restituição acima de R$ 50 | Não ocorre. Uma inserção que levaria o saldo acima de R$ 50,00 é rejeitada inteira, sem aceitação parcial, e o saldo não muda. | Pela D-4a, o saldo só cresce em PRONTA e sempre ≤ R$ 50. Entre a aceitação e o cancelamento a máquina está PREPARANDO, então o saldo só pode diminuir (troco). A restituição (RN05) devolve o preço cobrado no pedido, que saiu desse mesmo saldo: saldo final ≤ (saldo anterior − preço) + preço ≤ R$ 50. A restituição usa o preço gravado no pedido, não o preço atual. | ADR 0003 | #7, #11 |
| D-4c | Período do relatório | `GET /operador/relatorio?from=...&to=...`. Os dois parâmetros são obrigatórios, em ISO 8601 (ex.: `2026-11-01T00:00:00`), ambos inclusivos. Ausente ou inválido: 400 `DADOS_INVALIDOS`. Documentado no OpenAPI e na descrição do endpoint. | Decisão do responsável. | ADR 0003 | #17, #21 |
| D-4d | Token do operador | JWT HS256 com validade de 1 hora; segredo e credenciais em variáveis de ambiente. Token ausente, inválido ou expirado: 401 `NAO_AUTORIZADO`. | Atende RN11 sem estado no servidor. | [ADR 0004](adr/0004-autenticacao-operador-jwt.md) | #12 |
| D-4e | Dinheiro no JSON | Reais com duas casas decimais nos corpos de requisição e resposta (ex.: `4.50`); centavos inteiros em toda a aritmética interna. Mais de duas casas: 400. | Segue os exemplos do PDF e evita erros de ponto flutuante. | [ADR 0005](adr/0005-representacao-monetaria.md) | #18, #7, #16, #17 |
| D-4f | Operador no estado errado | 409 `ESTADO_INVALIDO` (ex.: reabastecer ou limpar fora de MANUTENCAO; entrar em manutenção fora de PRONTA/AGUARDANDO_LIMPEZA; sair sem estar em MANUTENCAO). 503 fica reservado às chamadas do cliente com a máquina indisponível. A alteração de preço não tem restrição de estado, porque RN10 não define nenhuma. | Decisão do responsável. | ADR 0003 | #13, #14, #15, #16 |

Escolha feita pelo agente dentro da D-4a, que admitia "409 ou o mesmo código do cliente": usar os códigos de `POST /pedidos` por estado. Pode ser revertida para 409 em todos os estados se o responsável preferir.

## Engenharia
- ENG-INFRA: aplicação reproduzível e versionada.
- ENG-PERSIST: estoque, crédito, estado e pedidos persistem entre reinicializações.
- ENG-API: validação e erros consistentes; exemplos: 404 inexistente, 400 dados inválidos, 402 crédito insuficiente, 409 estoque insuficiente/ocupada, 503 manutenção/limpeza, 401 token inválido, 422 excesso de reposição.
- ENG-QUAL: testes unitários e de integração; cobertura mínima de 75%; critérios de caixa-preta; análise estática e métricas.
- ENG-DOC: API documentada; separação de responsabilidades; decisão sobre padrão e diagrama de até uma página.

## Questões a resolver antes das respectivas implementações
Não são requisitos adicionais confirmados. Respostas são registradas na seção anterior e em [CONTEXT](CONTEXT.md#decisões).

**Resolvidas em 25/11/2026**
- **Q1** Crédito fora de PRONTA e restituição acima de R$ 50 → D-4a e D-4b.
- **Q2** Período do relatório → D-4c (parâmetros, formato, inclusividade). Detalhes restantes na Q6.
- **Q4** Expiração do token e representação monetária → D-4d e D-4e.
- **Q5** Código HTTP do operador no estado errado → D-4f.

**Em aberto** (propostas do agente; não bloqueiam M1)
- **Q3** Disponibilidade no cardápio não recebe açúcar escolhido. Proposta: receita base e copo, com validação completa do açúcar no pedido (#5/#9). Disponibilidade considera só estoque, como define RN10; o estado da máquina aparece em `/status`. Necessária antes de #5 (M2).
- **Q6** Detalhes do relatório não cobertos pela D-4c. Necessária antes de #17 (M3). Propostas:
  - valor sem fuso (`2026-11-01T00:00:00`) interpretado em America/Sao_Paulo; valor com fuso (`...-03:00`, `...Z`) aceito e convertido;
  - data sem hora (`2026-11-01`) rejeitada com 400, para que `to` inclusivo não exclua o próprio dia por engano;
  - `from` posterior a `to`: 400 `DADOS_INVALIDOS`;
  - contam apenas pedidos CONCLUIDO, pelo instante de conclusão e pelo preço cobrado. Pedidos EM_PREPARO ainda podem ser cancelados e ficam de fora.
- **Q7** Código para inserção que excede R$ 50,00 (D-4b não definiu). Proposta: 400 `LIMITE_CREDITO_EXCEDIDO`, pela linha "valor de crédito não aceito → 400" do PDF. Necessária antes de #7 (M2).
- **Q8** Código para cancelar pedido que não está EM_PREPARO (já CONCLUIDO ou CANCELADO). Proposta: 409 `PEDIDO_NAO_CANCELAVEL`. Necessária antes de #11 (M2).

## Entregas
E01 repositório e README; E02 API executável/documentada; E03 relatório de qualidade de 1–2 páginas; E04 documento de projeto e diagrama de até uma página; E05 histórico de contribuições; E06 declarações individuais; E07 vídeo (10–15 min sugeridos). Datas confirmadas: checkpoint 18/11/2026 e final 09/12/2026.
