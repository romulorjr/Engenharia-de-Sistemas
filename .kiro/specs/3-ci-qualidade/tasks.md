# Tarefas — #3 Configurar CI, testes e análise estática

Requisitos: [requirements.md](requirements.md). Design: [design.md](design.md). Status: **em andamento** desde 27/11/2026 (spec aprovada).

Implementação no mesmo PR da [#2](../2-aplicacao-base/tasks.md), depois das tarefas 1–5 da #2, em commits separados com `Refs #3`.

- [ ] 1. Configurar pytest, coverage e Ruff no `pyproject.toml`
  - Seções `[tool.pytest.ini_options]`, `[tool.coverage.*]`, `[tool.ruff]` do design; extra `dev` com pytest-cov, ruff e radon fixados.
  - Rodar `ruff check` e `ruff format --check` localmente (Ruff disponível no ambiente do agente).
  - _Requisitos: 1.1, 2.1, 2.3, 3.1_

- [ ] 2. Implementar o teste de camadas
  - `tests/unit/test_architecture.py` com a tabela de proibições do design; caso que prova a detecção.
  - Executável localmente pelo agente (só usa `ast` e pytest).
  - _Requisitos: 3.3_

- [ ] 3. Criar os scripts de CI
  - `scripts/ci/radon_gate.py` (falha em CC D+ e MI abaixo de A; aviso em CC C), `scripts/ci/smoke.py`, `scripts/ci/summary.py`, sem dependências além das do extra `dev`.
  - Testes em `tests/unit/test_ci_scripts.py` para o gate do Radon.
  - _Requisitos: 4.1, 4.2, 4.3, 5.1, 5.2, 2.4_

- [ ] 4. Criar `.github/workflows/ci.yml`
  - Job `testes-e-analise`, gatilhos, permissões, concorrência, etapas condicionais e artefatos do design.
  - _Requisitos: 1.2–1.5, 2.2, 2.4, 3.2, 6.1, 6.2, 6.3, 6.5_

- [ ] 5. Primeira execução e correções
  - Abrir o PR (rascunho), ler o run com `gh run view --log` e corrigir até ficar verde.
  - Provar a falha com um commit temporário de teste quebrado; registrar o link do run vermelho e reverter.
  - _Requisitos: 1.3, 1.4, 6.5_

- [ ] 6. Preparar a CI obrigatória (#27, passo b)
  - Atualizar `.github/branch-protection-main.json` com `testes-e-analise`; comentar na #27 o comando para o administrador.
  - _Requisitos: 6.4_

- [ ] 7. Registrar métricas e documentação
  - `docs/quality-report.md` com os números do run verde e o link.
  - README: "Testes" e "Análise estática" com os comandos do design; remover os avisos "planejado, não disponível".
  - ADR 0006 aceito; índice de ADR; CHANGELOG; CONTEXT; matriz (ENG-QUAL → workflow e run); contribuições.
  - _Requisitos: 7.1–7.4_
