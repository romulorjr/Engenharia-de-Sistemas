# Design — #3 Configurar CI, testes e análise estática

Requisitos: [requirements.md](requirements.md). Status: **rascunho para revisão**, 26/11/2026. Estratégia de testes: [ADR 0006](../../../docs/adr/0006-estrategia-de-testes.md) (proposto).

## Visão geral
Uma única fonte de configuração (`pyproject.toml`) e um único job de CI que executa, nesta ordem: instalação, Ruff, testes com cobertura, Radon e teste de fumaça. O job publica relatórios como artefato e um resumo legível na página do run. O mesmo conjunto de comandos roda localmente.

## Configuração no `pyproject.toml`
```toml
[project.optional-dependencies]
dev = [
  "pytest==9.2.0",
  "pytest-cov==7.1.0",
  "httpx==0.29.0",
  "ruff==0.17.6",
  "radon==6.0.1",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers --strict-config"
xfail_strict = true

[tool.coverage.run]
source = ["maquina_cafe"]
branch = true

[tool.coverage.report]
show_missing = true
exclude_also = ["if TYPE_CHECKING:"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "N", "PT", "RUF"]
```
Versões candidatas conferidas nas releases do GitHub em 26/11/2026; a primeira execução da CI confirma ou ajusta.

Decisões:
- **Cobertura fora do `addopts`.** Com `--cov-fail-under` no `addopts`, rodar um único arquivo de teste localmente falharia por cobertura baixa. A CI passa `--cov` explicitamente; o README mostra o comando completo.
- **Sem `omit`.** Só `if TYPE_CHECKING:` é excluído, porque nunca executa em tempo de execução.
- **Regras do Ruff.** Erros e avisos de estilo (E, W), erros lógicos (F, B), imports ordenados (I), sintaxe moderna para 3.12 (UP), simplificações (SIM), nomes (N), estilo de pytest (PT), regras do Ruff (RUF). Ficam de fora as regras PL (Pylint), que marcariam como "número mágico" os valores do PDF nos testes, e C90, porque a complexidade é controlada pelo Radon com o limite do relatório de qualidade.
- **`line-length = 100`.** Mensagens de erro em português são longas; 100 reduz quebras artificiais.

## Teste de camadas
`tests/unit/test_architecture.py` lê cada arquivo de `src/maquina_cafe/` com `ast` e coleta os módulos importados (`import x`, `from x import y`, inclusive imports relativos convertidos em absolutos).

| Camada (pasta) | Não pode importar |
|---|---|
| `domain` | `fastapi`, `starlette`, `pydantic`, `sqlalchemy`, `alembic`, `maquina_cafe.api`, `maquina_cafe.services`, `maquina_cafe.persistence` |
| `services` | `fastapi`, `starlette`, `sqlalchemy`, `alembic`, `maquina_cafe.api` |
| `persistence` | `fastapi`, `starlette`, `maquina_cafe.api`, `maquina_cafe.services` |
| `api` | `sqlalchemy`, `alembic` |

- `api` pode importar `persistence` só para montar dependências no ponto de composição (`create_app`); consultas e SQL continuam em `persistence`.
- O teste é parametrizado por arquivo; a falha mostra arquivo, linha e módulo proibido.
- Por que um teste e não o Ruff: a regra de imports banidos do Ruff (`TID251`) é global e só pode ser desligada por arquivo, não por módulo banido; não expressa "sqlalchemy só em persistence" e "fastapi só em api" ao mesmo tempo.
- **Decisão a confirmar:** é uma proposta do agente para impor a separação de camadas pedida no PDF. Pode ser retirada sem afetar o resto.

