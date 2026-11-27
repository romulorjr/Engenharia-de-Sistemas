# Requisitos — #3 Configurar CI, testes e análise estática

Issue: [#3](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/3). Requisito de rastreabilidade: ENG-QUAL. Milestone: M1 – Base técnica (27/11/2026). Relacionadas: [#2](../2-aplicacao-base/requirements.md) (aplicação base), [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) passo (b) (CI obrigatória na proteção de `main`), #20 (relatório final de qualidade).

Status: **aprovada** pelo responsável em 27/11/2026, com o refinamento 4.4–4.5 (aviso de classe C). Rascunho de 26/11/2026.

## Introdução
O PDF exige testes automatizados unitários e de integração com cobertura mínima de 75%, critérios de teste funcional ou caixa-preta e análise estática com relatório de métricas. Esta spec configura as ferramentas no `pyproject.toml`, cria o workflow do GitHub Actions e define como os resultados viram evidência no relatório de qualidade. A estratégia de testes do projeto é proposta no [ADR 0006](../../../docs/adr/0006-estrategia-de-testes.md).

## Glossário
- **CI:** workflow do GitHub Actions em `.github/workflows/ci.yml`.
- **Check obrigatório:** job da CI exigido pela proteção de `main` antes do merge.
- **Cobertura:** linhas e ramos do pacote `maquina_cafe` executados pela suíte, medidos pelo coverage.py via pytest-cov.

## Requisito 1 — Suíte de testes
**História:** Como integrante, quero executar toda a suíte com um comando, localmente e na CI, para saber se uma mudança quebrou algo.

Critérios de aceite:
1. O SISTEMA DEVE configurar o pytest no `pyproject.toml` com `testpaths = ["tests"]`, marcadores estritos e configuração estrita.
2. QUANDO um PR for aberto ou atualizado, ou houver push em `main`, A CI DEVE executar a suíte completa em Python 3.12 em ambiente limpo.
3. SE algum teste falhar, ENTÃO o job DEVE falhar.
4. SE nenhum teste for coletado, ENTÃO o job DEVE falhar (código de saída 5 do pytest não é ignorado).
5. A CI DEVE poder ser disparada manualmente (`workflow_dispatch`).

## Requisito 2 — Cobertura mínima
**História:** Como grupo, queremos a cobertura medida e imposta pela CI, para cumprir os 75% do PDF com números reais.

Critérios de aceite:
1. A CI DEVE medir cobertura de linhas e ramos de `maquina_cafe`.
2. SE a cobertura total ficar abaixo de 75%, ENTÃO o job DEVE falhar.
3. A configuração NÃO DEVE omitir módulos da aplicação da medição.
4. A CI DEVE publicar o relatório (`coverage.xml`) como artefato e escrever o percentual total no resumo do job.

## Requisito 3 — Lint, formatação e camadas
**História:** Como revisor, quero que estilo e erros comuns sejam verificados automaticamente, para focar a revisão no comportamento.

Critérios de aceite:
1. A CI DEVE executar `ruff check .` e `ruff format --check .` com a configuração do `pyproject.toml`, em Python 3.12 fixo.
2. SE houver erro de lint ou arquivo fora da formatação, ENTÃO o job DEVE falhar, com anotações nos arquivos do PR.
3. O SISTEMA DEVE ter um teste automático que falha se uma camada importar o que o steering proíbe: `fastapi`/`starlette` fora de `api`; `sqlalchemy`/`alembic` fora de `persistence`; `domain` importando outras camadas; `services` importando `api`.

## Requisito 4 — Métricas de complexidade
**História:** Como grupo, queremos métricas de complexidade e manutenibilidade a cada PR, para o relatório de qualidade e para detectar código difícil de manter.

Critérios de aceite:
1. A CI DEVE gerar os relatórios `radon cc src -s -a` e `radon mi src -s` e publicá-los como artefato.
2. SE algum bloco tiver complexidade ciclomática de classe D ou pior (CC > 20), ENTÃO o job DEVE falhar e listar os blocos.
3. SE algum módulo tiver índice de manutenibilidade abaixo da classe A (MI < 20), ENTÃO o job DEVE falhar e listar os módulos.
4. QUANDO algum bloco tiver complexidade de classe C (CC 11–20), A CI DEVE emitir um aviso com o bloco e a linha, sem falhar o job.
5. SE a CI falhar só por esses limites, ENTÃO os blocos e módulos apontados DEVEM ser listados e corrigidos; os limites NÃO DEVEM ser reduzidos para a CI passar.

## Requisito 5 — Teste de fumaça da inicialização
**História:** Como grupo, queremos provar a cada PR que a API inicia em ambiente limpo (#2).

Critérios de aceite:
1. A CI DEVE iniciar `uvicorn maquina_cafe.api.app:create_app --factory` e exigir resposta 200 em `/openapi.json` em até 15 segundos.
2. SE o servidor não responder no prazo, ENTÃO o job DEVE falhar e mostrar a saída do servidor.

## Requisito 6 — Check obrigatório e segurança do workflow
**História:** Como responsável, quero um nome de check estável e um workflow com permissões mínimas, para exigi-lo na proteção de `main`.

Critérios de aceite:
1. O job DEVE se chamar `testes-e-analise`, nome que será cadastrado na proteção (#27, passo b).
2. O workflow DEVE ter permissão apenas de leitura do conteúdo (`contents: read`) e não usar segredos.
3. QUANDO um novo push chegar à mesma branch, A CI DEVE cancelar a execução anterior ainda em andamento.
4. QUANDO a CI passar pela primeira vez, o PR DEVE atualizar `.github/branch-protection-main.json` com o check e comentar na #27 o comando para o administrador.
5. Todas as verificações (lint, formatação, testes, métricas, fumaça) DEVEM rodar mesmo que uma anterior falhe, desde que a instalação tenha funcionado, para que um único run mostre todos os problemas.

## Requisito 7 — Execução local e documentação
**História:** Como integrante, quero rodar localmente as mesmas verificações da CI.

Critérios de aceite:
1. O README DEVE listar, em "Testes" e "Análise estática", os mesmos comandos usados na CI.
2. `docs/quality-report.md` DEVE registrar os números da primeira execução verde (testes, cobertura, Ruff, Radon), com link para o run.
3. O ADR 0006 (estratégia de testes) DEVE ser aceito no mesmo PR.
4. CHANGELOG, CONTEXT, matriz de rastreabilidade e contribuições DEVEM ser atualizados no mesmo PR.

## Fora do escopo
Matriz de várias versões do Python, testes de mutação, publicação de pacote, implantação, Postman (#21).
