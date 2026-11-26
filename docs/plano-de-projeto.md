# Plano de projeto

Base: [contexto](CONTEXT.md), [especificação](../ESI%20-%20projeto%20maquina-cafe.pdf), [requisitos](requisitos.md) e [ADR](adr/0001-escolha-da-stack.md). Criado em 14/10/2026; atualizado em 25/11/2026 com o [replanejamento aprovado](#replanejamento-aprovado-em-25112026) e o novo [fluxo de branches](#branches-commits-e-prs).

## Objetivo e estratégia
Entregar um MVP de uma máquina de café como API REST persistente, cobrindo RN01–RN12, com testes e documentação. Começar por um fluxo vertical: cardápio → crédito → pedido → preparo → troco. Acrescentar operador e relatórios sem concentrar regras nos controllers. Nenhuma funcionalidade está implementada nesta base.

## Cronograma e milestones
Datas em 2026, America/Sao_Paulo. O PDF define grupos 12–16/10, infraestrutura 19–25/10, cardápio/estoque/crédito 26/10–01/11, transações 02–29/11 e fechamento/documentação/vídeo 03/11–08/12. A sobreposição de documentação é mantida. Checkpoint 18/11 e entrega 09/12 são datas confirmadas; subdivisões abaixo são planejamento interno, não novos prazos do docente.

| Milestone | Período | Vencimento | Resultado |
|---|---|---|---|
| Fase 1 – Infra | 19–25/10 | 2026-10-25 | Documentação, ambiente, CI e persistência inicial. |
| Fase 2 – Cardápio/Estoque/Crédito | 26/10–01/11 | 2026-11-01 | Cardápio, estoque, crédito, troco e autenticação básica. |
| Fase 3 – Pedidos/Transações | 02–18/11 | 2026-11-18 | Pedidos atômicos, preparo, cancelamento e checkpoint em 18/11. |
| Fase 4 – Operador/Manutenção | 19–29/11 | 2026-11-29 | Limpeza, reposição, manutenção, preços e relatórios. |
| Fase 5 – Testes/Qualidade | 30/11–02/12 | 2026-12-02 | Consolidação; testes são desenvolvidos desde a infraestrutura. |
| Fase 6 – Documentação/Vídeo | 03/11–08/12 | 2026-12-08 | Documentação contínua, relatórios, declarações e vídeo. |
| Entrega Final | 09/12 | 2026-12-09 | Entrega dos sete artefatos revisados. |

Até 16/10: confirmar papéis e usuários GitHub. Até 18/11: demonstrar o fluxo vertical, apresentar testes disponíveis e riscos. As sete entregas são artefatos, não fases.

Situação em 25/11/2026: nenhum milestone foi criado no GitHub e nenhuma issue de código foi iniciada. As Fases 1–3 venceram sem entregas e o checkpoint de 18/11 passou. O cronograma acima fica como registro histórico, substituído pelo replanejamento abaixo.

## Replanejamento aprovado em 25/11/2026
**Status: aprovado pelo responsável em 25/11/2026 (decisão 1).** Faltam 14 dias para 09/12. Cada milestone termina com um resultado verificável por teste ou demonstração. As datas são planejamento interno; checkpoint e entrega final continuam conforme o PDF.

| Milestone | Período | Vencimento | Issues | Resultado verificável |
|---|---|---|---|---|
| M1 – Base técnica | 26–27/11 | 2026-11-27 | #1, #2, #3, #4, #18 (contrato de erro), #27 (proteção de `main`) | Aplicação inicia; CI executa pytest com cobertura ≥75%, Ruff e Radon; banco inicializa cheio uma única vez |
| M2 – Fluxo do cliente | 28/11–01/12 | 2026-12-01 | #5, #7, #8, #9, #10, #11 | Exemplo da seção 2 do PDF (cappuccino, R$ 10,00, troco R$ 3,50) reproduzido em teste de integração e no Swagger |
| M3 – Operador e manutenção | 02–03/12 | 2026-12-03 | #12, #6, #13, #15, #14, #16, #17, #19 | Rotas `/operador/*` com token; ciclo de 30 preparos e limpeza; reinício preserva estoque, crédito, estado e pedidos |
| M4 – Qualidade e documentação | 04–06/12 | 2026-12-06 | #20, #21 | Relatório de qualidade, documento de projeto com diagrama, OpenAPI exportado e coleção Postman, declarações |
| M5 – Entrega | 07–09/12 | 2026-12-09 | #23, #24 | Ensaio em ambiente limpo, vídeo de 10–15 min, tag de release |

Congelamento de funcionalidades em 03/12. O período de 04 a 06/12 fica reservado para correções, documentação e ensaio.

Vínculos no GitHub: ver [configuração do GitHub](configuracao-github.md#estado-em-25112026). Uma issue só pode ter um milestone:
- #1 (governança) entra em M1 e fecha com o PR #26.
- #18 entra em M1 porque o envelope e o mapeamento de erros ([ADR 0003](adr/0003-modelo-de-erros.md)) são base para todas as rotas. A validação de cada rota é feita na issue da rota e verificada por `test_error_contract` ao longo de M2–M3.
- #23 entra em M5 (vídeo). As declarações individuais de #23 têm meta interna de 06/12.
- #22 ficou sem milestone e foi fechada em 25/11: o checkpoint aconteceu em 18/11 ([registro](checkpoint-18-11.md)).
- #27 foi criada em 25/11 para a proteção de `main`, que o agente não conseguiu aplicar (HTTP 403), e entrou em M1.

**Regra de re-escopo.** Depois de criados os milestones, nenhuma issue muda de milestone silenciosamente. Se um milestone precisar de re-escopo, abrir uma issue nova descrevendo o que sai, o que entra e o motivo, e registrá-la aqui e no [CONTEXT](CONTEXT.md).

**Ordem e paralelismo.** M1 é sequencial (#2 → #3 e #4). #4 segue o [ADR 0002](adr/0002-persistencia-e-atomicidade.md), aceito em 25/11 (opção A: SQLAlchemy + Alembic). Em M2, #5, #7 e #8 podem andar em paralelo; #9 depende de #5 e #7; #10 de #9; #11 de #10. Em M3, #12 libera as rotas do operador; #13 antecede #14 e #15.

**Linha de corte.** O PDF permite selecionar as regras viáveis no prazo. Se M2 atrasar, a prioridade é:
1. Obrigatório: RN01–RN06, RN11, persistência, contrato de erros, Swagger e testes com cobertura ≥75%.
2. Em seguida: RN07, RN08, RN09 e consulta de estoque (#6, #13, #14, #15).
3. Por último: RN10 alteração de preço (#16) e RN12 relatório (#17).

Qualquer corte será registrado no README, no relatório de qualidade e no vídeo, sem apresentar regra não implementada como entregue.

**Issue fora do novo cronograma.** #22 (checkpoint de 18/11) foi fechada em 25/11 com o registro em [checkpoint-18-11.md](checkpoint-18-11.md); o que foi apresentado e o retorno do docente ainda precisam ser preenchidos pelo grupo.

**Distribuição.** Cada integrante deve assumir ao menos uma issue de código e revisar ao menos um PR de outra pessoa, para que E05 e E06 reflitam a participação real. A distribuição será registrada nas issues e em [contribuições](contributions.md).

## Backlog inicial
Pxx identifica o item do plano; #n identifica a issue real. Responsáveis ainda serão distribuídos pelo grupo. Milestones M1–M5 aplicados no GitHub em 25/11/2026; labels ainda não aplicadas.

| Plano | Issue | Requisito | Milestone | Prioridade | Dependências |
|---|---|---|---|---|---|
| P01 | [#1](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/1) Organizar documentação e governança | ENG-DOC | M1 – Base técnica | alta | — |
| P02 | [#2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) Preparar aplicação e dependências reproduzíveis | ENG-INFRA | M1 – Base técnica | alta | P01 |
| P03 | [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3) Configurar CI, testes e análise estática | ENG-QUAL | M1 – Base técnica | alta | P02 |
| P04 | [#4](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/4) Criar banco, migrações e inicialização idempotente | ENG-PERSIST | M1 – Base técnica | alta | P02 |
| P05 | [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) Implementar cardápio e disponibilidade | RN10; CAT01 | M2 – Fluxo do cliente | alta | P04 |
| P06 | [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) Consultar estoque e alertas | EST01; RN11 | M3 – Operador e manutenção | alta | P04, P12 |
| P07 | [#7](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/7) Inserir crédito e validar limites | RN01 | M2 – Fluxo do cliente | alta | P04 |
| P08 | [#8](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/8) Devolver troco | RN06 | M2 – Fluxo do cliente | alta | P07 |
| P09 | [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) Aceitar pedido e debitar atomicamente | RN02; RN03 | M2 – Fluxo do cliente | alta | P05, P07 |
| P10 | [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) Concluir preparo e controlar estados | RN04; RN07 | M2 – Fluxo do cliente | alta | P09 |
| P11 | [#11](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/11) Cancelar pedido sem repor ingredientes | RN05 | M2 – Fluxo do cliente | alta | P10 |
| P12 | [#12](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/12) Autenticar e autorizar operador | RN11 | M3 – Operador e manutenção | alta | P02 |
| P13 | [#13](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/13) Entrar e sair da manutenção | RN08 | M3 – Operador e manutenção | alta | P10, P12 |
| P14 | [#14](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/14) Reabastecer reservatórios | RN09 | M3 – Operador e manutenção | alta | P06, P13 |
| P15 | [#15](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/15) Registrar limpeza obrigatória | RN07 | M3 – Operador e manutenção | alta | P13 |
| P16 | [#16](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/16) Alterar preço de bebida | RN10 | M3 – Operador e manutenção | média | P05, P12 |
| P17 | [#17](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/17) Consultar relatório por período | RN12 | M3 – Operador e manutenção | média | P10, P11, P12, P16 |
| P18 | [#18](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/18) Padronizar validação e erros da API | ENG-API | M1 – Base técnica | alta | P02 (contrato); validação por rota acompanha P05–P17 |
| P19 | [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) Validar persistência e recuperação | ENG-PERSIST; RN03; RN04 | M3 – Operador e manutenção | alta | P10, P11, P15 |
| P20 | [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20) Consolidar testes de caixa-preta e relatório de qualidade | ENG-QUAL; E03 | M4 – Qualidade e documentação | alta | P03, P17, P18, P19 |
| P21 | [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) Documentar API, arquitetura e padrões | ENG-DOC; E02; E04 | M4 – Qualidade e documentação | alta | P17, P18 |
| P22 | [#22](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/22) Preparar checkpoint de 18/11 | CHECKPOINT | — (sem milestone; fechada em 25/11) | alta | P08, P10, P11 |
| P23 | [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) Reunir contribuições, declarações e vídeo | E05; E06; E07 | M5 – Entrega | alta | P20, P21 |
| P24 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) Auditar e entregar os sete artefatos | E01; E02; E03; E04; E05; E06; E07 | M5 – Entrega | alta | P20, P21, P23 |
| P25 | [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) Aplicar proteção da branch main | ENG-QUAL | M1 – Base técnica | alta | — (passo 2 depende de P03) |

## Critérios de aceite por issue

### [#1](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/1) — Organizar documentação e governança
- [ ] README, contexto, plano, ADR e templates revisáveis em PR.
- [ ] PDF preservado; nenhuma funcionalidade apresentada como implementada.

Evidência planejada: revisão documental.

### [#2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) — Preparar aplicação e dependências reproduzíveis
- [ ] Aplicação FastAPI inicializa em ambiente limpo com versões fixadas.
- [ ] Comandos de instalação e execução comprovados; configuração via ambiente.

Evidência planejada: test_app_startup.

### [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3) — Configurar CI, testes e análise estática
- [ ] PRs executam pytest, cobertura mínima de 75%, Ruff check e format check.
- [ ] Relatórios publicados; falhas bloqueiam aprovação, sem ignorar ausência de testes.

Evidência planejada: validação do workflow em PR.

### [#4](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/4) — Criar banco, migrações e inicialização idempotente
- [x] Opção de persistência do [ADR 0002](adr/0002-persistencia-e-atomicidade.md) escolhida e ADR aceito antes do código (25/11: opção A).
- [ ] Migrações Alembic com `render_as_batch=True`; só `persistence/` importa `sqlalchemy` e `alembic`.
- [ ] Transações de escrita com `BEGIN IMMEDIATE`; repositories não fazem commit.
- [ ] Estoque inicial cheio apenas na primeira inicialização.
- [ ] Migrações reproduzíveis; reiniciar não restaura crédito, estoque ou estado indevidamente.

Evidência planejada: test_initialization_idempotent.

### [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) — Implementar cardápio e disponibilidade
- [ ] Cinco receitas, preços e tempos exatamente como no PDF.
- [ ] Disponibilidade considera ingredientes da receita e copo; açúcar escolhido é validado no pedido.
- [ ] D-Q3: `disponivel: true` quando há estoque para uma unidade (água, café, leite, chocolate e açúcar da receita, açúcar da receita = 0 g) e ao menos 1 copo; crédito e estado da máquina não entram no cálculo. Descrição igual à de `GET /produtos` em `docs/api/openapi.yaml`.

Evidência planejada: test_menu_recipes_and_availability; test_menu_availability_boundaries (limite exato de cada ingrediente, uma unidade a menos, 0 copo, açúcar zerado, máquina em MANUTENCAO, crédito zero).

### [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) — Consultar estoque e alertas
- [ ] Seis reservatórios com capacidades e unidades do PDF.
- [ ] Alerta estritamente abaixo do limiar; rota exige token.

Evidência planejada: test_stock_alert_boundaries.

### [#7](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/7) — Inserir crédito e validar limites
- [ ] Crédito só em PRONTA: PREPARANDO → 409 `MAQUINA_OCUPADA`; MANUTENCAO/AGUARDANDO_LIMPEZA → 503 (D-4a).
- [ ] Inserção que excederia R$ 50,00 é rejeitada inteira, sem aceitação parcial (D-4b).
- [ ] Valores em reais com até duas casas; mais casas → 400 (D-4e).
- [ ] D-Q7: inserção que excederia R$ 50,00 → 400 `LIMITE_CREDITO_EXCEDIDO`, saldo inalterado.
- [ ] Aceita apenas 50, 100, 200, 500, 1000 e 2000 centavos.
- [ ] Acúmulo máximo de 5000 centavos; entrada rejeitada não altera saldo.

Evidência planejada: test_credit_denominations_and_limit; test_credit_limit_exceeded_rejects_whole_insertion (49,50 + 0,50 aceito; 50,00 + 0,50 e 45,00 + 10,00 rejeitados com 400 `LIMITE_CREDITO_EXCEDIDO` e saldo inalterado); test_credit_rejected_outside_pronta.

### [#8](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/8) — Devolver troco
- [ ] Devolve todo saldo e zera crédito em uma transação, em qualquer estado.
- [ ] Solicitações concorrentes não devolvem o mesmo saldo duas vezes.

Evidência planejada: test_change_all_states_and_concurrency.

### [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) — Aceitar pedido e debitar atomicamente
- [ ] `test_order_rollback_on_midway_failure`: falha injetada após o débito deixa saldo, estoque, estado e pedidos inalterados (ADR 0002).
- [ ] Exige PRONTA, crédito e estoque inclusive açúcar de 0 a 3 porções e um copo.
- [ ] Debita e cria pedido em uma transação; falha reverte tudo; dois pedidos concorrentes não são aceitos juntos.

Evidência planejada: test_order_atomicity_and_concurrency.

### [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) — Concluir preparo e controlar estados
- [ ] Relógio substituível em testes; duração respeita receita, sem esperas reais nos testes.
- [ ] Conclusão ocorre uma única vez, inclusive após reinício; 30ª conclusão exige limpeza.

Evidência planejada: test_preparation_deadline_and_30th_completion.

### [#11](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/11) — Cancelar pedido sem repor ingredientes
- [ ] `test_cancel_rollback_on_midway_failure`: falha injetada após a restituição deixa pedido EM_PREPARO e saldo inalterado (ADR 0002).
- [ ] Restituição usa o preço cobrado no pedido; saldo nunca passa de R$ 50,00 (D-4b).
- [ ] D-Q8: cancelar pedido CONCLUIDO ou CANCELADO → 409 `PEDIDO_NAO_CANCELAVEL`; saldo, estoque e estado inalterados.
- [ ] Só EM_PREPARO cancela; preço cobrado retorna uma única vez ao saldo.
- [ ] Ingredientes não retornam; cancelamento não conta como conclusão; corrida com término é testada.

Evidência planejada: test_cancel_refund_and_consumption; test_cancel_rollback_on_midway_failure; test_cancel_non_cancellable_order (CONCLUIDO, CANCELADO e cancelamento repetido → 409; inexistente → 404).

### [#12](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/12) — Autenticar e autorizar operador
- [ ] JWT HS256 com validade de 1 hora; `OPERADOR_USUARIO`, `OPERADOR_SENHA` e `JWT_SECRET` por ambiente (D-4d, [ADR 0004](adr/0004-autenticacao-operador-jwt.md)).
- [ ] Token ausente, inválido ou expirado → 401 `NAO_AUTORIZADO`; credenciais erradas → 401 `CREDENCIAIS_INVALIDAS`.
- [ ] Credenciais por ambiente, sem valores reais no repositório.
- [ ] Login emite token; operações de operador rejeitam token ausente/inválido; política de expiração documentada.

Evidência planejada: test_operator_authentication.

### [#13](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/13) — Entrar e sair da manutenção
- [ ] Transição inválida → 409 `ESTADO_INVALIDO` (D-4f).
- [ ] Entrada somente em PRONTA ou AGUARDANDO_LIMPEZA.
- [ ] Saída preserva limpeza pendente; transições inválidas não alteram estado.

Evidência planejada: test_maintenance_transitions.

### [#14](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/14) — Reabastecer reservatórios
- [ ] Fora de MANUTENCAO → 409 `ESTADO_INVALIDO` (D-4f); acima da capacidade → 422 `CAPACIDADE_EXCEDIDA`.
- [ ] Exige manutenção e operador; quantidades/unidades válidas.
- [ ] Limite máximo aceito; excesso rejeitado sem modificação parcial.

Evidência planejada: test_refill_capacity_and_state.

### [#15](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/15) — Registrar limpeza obrigatória
- [ ] Fora de MANUTENCAO → 409 `ESTADO_INVALIDO` (D-4f).
- [ ] Somente em manutenção; zera contador e pendência.
- [ ] Permanece em manutenção até saída explícita; bloqueia pedido após 30 conclusões.

Evidência planejada: test_cleaning_cycle.

### [#16](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/16) — Alterar preço de bebida
- [ ] Preço em reais com até duas casas e maior que zero (D-4e); sem restrição de estado (D-4f).
- [ ] Operador altera para valor positivo, com precisão monetária documentada.
- [ ] Pedidos anteriores preservam preço cobrado para cancelamentos e relatórios.

Evidência planejada: test_price_update_and_snapshot.

### [#17](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/17) — Consultar relatório por período
- [ ] Parâmetros `from` e `to` obrigatórios, ISO 8601, ambos inclusivos; ausente ou inválido → 400; documentados no OpenAPI (D-4c).
- [ ] D-Q6: com ou sem fuso; sem fuso = America/Sao_Paulo (UTC−03:00); `Z` e deslocamentos aceitos; data sem hora → 400; `from` > `to` → 400; só CONCLUIDO, pelo instante de conclusão. Descrição e exemplos iguais aos de `docs/api/openapi.yaml`.
- [ ] Totais e quantidades geral e por bebida; cancelados excluídos.
- [ ] Limites do período, fuso e tratamento de pedidos em preparo documentados e testados.

Evidência planejada: test_sales_report_period_and_cancellations; test_report_period_timezones_and_invalid_input (mesmo instante com e sem fuso dá o mesmo relatório; limites `from` e `to` exatos incluídos; data sem hora, valor inválido, ausente e `from` > `to` → 400).

### [#18](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/18) — Padronizar validação e erros da API
- [ ] Envelope `erro`/`mensagem` e mapeamento do [ADR 0003](adr/0003-modelo-de-erros.md); validação do FastAPI convertida de 422 para 400.
- [ ] Dinheiro conforme [ADR 0005](adr/0005-representacao-monetaria.md): reais com duas casas no JSON, centavos internamente.
- [ ] Contrato de erro consistente, com casos 400, 401, 402, 404, 409, 422 e 503 documentados.
- [ ] Validação de açúcar, identificadores e dinheiro cobre entradas inválidas sem mutação.

Evidência planejada: test_error_contract.

### [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) — Validar persistência e recuperação
- [ ] Reabrir banco conserva estoque, crédito, estado e pedidos.
- [ ] Falha transacional e reinicialização durante preparo não duplicam consumo ou conclusão.

Evidência planejada: test_restart_recovery.

### [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20) — Consolidar testes de caixa-preta e relatório de qualidade
- [ ] Partições, limites e transições rastreados para RN01–RN12.
- [ ] Cobertura >=75% medida, relatório de 1–2 páginas com métricas e análise estática.

Evidência planejada: suite completa e relatório de cobertura.

### [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) — Documentar API, arquitetura e padrões
- [ ] OpenAPI declara as respostas de erro do ADR 0003 por rota, o formato monetário do ADR 0005 e os parâmetros `from`/`to`.
- [ ] OpenAPI gerado exportado em `docs/api/openapi.yaml`, substituindo o contrato parcial de 25/11; test_openapi_contract confirma que as descrições de D-Q3 e D-Q6 e os exemplos de `from`/`to` estão presentes.
- [ ] OpenAPI e fluxo completo reproduzíveis; README atualizado.
- [ ] Documento justifica padrão ou solução simples; diagrama de até uma página fiel ao código.

Evidência planejada: test_openapi_contract e revisão do diagrama.

### [#22](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/22) — Preparar checkpoint de 18/11
Fechada em 25/11/2026. Checkpoint realizado em 18/11; registro em [checkpoint-18-11.md](checkpoint-18-11.md).
- [ ] Demonstração de cardápio → crédito → pedido → conclusão → troco. Não atendido: não havia código em 18/11; coberto por M2 e pelo vídeo.
- [ ] Estado do backlog, riscos, cobertura atual e limitações apresentados ao docente. A confirmar pelo grupo no registro.

Evidência: [checkpoint-18-11.md](checkpoint-18-11.md).

### [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) — Reunir contribuições, declarações e vídeo
- [ ] Histórico real dos cinco integrantes e declarações individuais sem autoria fictícia.
- [ ] Vídeo sugerido de 10–15 min demonstra código, testes e fluxo; links acessíveis.

Evidência planejada: checklist de evidências.

### [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) — Auditar e entregar os sete artefatos
- [ ] Execução em ambiente limpo e revisão dos sete artefatos.
- [ ] Entrega até 09/12/2026; release/tag após revisão, com pendências declaradas.

Evidência planejada: ensaio final em ambiente limpo.

### [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) — Aplicar proteção da branch main
- [ ] Proteção de `.github/branch-protection-main.json` aplicada por administrador e verificada; push direto em `main` recusado.
- [ ] Após a #3, check da CI exigido na proteção.

Evidência planejada: saída do comando de verificação registrada em configuracao-github.md.

## Definition of Done
- Requisito e issue identificados; critérios de aceite demonstrados. Funcionalidades e refatorações têm spec em `.kiro/specs/<issue>-<resumo>/`.
- Código nas camadas corretas: controllers sem regra de negócio; regras em serviços/domínio; SQL apenas na persistência.
- Testes unitários e de integração pertinentes, incluindo limites e erros; cobertura global da aplicação >=75%. Não excluir módulos para atingir artificialmente a meta.
- CI executa testes, cobertura, lint e verificação de formatação; métricas de complexidade registradas; nenhum problema crítico novo. Aplicável a PRs de código após #3.
- Mudanças monetárias/estoque com atomicidade, persistência e concorrência verificadas quando relevantes.
- Outro integrante revisa o PR; comentários relevantes resolvidos.
- OpenAPI/Postman atualizados quando a API muda, com exemplos e códigos de erro.
- README, [CONTEXT](CONTEXT.md), [CHANGELOG](../CHANGELOG.md), ADR (se aplicável), diagrama, [matriz](rastreabilidade.md), [relatório de qualidade](quality-report.md) e [contribuições](contributions.md) atualizados quando afetados.
- Evidências reais e autoria preservadas; nenhum segredo ou banco local versionado.
- PR somente documental: links, consistência e revisão substituem testes de aplicação que ainda não existem; não declarar cobertura fictícia.

## Branches, commits e PRs
Decisão do responsável em 25/11/2026 (decisão 2): `develop` foi abandonada.

- `main` é a única branch de longa duração e contém a versão revisada.
- Branches de trabalho partem de `main`: `feature/<issue>-<resumo>`, `fix/<issue>-<resumo>`, `docs/<resumo>`, `test/<issue>-<resumo>`.
- Todo PR mira `main`, segue o [template](../.github/PULL_REQUEST_TEMPLATE.md) e precisa de aprovação de outro integrante.
- Proteção de `main` decidida: PR obrigatório com 1 aprovação, aprovações descartadas após novo push, conversas resolvidas, regras valendo também para administradores, sem force push e sem exclusão. Configuração em `.github/branch-protection-main.json`. **Ainda não aplicada:** a integração do agente recebeu HTTP 403 (sem permissão de administração). Aplicação manual pelo administrador na [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) (M1). Até lá, a regra vale por acordo da equipe.
- CI verde obrigatória: o check será exigido assim que o workflow da #3 existir e passar uma vez (passo 2 da #27). Antes disso não há nome de check para cadastrar.
- `develop` estava atrás de `main` (seu único commit, ce5eca4, já está em `main`). Foi arquivada como a tag `archive/develop` e a branch remota foi removida. Para consultar: `git checkout archive/develop`.

Usar Conventional Commits: feat, fix, docs, test, refactor, chore, ci. Exemplo: feat(credito): validar denominacoes aceitas; rodapé Refs #7. Commits pequenos e coesos, sem atribuir ao grupo trabalho não realizado por ele.

PR descreve problema, mudança, requisitos, testes executados e riscos. Preferir uma issue por PR.

## Testes e rastreabilidade
[Matriz requisito → issue → teste](rastreabilidade.md). Usar partição de equivalência, valores-limite e transições de estado. Ex.: crédito 49,50 + 0,50 aceito versus 50 + 0,50 rejeitado; alerta exatamente no limite não aciona; açúcar -1/0/3/4; conclusões 29/30; reposição no limite e acima. Testar falha de transação, cancelamento repetido, corrida pedido/troco e reinício. Relógio controlado evita sleeps. Testes previstos ainda não existem.

## Riscos e mitigação
| Risco | Mitigação |
|---|---|
| Prazo e aprendizado da stack | Fluxo vertical primeiro; ambiente reproduzível; revisão do plano no checkpoint |
| Débito duplicado / estoque negativo | Transações, serialização e testes concorrentes reais |
| Divergência de estado após reinício | Persistir término previsto e testar recuperação idempotente |
| Requisitos ambíguos | Resolver questões de requisitos.md na issue antes da implementação; decisões de 25/11 registradas em requisitos.md e ADRs 0003–0005 |
| Hooks do Kiro não verificados como ativos | Executar testes e análise estática à mão (README) até a verificação; CI da #3 é a garantia que vale |
| Proteção de `main` exige revisão de outro integrante | Revisores definidos por issue; PRs pequenos para revisão rápida |
| SQLite e concorrência | Configurar transações explicitamente, testar conexões independentes; reavaliar PostgreSQL se necessário |
| Cobertura apenas numérica | Caixa-preta, limites e transições; revisar qualidade das asserções |
| Participação concentrada | Distribuir issues e revisões; preservar histórico e declarações individuais |
| Vídeo/documentação tardios | Atualizar desde 03/11; ensaiar fluxo em ambiente limpo antes de 08/12 |
| Administração GitHub indisponível pelo conector | Aplicar script idempotente com GitHub CLI autenticado e conferir resultados |

## Evidências das sete entregas
| Entrega | Evidência final prevista | Issue |
|---|---|---|
| E01 | README, instruções reproduzíveis e histórico do repositório | #1, #24 |
| E02 | API executável, OpenAPI e fluxo completo | #2, #21 |
| E03 | Relatório de 1–2 páginas, cobertura e métricas de análise | #20 |
| E04 | Documento de projeto com decisão de padrão e diagrama de até uma página | #21 |
| E05 | Histórico real de commits, PRs e revisões dos integrantes | #23 |
| E06 | Declarações individuais curtas e verificáveis | #23 |
| E07 | Vídeo de demonstração; 10–15 minutos sugeridos | #23 |

## Próximas ações
Atualizado em 25/11/2026 (segunda rodada de decisões). Revisar as specs de #2 e #3 e autorizar a implementação. Aplicar a proteção de `main` (#27, passo a). Obter revisão de outro integrante e mesclar o PR #26 (#1). Executar `scripts/configure-github.ps1 -Apply` e registrar o resultado. Preencher o registro do checkpoint (#22). Distribuir responsáveis pelas issues de M2. Quando o workflow da #3 passar, exigir o check na proteção de `main` (#27, passo b).
