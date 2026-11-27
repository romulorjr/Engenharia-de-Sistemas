"""Camada de persistência.

Modelos SQLAlchemy, repositories e migrações Alembic (ADR 0002). Única camada
que importa ``sqlalchemy`` e ``alembic``. Repositories recebem a sessão da
unidade de trabalho e nunca fazem commit.
"""
