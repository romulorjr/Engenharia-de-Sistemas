# Tarefas — #2 Preparar aplicação e dependências reproduzíveis

Requisitos: [requirements.md](requirements.md). Design: [design.md](design.md). Status: **implementada** em 27/11/2026 no [PR #29](https://github.com/romulorjr/Engenharia-de-Sistemas/pull/29); tarefas abaixo concluídas, exceto onde indicado.

Implementação no mesmo PR da [#3](../3-ci-qualidade/tasks.md), em commits separados com `Refs #2`. Pendente fora das tarefas: execução dos comandos de Windows por um integrante (critério da #2 no plano).

- [x] 1. Criar `pyproject.toml` com metadados e dependências
  - Nome `maquina-cafe`, versão `0.1.0`, `requires-python = ">=3.12"`, backend setuptools, `packages.find` em `src`.
  - Dependências de execução: fastapi, pydantic, uvicorn, com `==` nas versões candidatas do design.
  - Extra `dev`: pytest, httpx (e as ferramentas da #3).
  - _Requisitos: 1.1, 1.2, 1.3, 1.5_

- [x] 2. Criar os pacotes das camadas
  - `__init__.py` com docstring em `api`, `services`, `domain`, `persistence`; remover os `.gitkeep` substituídos.
  - `maquina_cafe/__init__.py` com `__version__` lida de `importlib.metadata`.
  - _Requisitos: 4.1, 4.2_

- [x] 3. Implementar `config.Settings` e `InvalidSettingsError`
  - `from_env(environ)` com padrão, leitura e rejeição de valor vazio.
  - Testes `test_settings_default_database_url`, `test_settings_reads_environment`, `test_settings_rejects_empty_value` em `tests/unit/test_config.py`.
  - _Requisitos: 3.1, 3.2_

- [x] 4. Implementar `create_app`
  - Sem global `app`; título, versão e descrição; `app.state.settings`.
  - `tests/conftest.py` com fixtures `settings` e `client`.
  - Testes `test_app_startup`, `test_create_app_uses_given_settings`, `test_create_app_rejects_invalid_environment` em `tests/integration/test_app_startup.py`.
  - _Requisitos: 2.1–2.6_

- [x] 5. Criar `.env.example`
  - `MAQUINA_CAFE_DATABASE_URL` com explicação e valor de exemplo.
  - _Requisitos: 3.3, 3.4_

- [x] 6. Validar na CI e fixar versões
  - Depende da tarefa 3 da spec da #3 (workflow).
  - Ler o log com `gh run view --log`; corrigir incompatibilidades; anexar o `pip freeze` ao PR.
  - _Requisitos: 1.2, 1.4, 5.2_

- [x] 7. Atualizar a documentação
  - README: "Executar localmente" e "Testes" com os comandos do design (Linux/macOS e PowerShell); estrutura de pastas; status.
  - CHANGELOG (`[Unreleased]`), CONTEXT, `docs/rastreabilidade.md` (ENG-INFRA → arquivos e testes reais), `docs/quality-report.md` (números da CI), `docs/contributions.md`, `docs/arquitetura.md` (componentes reais: `create_app`, `Settings`).
  - _Requisitos: 5.3, 5.4_