## Workflow `.github/workflows/ci.yml`
```yaml
name: CI
on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  testes-e-analise:
    name: testes-e-analise
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: pyproject.toml
      - name: Instalar
        id: instalar
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e ".[dev]"
          python -m pip freeze | tee pip-freeze.txt
      - name: Ruff (lint)
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: ruff check --output-format=github .
      - name: Ruff (formatação)
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: ruff format --check .
      - name: Testes e cobertura
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: >-
          python -m pytest --cov=maquina_cafe --cov-branch
          --cov-report=term-missing --cov-report=xml --cov-fail-under=75
      - name: Radon
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: python scripts/ci/radon_gate.py
      - name: Fumaça (uvicorn)
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: python scripts/ci/smoke.py
      - name: Resumo
        if: ${{ !cancelled() && steps.instalar.outcome == 'success' }}
        run: python scripts/ci/summary.py >> "$GITHUB_STEP_SUMMARY"
      - uses: actions/upload-artifact@v7
        if: ${{ !cancelled() }}
        with:
          name: relatorios-qualidade
          path: |
            pip-freeze.txt
            coverage.xml
            radon-cc.txt
            radon-mi.txt
          if-no-files-found: warn
```
Decisões:
- **`pull_request` sem filtro de branch.** O PR desta issue mira a branch do PR #26 até que ele seja mesclado; com filtro `branches: [main]` a CI não rodaria nele.
- **`!cancelled() && instalar == success`.** Cada verificação roda mesmo que a anterior falhe, e o job termina vermelho se qualquer uma falhar. Se a instalação falhar, as demais não rodam, evitando erros em cascata.
- **Scripts Python em `scripts/ci/` em vez de shell.** Os mesmos comandos rodam no Windows dos integrantes:
  - `radon_gate.py`: grava `radon-cc.txt` e `radon-mi.txt`; usa a API do Radon (ou `radon cc -j`/`radon mi -j`) para falhar com classe D+ de CC ou MI abaixo de A, listando os itens.
  - `smoke.py`: inicia `uvicorn` como subprocesso em porta livre, consulta `/openapi.json` por até 15 s com `urllib`, encerra o processo e mostra a saída do servidor em caso de falha.
  - `summary.py`: escreve em Markdown o total de cobertura (`coverage report --format=total`), a média de CC e o resultado de cada etapa.
- **Ações nas versões principais atuais** (`checkout@v7`, `setup-python@v7`, `upload-artifact@v7`, conferidas em 26/11/2026).
- **Sem segredos e só leitura.** Nenhuma etapa precisa de token.

## Execução local (README)
```bash
ruff check .
ruff format --check .
python -m pytest --cov=maquina_cafe --cov-branch --cov-report=term-missing --cov-fail-under=75
python scripts/ci/radon_gate.py
python scripts/ci/smoke.py
```
`scripts/kiro/quality_check.py` (hooks) continua rodando Ruff e `pytest -q` sem cobertura, para ser rápido; o README deixa claro que a CI é a referência.

## Proteção de `main` (#27, passo b)
Depois do primeiro run verde, o PR troca em `.github/branch-protection-main.json`:
```json
"required_status_checks": { "strict": true, "contexts": ["testes-e-analise"] }
```
e comenta na #27 o comando `gh api -X PUT ...` para o administrador. O agente não consegue aplicar (HTTP 403).

## Relatório de qualidade
`docs/quality-report.md` ganha uma linha no histórico com: data, PR, número de testes unitários e de integração, cobertura de linhas e ramos, resultado do Ruff, média de CC, pior bloco, pior MI e link do run. Só números lidos do log do run.

## Testes desta issue
| Verificação | Como | Requisito |
|---|---|---|
| Suíte falha com teste quebrado | Na implementação, um commit temporário com teste falhando deixa o job vermelho; o commit é revertido antes da revisão e o link do run fica no PR | 1.3 |
| Falha com cobertura baixa | Conferido pelo `--cov-fail-under=75` no log; não forçado artificialmente | 2.2 |
| Teste de camadas | `test_architecture` parametrizado; um caso com código de exemplo em memória prova que detecta `import fastapi` em `domain` | 3.3 |
| Gate do Radon | Testes unitários de `radon_gate.py` com código de exemplo de alta complexidade | 4.2, 4.3 |
| Fumaça | Etapa da CI; falha mostra a saída do uvicorn | 5.1, 5.2 |

Os scripts em `scripts/ci/` ficam fora de `maquina_cafe` e não entram na cobertura da aplicação; seus testes ficam em `tests/unit/test_ci_scripts.py`.

## Riscos
| Risco | Mitigação |
|---|---|
| Versão candidata incompatível | Ajustar após o primeiro run e registrar no PR |
| Radon sem suporte a alguma sintaxe recente | O gate usa a API do Radon; se falhar, avaliar `ruff` C901 e registrar a troca em ADR |
| Cobertura alta mas testes fracos | ADR 0006 exige critérios de caixa-preta e testes por linha da tabela de erros |
| Hooks do Kiro inativos | A CI é a verificação que vale (CONTEXT, Bloqueios) |

## Questões para o responsável
1. Aprovar o teste de camadas (`test_architecture.py`) ou retirá-lo.
2. Aprovar os limites do Radon (falhar em CC classe D+ e MI abaixo de A), iguais às metas de `docs/quality-report.md`.
3. Aprovar o ADR 0006.
