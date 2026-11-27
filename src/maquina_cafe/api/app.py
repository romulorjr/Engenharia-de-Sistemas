"""Fábrica da aplicação FastAPI.

Importar este módulo não cria a aplicação nem lê o ambiente. Para executar:
``uvicorn maquina_cafe.api.app:create_app --factory``.
"""

from fastapi import FastAPI

from maquina_cafe import __version__
from maquina_cafe.config import Settings

TITLE = "Máquina de Café ESI"
DESCRIPTION = (
    "API REST de uma máquina de café automática (disciplina ESI). "
    "Valores monetários em reais com duas casas decimais (ADR 0005); "
    'erros no formato {"erro", "mensagem"} (ADR 0003).'
)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Monta a aplicação.

    Usa ``settings`` quando informado; caso contrário, lê a configuração das
    variáveis de ambiente (``Settings.from_env``).
    """
    resolved = settings if settings is not None else Settings.from_env()
    app = FastAPI(title=TITLE, version=__version__, description=DESCRIPTION)
    app.state.settings = resolved
    return app
