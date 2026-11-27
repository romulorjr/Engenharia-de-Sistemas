# Design — #2 Preparar aplicação e dependências reproduzíveis

Requisitos: [requirements.md](requirements.md). Status: **aprovado** em 27/11/2026 (rascunho de 26/11).

## Visão geral
Esqueleto mínimo que já respeita as camadas do steering: um pacote `maquina_cafe` instalável, uma fábrica `create_app` que é o ponto de composição da aplicação e uma configuração imutável lida do ambiente. Nada de regra de negócio.

## Restrição do ambiente do agente
O ambiente Kiro Web do agente não acessa o PyPI. O agente não consegue instalar FastAPI nem executar os testes desta issue localmente. Por isso:
- a verificação de instalação, testes e inicialização acontece na CI da #3, que o agente lê com `gh run view --log`;
- #2 e #3 são implementadas no mesmo PR, em commits separados, para que #2 não seja mesclada sem verificação;
- integrantes com internet podem reproduzir os mesmos comandos localmente.

Esta restrição não muda a stack (ADR 0002).

## Arquivos
```text
pyproject.toml                         metadados, dependências fixadas, config de ferramentas (#3)
.env.example                           variáveis documentadas
src/maquina_cafe/__init__.py           __version__ lida dos metadados do pacote
src/maquina_cafe/config.py             Settings, InvalidSettingsError
src/maquina_cafe/api/__init__.py       docstring da camada
src/maquina_cafe/api/app.py            create_app
src/maquina_cafe/services/__init__.py  docstring da camada
src/maquina_cafe/domain/__init__.py    docstring da camada
src/maquina_cafe/persistence/__init__.py docstring da camada
tests/conftest.py                      fixtures comuns (settings de teste, client)
tests/unit/test_config.py
tests/integration/test_app_startup.py
```
Os arquivos `.gitkeep` de `src/` e `tests/` são removidos quando a pasta recebe arquivos.

## Componentes

### `config.Settings`
```python
@dataclass(frozen=True)
class Settings:
    database_url: str = "sqlite:///maquina_cafe.db"

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Settings": ...

class InvalidSettingsError(ValueError): ...
```
- `from_env` recebe o mapeamento por parâmetro (padrão `os.environ`), o que permite testar sem alterar o ambiente do processo.
- Variável ausente usa o padrão; definida e vazia (ou só espaços) lança `InvalidSettingsError("MAQUINA_CAFE_DATABASE_URL não pode ser vazia.")`.
- Nome em inglês pela convenção de 27/11 (configuração é termo técnico) e pela regra N818 do Ruff (exceções terminam em `Error`). O rascunho usava `ConfiguracaoInvalida`.
- Sem `pydantic-settings`: um `dataclass` resolve com uma variável e não acrescenta dependência. Reavaliar se a #12 tornar a validação extensa.
- Sem leitura de arquivo `.env` pela aplicação. O README mostra como exportar as variáveis no shell (Linux/macOS e PowerShell).

### `api.app.create_app`
```python
def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings.from_env()
    app = FastAPI(title="Máquina de Café ESI", version=__version__, description=...)
    app.state.settings = settings
    return app
```
- Ponto de composição: as próximas issues registram routers, handlers de erro (#18) e a fábrica da unidade de trabalho (#4) aqui.
- Sem variável global `app`: importar o módulo não lê o ambiente. O uvicorn usa `--factory`.
- `__version__` vem de `importlib.metadata.version("maquina-cafe")`, com uma só fonte de versão no `pyproject.toml`.

### Docstrings das camadas
Cada `__init__.py` explica a responsabilidade e as importações permitidas, conforme o steering:
- `api`: controllers HTTP; validação de formato; tradução de exceções para HTTP.
- `services`: regras RN01–RN12 e fronteiras de transação (ADR 0002).
- `domain`: entidades, receitas, estados e valores, sem framework.
- `persistence`: modelos SQLAlchemy, repositories, migrações.

## Dependências
Versões candidatas, conferidas nas releases do GitHub em 26/11/2026. As versões finais são as que passarem na primeira execução da CI; o `pip freeze` dessa execução é anexado ao PR.

| Pacote | Uso | Grupo | Versão candidata |
|---|---|---|---|
| fastapi | framework web | execução | 0.165.0 |
| pydantic | schemas da API (importado diretamente) | execução | 2.14.4 |
| uvicorn | servidor ASGI | execução | 0.54.0 |
| pytest | testes | dev | 9.2.0 |
| httpx | `TestClient` do FastAPI | dev | 0.29.0 (publicada em 26/11; se a CI falhar com ela, fixar a última 0.28.x) |
| pytest-cov, ruff, radon | cobertura e análise estática | dev | definidos na spec da #3 |
| setuptools | backend de build | build | `>=84` |

Por que `==` só nas diretas: atende ao critério "versões fixadas" do plano sem obrigar o grupo a uma ferramenta de lock. O `pip freeze` publicado pela CI registra as indiretas. Se a CI e uma máquina local divergirem por causa de uma indireta, adotar um arquivo de restrições gerado a partir desse `pip freeze` (decisão a registrar, se necessária).

## Comandos documentados
Linux/macOS:
```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
uvicorn maquina_cafe.api.app:create_app --factory --reload
```
Windows PowerShell:
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
uvicorn maquina_cafe.api.app:create_app --factory --reload
```
Swagger em `http://127.0.0.1:8000/docs`.

## Convenção de nomes
Aprovada em 27/11/2026 e registrada no [steering](../../steering/project.md#nomenclatura-naming) e no CONTEXT: nomes do domínio em português (bebida, pedido, credito, estoque, estado, receita, reservatorio); termos técnicos, arquivos e módulos, testes e mensagens de commit em inglês.

## Testes
| Teste | Tipo | Verifica | Requisito |
|---|---|---|---|
| `test_settings_default_database_url` | unitário | padrão `sqlite:///maquina_cafe.db` com ambiente vazio | 3.1 |
| `test_settings_reads_environment` | unitário | valor de `MAQUINA_CAFE_DATABASE_URL` é usado | 3.1 |
| `test_settings_rejects_empty_value` | unitário | vazio e só espaços → `InvalidSettingsError` com o nome da variável | 3.2 |
| `test_app_startup` | integração | `/openapi.json` 200, título, versão igual a `__version__`; `/docs` 200 | 2.5, 2.6 |
| `test_create_app_uses_given_settings` | integração | `app.state.settings` é a configuração passada, mesmo com o ambiente diferente | 2.2 |
| `test_create_app_rejects_invalid_environment` | integração | sem parâmetro e com variável vazia, `create_app` lança `InvalidSettingsError` | 2.3, 3.2 |
| Teste de fumaça na CI | sistema | `uvicorn --factory` sobe e `/openapi.json` responde 200 | 2.5, 5.2 |

Cobertura esperada do código desta issue: 100% de linhas e ramos (código pequeno, todos os caminhos testados).

## Riscos
| Risco | Mitigação |
|---|---|
| Versões candidatas incompatíveis entre si | Primeira execução da CI decide; ajustar e registrar no PR |
| Diferenças no Windows (ativação do venv, `py` launcher) | Comandos PowerShell no README; pedir a um integrante com Windows que os execute na revisão |
| `--reload` em pastas grandes | Só para desenvolvimento; a CI usa sem `--reload` |

## Respostas do responsável (27/11/2026)
1. Convenção de nomes: aprovada.
2. `==` só nas dependências diretas: aprovado; Python 3.12 fixo na CI; lock completo com hashes fora do escopo, a reavaliar só se houver divergência de ambiente (ADR 0006).
