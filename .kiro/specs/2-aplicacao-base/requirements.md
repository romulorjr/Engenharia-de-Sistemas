# Requisitos — #2 Preparar aplicação e dependências reproduzíveis

Issue: [#2](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/2). Requisito de rastreabilidade: ENG-INFRA. Milestone: M1 – Base técnica (27/11/2026). Decisões aplicáveis: [ADR 0001](../../../docs/adr/0001-escolha-da-stack.md) (stack), [ADR 0002](../../../docs/adr/0002-persistencia-e-atomicidade.md) (SQLAlchemy + Alembic, usados a partir da #4).

Status: **rascunho para revisão**, 26/11/2026. Nenhum código foi escrito.

## Introdução
Hoje o repositório não tem aplicação nem manifesto de dependências. Esta spec cria o esqueleto instalável da API: pacote Python em camadas, fábrica da aplicação FastAPI, configuração por variáveis de ambiente e instruções de execução. Não implementa nenhuma regra RN01–RN12 nem endpoint do PDF. Banco e migrações são da #4; erros padronizados, da #18; CI, cobertura e análise estática, da #3.

## Glossário
- **Ambiente limpo:** ambiente virtual novo com Python 3.12, sem pacotes além dos instalados pelo comando documentado.
- **Fábrica da aplicação:** função `create_app` que monta e devolve a aplicação FastAPI sem efeitos colaterais na importação.
- **Configuração:** valores lidos de variáveis de ambiente na criação da aplicação.

## Requisito 1 — Projeto instalável e reproduzível
**História:** Como integrante do grupo, quero instalar o projeto com um único comando documentado, para executar e testar a API em qualquer máquina.

Critérios de aceite:
1. O projeto DEVE ter um `pyproject.toml` na raiz com o pacote `maquina_cafe` em layout `src/` e `requires-python = ">=3.12"`.
2. QUANDO um integrante executar `python -m pip install -e ".[dev]"` em ambiente limpo, O SISTEMA DEVE instalar a aplicação e as ferramentas de desenvolvimento sem passos manuais adicionais.
3. O `pyproject.toml` DEVE fixar com `==` a versão de cada dependência direta, de execução e de desenvolvimento.
4. O conjunto completo de pacotes instalados (incluindo dependências indiretas) DEVE ser registrado a cada execução da CI (#3), para que qualquer instalação possa ser comparada com a da CI.
5. O projeto NÃO DEVE declarar dependências que ainda não são usadas pelo código desta issue; SQLAlchemy e Alembic entram na #4 e PyJWT na #12.

## Requisito 2 — Inicialização da aplicação
**História:** Como integrante, quero iniciar a API localmente e ver a documentação Swagger, para acompanhar a evolução dos endpoints.

Critérios de aceite:
1. O SISTEMA DEVE oferecer a função `maquina_cafe.api.app.create_app(settings=None)` que devolve uma aplicação FastAPI.
2. QUANDO `create_app` receber uma configuração explícita, O SISTEMA DEVE usá-la sem ler variáveis de ambiente.
3. QUANDO `create_app` for chamada sem configuração, O SISTEMA DEVE ler a configuração das variáveis de ambiente.
4. A importação de `maquina_cafe.api.app` NÃO DEVE criar a aplicação nem ler variáveis de ambiente.
5. QUANDO um integrante executar `uvicorn maquina_cafe.api.app:create_app --factory`, O SISTEMA DEVE iniciar e responder 200 em `/docs` e em `/openapi.json`.
6. O OpenAPI DEVE ter título "Máquina de Café ESI" e a versão declarada no `pyproject.toml`.

## Requisito 3 — Configuração por variáveis de ambiente
**História:** Como integrante, quero configurar a aplicação por variáveis de ambiente documentadas, sem segredos no repositório.

Critérios de aceite:
1. O SISTEMA DEVE ler a variável `MAQUINA_CAFE_DATABASE_URL`, com valor padrão `sqlite:///maquina_cafe.db`. Nesta issue o valor só é guardado; a #4 o usa.
2. SE uma variável de configuração estiver definida com valor vazio, ENTÃO O SISTEMA DEVE recusar a criação da aplicação com erro que nomeia a variável.
3. O repositório DEVE conter `.env.example` com cada variável, seu significado e um valor de exemplo sem dado real.
4. O repositório NÃO DEVE conter `.env` nem banco local (já ignorados pelo `.gitignore`).

## Requisito 4 — Estrutura em camadas
**História:** Como integrante, quero as camadas do projeto criadas como pacotes Python, para que cada issue saiba onde colocar seu código.

Critérios de aceite:
1. O pacote DEVE conter os subpacotes `api`, `services`, `domain` e `persistence`, com `__init__.py` e uma docstring que descreve a responsabilidade da camada, substituindo os `.gitkeep`.
2. A configuração DEVE ficar em `maquina_cafe/config.py`, fora das camadas de negócio.
3. `domain` e `services` NÃO DEVEM importar `fastapi`; essa regra é verificada automaticamente pela #3.

## Requisito 5 — Verificação e documentação
**História:** Como integrante, quero instruções testadas e evidência automática de que a aplicação inicia, para confiar no README.

Critérios de aceite:
1. O repositório DEVE ter o teste de integração `test_app_startup` (`/openapi.json` e `/docs` respondem 200; título e versão corretos) e testes unitários da configuração.
2. QUANDO a CI da #3 rodar, ELA DEVE instalar o projeto em ambiente limpo, executar esses testes e iniciar o servidor com `uvicorn` uma vez (teste de fumaça).
3. O README DEVE trazer, em "Executar localmente" e "Testes", os comandos para Linux/macOS e Windows PowerShell, exatamente como executados na CI.
4. CHANGELOG, CONTEXT, matriz de rastreabilidade, relatório de qualidade e contribuições DEVEM ser atualizados no mesmo PR.

## Fora do escopo
Endpoints do PDF, banco, migrações, autenticação, handlers de erro, Docker, implantação.
