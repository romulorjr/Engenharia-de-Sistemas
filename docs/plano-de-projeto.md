# Plano de projeto

Base: [contexto](CONTEXT.md), [especificação](../ESI%20-%20projeto%20maquina-cafe.pdf), [requisitos](requisitos.md) e [ADR](adr/0001-escolha-da-stack.md). Atualizado em 14/10/2026.

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

## Backlog inicial
Pxx identifica o item do plano; #n identifica a issue real. Responsáveis ainda serão distribuídos pelo grupo. Milestones/labels estão previstos na configuração administrativa, ainda não aplicados.

| Plano | Issue | Requisito | Milestone | Prioridade | Dependências |
|---|---|---|---|---|---|
| P01 | [#1](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/1) Organizar documentação e governança | ENG-DOC | Fase 1 – Infra | alta | — |
| P02 | [#2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) Preparar aplicação e dependências reproduzíveis | ENG-INFRA | Fase 1 – Infra | alta | P01 |
| P03 | [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3) Configurar CI, testes e análise estática | ENG-QUAL | Fase 1 – Infra | alta | P02 |
| P04 | [#4](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/4) Criar banco, migrações e inicialização idempotente | ENG-PERSIST | Fase 1 – Infra | alta | P02 |
| P05 | [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) Implementar cardápio e disponibilidade | RN10; CAT01 | Fase 2 – Cardápio/Estoque/Crédito | alta | P04 |
| P06 | [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) Consultar estoque e alertas | EST01; RN11 | Fase 2 – Cardápio/Estoque/Crédito | alta | P04, P12 |
| P07 | [#7](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/7) Inserir crédito e validar limites | RN01 | Fase 2 – Cardápio/Estoque/Crédito | alta | P04 |
| P08 | [#8](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/8) Devolver troco | RN06 | Fase 2 – Cardápio/Estoque/Crédito | alta | P07 |
| P09 | [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) Aceitar pedido e debitar atomicamente | RN02; RN03 | Fase 3 – Pedidos/Transações | alta | P05, P07 |
| P10 | [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) Concluir preparo e controlar estados | RN04; RN07 | Fase 3 – Pedidos/Transações | alta | P09 |
| P11 | [#11](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/11) Cancelar pedido sem repor ingredientes | RN05 | Fase 3 – Pedidos/Transações | alta | P10 |
| P12 | [#12](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/12) Autenticar e autorizar operador | RN11 | Fase 2 – Cardápio/Estoque/Crédito | alta | P02 |
| P13 | [#13](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/13) Entrar e sair da manutenção | RN08 | Fase 4 – Operador/Manutenção | alta | P10, P12 |
| P14 | [#14](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/14) Reabastecer reservatórios | RN09 | Fase 4 – Operador/Manutenção | alta | P06, P13 |
| P15 | [#15](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/15) Registrar limpeza obrigatória | RN07 | Fase 4 – Operador/Manutenção | alta | P13 |
| P16 | [#16](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/16) Alterar preço de bebida | RN10 | Fase 4 – Operador/Manutenção | média | P05, P12 |
| P17 | [#17](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/17) Consultar relatório por período | RN12 | Fase 4 – Operador/Manutenção | média | P10, P11, P12, P16 |
| P18 | [#18](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/18) Padronizar validação e erros da API | ENG-API | Fase 3 – Pedidos/Transações | alta | P02, P09 |
| P19 | [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) Validar persistência e recuperação | ENG-PERSIST; RN03; RN04 | Fase 5 – Testes/Qualidade | alta | P10, P11, P15 |
| P20 | [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20) Consolidar testes de caixa-preta e relatório de qualidade | ENG-QUAL; E03 | Fase 5 – Testes/Qualidade | alta | P03, P17, P18, P19 |
| P21 | [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) Documentar API, arquitetura e padrões | ENG-DOC; E02; E04 | Fase 6 – Documentação/Vídeo | alta | P17, P18 |
| P22 | [#22](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/22) Preparar checkpoint de 18/11 | CHECKPOINT | Fase 3 – Pedidos/Transações | alta | P08, P10, P11 |
| P23 | [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) Reunir contribuições, declarações e vídeo | E05; E06; E07 | Fase 6 – Documentação/Vídeo | alta | P20, P21 |
| P24 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) Auditar e entregar os sete artefatos | E01; E02; E03; E04; E05; E06; E07 | Entrega Final | alta | P20, P21, P23 |

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
- [ ] Estoque inicial cheio apenas na primeira inicialização.
- [ ] Migrações reproduzíveis; reiniciar não restaura crédito, estoque ou estado indevidamente.

Evidência planejada: test_initialization_idempotent.

### [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) — Implementar cardápio e disponibilidade
- [ ] Cinco receitas, preços e tempos exatamente como no PDF.
- [ ] Disponibilidade considera ingredientes da receita e copo; açúcar escolhido é validado no pedido.

Evidência planejada: test_menu_recipes_and_availability.

### [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) — Consultar estoque e alertas
- [ ] Seis reservatórios com capacidades e unidades do PDF.
- [ ] Alerta estritamente abaixo do limiar; rota exige token.

Evidência planejada: test_stock_alert_boundaries.

### [#7](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/7) — Inserir crédito e validar limites
- [ ] Aceita apenas 50, 100, 200, 500, 1000 e 2000 centavos.
- [ ] Acúmulo máximo de 5000 centavos; entrada rejeitada não altera saldo.

Evidência planejada: test_credit_denominations_and_limit.

### [#8](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/8) — Devolver troco
- [ ] Devolve todo saldo e zera crédito em uma transação, em qualquer estado.
- [ ] Solicitações concorrentes não devolvem o mesmo saldo duas vezes.

Evidência planejada: test_change_all_states_and_concurrency.

### [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) — Aceitar pedido e debitar atomicamente
- [ ] Exige PRONTA, crédito e estoque inclusive açúcar de 0 a 3 porções e um copo.
- [ ] Debita e cria pedido em uma transação; falha reverte tudo; dois pedidos concorrentes não são aceitos juntos.

Evidência planejada: test_order_atomicity_and_concurrency.

### [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) — Concluir preparo e controlar estados
- [ ] Relógio substituível em testes; duração respeita receita, sem esperas reais nos testes.
- [ ] Conclusão ocorre uma única vez, inclusive após reinício; 30ª conclusão exige limpeza.

Evidência planejada: test_preparation_deadline_and_30th_completion.

### [#11](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/11) — Cancelar pedido sem repor ingredientes
- [ ] Só EM_PREPARO cancela; preço cobrado retorna uma única vez ao saldo.
- [ ] Ingredientes não retornam; cancelamento não conta como conclusão; corrida com término é testada.

Evidência planejada: test_cancel_refund_and_consumption.

### [#12](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/12) — Autenticar e autorizar operador
- [ ] Credenciais por ambiente, sem valores reais no repositório.
- [ ] Login emite token; operações de operador rejeitam token ausente/inválido; política de expiração documentada.

Evidência planejada: test_operator_authentication.

### [#13](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/13) — Entrar e sair da manutenção
- [ ] Entrada somente em PRONTA ou AGUARDANDO_LIMPEZA.
- [ ] Saída preserva limpeza pendente; transições inválidas não alteram estado.

Evidência planejada: test_maintenance_transitions.

### [#14](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/14) — Reabastecer reservatórios
- [ ] Exige manutenção e operador; quantidades/unidades válidas.
- [ ] Limite máximo aceito; excesso rejeitado sem modificação parcial.

Evidência planejada: test_refill_capacity_and_state.

### [#15](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/15) — Registrar limpeza obrigatória
- [ ] Somente em manutenção; zera contador e pendência.
- [ ] Permanece em manutenção até saída explícita; bloqueia pedido após 30 conclusões.

Evidência planejada: test_cleaning_cycle.

### [#16](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/16) — Alterar preço de bebida
- [ ] Operador altera para valor positivo, com precisão monetária documentada.
- [ ] Pedidos anteriores preservam preço cobrado para cancelamentos e relatórios.

Evidência planejada: test_price_update_and_snapshot.

### [#17](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/17) — Consultar relatório por período
- [ ] Totais e quantidades geral e por bebida; cancelados excluídos.
- [ ] Limites do período, fuso e tratamento de pedidos em preparo documentados e testados.

Evidência planejada: test_sales_report_period_and_cancellations.

### [#18](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/18) — Padronizar validação e erros da API
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
- [ ] OpenAPI e fluxo completo reproduzíveis; README atualizado.
- [ ] Documento justifica padrão ou solução simples; diagrama de até uma página fiel ao código.

Evidência planejada: test_openapi_contract e revisão do diagrama.

### [#22](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/22) — Preparar checkpoint de 18/11
- [ ] Demonstração de cardápio → crédito → pedido → conclusão → troco.
- [ ] Estado do backlog, riscos, cobertura atual e limitações apresentados ao docente.

Evidência planejada: ensaio do checkpoint.

### [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) — Reunir contribuições, declarações e vídeo
- [ ] Histórico real dos cinco integrantes e declarações individuais sem autoria fictícia.
- [ ] Vídeo sugerido de 10–15 min demonstra código, testes e fluxo; links acessíveis.

Evidência planejada: checklist de evidências.

### [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) — Auditar e entregar os sete artefatos
- [ ] Execução em ambiente limpo e revisão dos sete artefatos.
- [ ] Entrega até 09/12/2026; release/tag após revisão, com pendências declaradas.

Evidência planejada: ensaio final em ambiente limpo.

## Definition of Done
- Requisito e issue identificados; critérios de aceite demonstrados.
- Testes unitários e de integração pertinentes, incluindo limites e erros; cobertura global da aplicação >=75%. Não excluir módulos para atingir artificialmente a meta.
- CI executa testes, cobertura, lint e verificação de formatação; métricas de complexidade registradas. Aplicável a PRs de código após #3.
- Mudanças monetárias/estoque com atomicidade, persistência e concorrência verificadas quando relevantes.
- Outro integrante revisa o PR; comentários relevantes resolvidos.
- README, OpenAPI, ADR e matriz atualizados quando afetados.
- Evidências reais e autoria preservadas; nenhum segredo ou banco local versionado.
- PR somente documental: links, consistência e revisão substituem testes de aplicação que ainda não existem; não declarar cobertura fictícia.

## Branches, commits e PRs
main mantém a versão revisada para demonstração. develop integra funcionalidades. feature/<issue>-<resumo>, docs/<resumo>, fix/<issue>-<resumo> partem de develop; hotfix/* parte de main e é reincorporado a develop. O PR inicial de documentação vai para main; após integração, sincronizar develop por PR, sem reset forçado.

Usar Conventional Commits: feat, fix, docs, test, refactor, chore, ci. Exemplo: feat(credito): validar denominacoes aceitas; rodapé Refs #7. Commits pequenos e coesos, sem atribuir ao grupo trabalho não realizado por ele.

PR descreve problema, mudança, requisitos, testes executados e riscos. Preferir uma issue por PR. Exigir uma aprovação de outro integrante e checks verdes; evitar push direto em main/develop. Bloquear force push e exclusão. Os checks obrigatórios só serão nomeados na proteção depois que o workflow real existir e passar (#3).

## Testes e rastreabilidade
[Matriz requisito → issue → teste](rastreabilidade.md). Usar partição de equivalência, valores-limite e transições de estado. Ex.: crédito 49,50 + 0,50 aceito versus 50 + 0,50 rejeitado; alerta exatamente no limite não aciona; açúcar -1/0/3/4; conclusões 29/30; reposição no limite e acima. Testar falha de transação, cancelamento repetido, corrida pedido/troco e reinício. Relógio controlado evita sleeps. Testes previstos ainda não existem.

## Riscos e mitigação
| Risco | Mitigação |
|---|---|
| Prazo e aprendizado da stack | Fluxo vertical primeiro; ambiente reproduzível; revisão do plano no checkpoint |
| Débito duplicado / estoque negativo | Transações, serialização e testes concorrentes reais |
| Divergência de estado após reinício | Persistir término previsto e testar recuperação idempotente |
| Requisitos ambíguos | Resolver questões de requisitos.md na issue antes da implementação |
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
Revisar PR inicial; aplicar configuração GitHub; distribuir responsáveis; iniciar #2, #3 e #4. Confirmar licença antes de adicionar LICENSE. Criar a aplicação e fixar dependências antes de prometer comandos funcionais.
