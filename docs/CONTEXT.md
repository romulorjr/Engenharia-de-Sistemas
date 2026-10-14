# Contexto do projeto

Atualizado em 14/10/2026. Projeto ESI – Engenharia de Sistemas de Informação.

Fonte normativa: [ESI - projeto maquina-cafe.pdf](../ESI%20-%20projeto%20maquina-cafe.pdf). O PDF é preservado. Este documento registra decisões e não substitui a especificação.

## Escopo confirmado
Back-end de uma máquina de café, preferencialmente API REST; sem interface gráfica ou hardware. Cinco bebidas, seis reservatórios, crédito, pedidos, quatro estados, operador e relatórios. RN01–RN12, banco persistente, testes unitários e integração, cobertura mínima de 75%, análise estática, documentação e sete artefatos finais.

## Equipe (ordem alfabética)
- Bruno de Andrade Gama Kraker
- Pedro Henryk Bezerra Souza
- Rodrigo Franco de Moraes
- Rômulo Maurício Fonseca Júnior
- Thales Iamamura

Papéis, responsáveis por issues e usuários GitHub: a definir pelo grupo. Não inferir autoria nem atribuir contribuições antecipadamente.

## Decisões e datas
Não há preferência ou restrição tecnológica, conforme confirmação do responsável. Stack de referência escolhida para o MVP: Python, FastAPI, SQLAlchemy e SQLite; ver [ADR 0001](adr/0001-escolha-da-stack.md). Ainda não implementada.
Checkpoint: 18/11/2026. Entrega final: 09/12/2026. Ano confirmado pelo responsável. Fuso do planejamento: America/Sao_Paulo.

## Estado inicial
Repositório público com README de uma linha e especificação PDF; dois commits; apenas main, sem proteção. Sem aplicação, testes ou licença. Esta mudança cria planejamento, estrutura e governança. Não declara funcionalidades entregues ou cobertura medida.

## Trabalho contínuo
Ler este arquivo e [plano](plano-de-projeto.md) antes de mudanças. Usar Conventional Commits e rastreabilidade requisito → issue → teste. Alterações funcionais devem atualizar testes e documentação. Não modificar referências sincronizadas sob sources/ no ambiente do projeto.

## Pendências
Licença, papéis e usuários GitHub. Resolver as ambiguidades de domínio registradas em requisitos.md antes da implementação correspondente. Configuração administrativa do GitHub depende de ferramenta com acesso apropriado.
