"""Camada de API (controllers HTTP).

Recebe as requisições, valida o formato da entrada, chama os serviços e produz
as respostas HTTP. Traduz exceções de domínio em códigos HTTP (ADR 0003).
Não contém regra de negócio nem SQL. ``app.create_app`` é o ponto de composição
onde routers, handlers de erro e dependências são registrados.
"""
