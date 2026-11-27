# Rastreabilidade requisito → issue → implementação → teste → documentação

Fonte: [requisitos](requisitos.md). Atualizado em 27/11/2026. Os testes de #2 e #3 existem e passam na CI (PR #29); os demais são **planejados, ainda não implementados ou executados**. Ao implementar, preencher: módulo/classe em "Implementação", caminho e nome real do teste, documento afetado (README, OpenAPI, ADR, diagrama) e link do PR. Pxx não substitui o número real da issue.

Estados: Planejado → Em andamento → Em revisão → Concluído (PR mesclado, teste passando na CI).

| Requisito | Issue | Implementação | Teste/evidência planejado | Documentação | Estado |
|---|---|---|---|---|---|
| ENG-DOC | [#1](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/1) | PR #25; [PR #26](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/26) | revisão documental; `scripts/kiro/docs_guard.py` | README, CONTEXT, CHANGELOG, steering, ADR README | Em revisão |
| ENG-INFRA | [#2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2) | `pyproject.toml`; `src/maquina_cafe/__init__.py`, `config.py` (`Settings`, `InvalidSettingsError`), `api/app.py` (`create_app`); `.env.example` ([PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29)) | `tests/integration/test_app_startup.py` (test_app_startup, test_create_app_uses_given_settings, test_create_app_reads_environment_without_settings, test_create_app_rejects_invalid_environment, test_importing_app_module_has_no_side_effects); `tests/unit/test_config.py` (test_settings_*); fumaça `scripts/ci/smoke.py`; run [46014939322](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46014939322) | README (Executar localmente), spec, arquitetura.md | Em revisão (CI verde) |
| ENG-QUAL | [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3) | `.github/workflows/ci.yml` (job `testes-e-analise`); `scripts/ci/radon_gate.py`, `smoke.py`, `summary.py`; config no `pyproject.toml` ([PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29)) | `tests/unit/test_architecture.py`; `tests/unit/test_ci_scripts.py`; run verde [46014939322](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46014939322); run vermelho provocado [46015179174](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46015179174) | README (Testes, Análise estática), ADR 0006 (aceito), quality-report.md | Em revisão (CI verde) |
| ENG-PERSIST | [#4](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/4) | — | test_initialization_idempotent | ADR 0002 (aceito, opção A) | Planejado |
| RN10 | [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) | — | test_menu_recipes_and_availability; test_menu_availability_boundaries | requisitos D-Q3; `docs/api/openapi.yaml` (GET /produtos) | Planejado |
| CAT01 | [#5](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/5) | — | test_menu_recipes_and_availability | `docs/api/openapi.yaml` (GET /produtos) | Planejado |
| EST01 | [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) | — | test_stock_alert_boundaries | — | Planejado |
| RN11 | [#6](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/6) | — | test_stock_alert_boundaries | ADR 0004 (D-4d) | Planejado |
| RN01 | [#7](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/7) | — | test_credit_denominations_and_limit; test_credit_limit_exceeded_rejects_whole_insertion; test_credit_rejected_outside_pronta | requisitos D-4a, D-4b, D-Q7; ADR 0003, 0005 | Planejado |
| RN06 | [#8](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/8) | — | test_change_all_states_and_concurrency | ADR 0002 | Planejado |
| RN02 | [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) | — | test_order_atomicity_and_concurrency | ADR 0002, 0003 | Planejado |
| RN03 | [#9](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/9) | — | test_order_atomicity_and_concurrency; test_order_rollback_on_midway_failure | ADR 0002, 0005 | Planejado |
| RN04 | [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) | — | test_preparation_deadline_and_30th_completion | — | Planejado |
| RN07 | [#10](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/10) | — | test_preparation_deadline_and_30th_completion | — | Planejado |
| RN05 | [#11](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/11) | — | test_cancel_refund_and_consumption; test_cancel_rollback_on_midway_failure; test_cancel_non_cancellable_order | ADR 0002, 0003; requisitos D-4b, D-Q8 | Planejado |
| RN11 | [#12](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/12) | — | test_operator_authentication | ADR 0004 (D-4d) | Planejado |
| RN08 | [#13](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/13) | — | test_maintenance_transitions | ADR 0003 (D-4f) | Planejado |
| RN09 | [#14](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/14) | — | test_refill_capacity_and_state | ADR 0003 (D-4f) | Planejado |
| RN07 | [#15](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/15) | — | test_cleaning_cycle | ADR 0003 (D-4f) | Planejado |
| RN10 | [#16](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/16) | — | test_price_update_and_snapshot | ADR 0005; requisitos D-4f (sem restrição de estado) | Planejado |
| RN12 | [#17](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/17) | — | test_sales_report_period_and_cancellations; test_report_period_timezones_and_invalid_input | requisitos D-4c, D-Q6; ADR 0003; `docs/api/openapi.yaml` (GET /operador/relatorio) | Planejado |
| ENG-API | [#18](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/18) | — | test_error_contract | ADR 0003, 0005 | Planejado |
| ENG-PERSIST | [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) | — | test_restart_recovery | ADR 0002 (aceito, opção A) | Planejado |
| RN03 | [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) | — | test_restart_recovery | ADR 0002, 0005 | Planejado |
| RN04 | [#19](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/19) | — | test_restart_recovery | — | Planejado |
| ENG-QUAL | [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20) | — | suite completa e relatório de cobertura | — | Planejado |
| E03 | [#20](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/20) | — | suite completa e relatório de cobertura | — | Planejado |
| ENG-DOC | [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) | `docs/api/openapi.yaml` (contrato parcial planejado) | test_openapi_contract e revisão do diagrama | `docs/api/openapi.yaml` | Planejado |
| E02 | [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) | — | test_openapi_contract e revisão do diagrama | — | Planejado |
| E04 | [#21](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/21) | — | test_openapi_contract e revisão do diagrama | — | Planejado |
| CHECKPOINT | [#22](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/22) | — | checkpoint realizado em 18/11; sem demonstração do fluxo (não havia código) | [checkpoint-18-11.md](checkpoint-18-11.md) | Concluído (fechada em 26/11; conteúdo a preencher pelo grupo) |
| E05 | [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) | — | checklist de evidências | — | Planejado |
| E06 | [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) | — | checklist de evidências | — | Planejado |
| E07 | [#23](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/23) | — | checklist de evidências | — | Planejado |
| E01 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E02 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E03 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E04 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E05 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E06 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| E07 | [#24](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/24) | — | ensaio final em ambiente limpo | — | Planejado |
| ENG-QUAL | [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) | `.github/ruleset-main.json` (recomendado); `.github/branch-protection-main.json` (alternativa) | verificação `gh api .../rules/branches/main` | configuracao-github.md | Aguardando execução pelo administrador (agente: HTTP 403) |
| ENG-QUAL | [#30](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/30) | — | CI sem `StarletteDeprecationWarning` | quality-report.md (dívida técnica) | Planejado (sem milestone) |

RN01–RN12 estão cobertas no planejamento. Aprovação desta matriz não significa aprovação da implementação. ENG-* e E01–E07 foram definidos pelo plano para rastrear engenharia e entregas.
