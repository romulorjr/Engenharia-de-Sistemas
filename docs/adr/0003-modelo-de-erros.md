# ADR 0003 — Modelo de erros e mapeamento HTTP

Data: 25/11/2026. Status: **Aceito**, exceto as linhas marcadas "proposto", que aguardam confirmação.
Requisitos: ENG-API, RN01, RN02, RN05, RN08, RN09, RN11, RN12. Issues: #18, #7, #9, #11, #12, #13, #14, #15, #17. Decisões do responsável: itens 4a, 4b, 4c e 4f de 25/11/2026, registradas em [requisitos](../requisitos.md#decisões-de-interpretação-25112026).

## Contexto
O PDF sugere códigos HTTP (página 4) e mostra erros no formato `{"erro": "...", "mensagem": "..."}` (páginas 6–7). O FastAPI, por padrão, responde erros de validação com 422 e `{"detail": [...]}`, o que contradiz o 400 do PDF e o 422 reservado para reabastecimento acima da capacidade.

## Decisão
1. **Envelope único.** Toda resposta de erro é JSON `{"erro": "CODIGO", "mensagem": "texto para pessoas"}`, com `"detalhes": [...]` opcional para erros de campo. Vale também para erros do framework (rota inexistente, método não permitido, validação).
2. **Validação gera 400.** `RequestValidationError` do FastAPI/Pydantic vira 400 `DADOS_INVALIDOS`, não 422.
3. **Serviços não conhecem HTTP.** Serviços e domínio lançam exceções de domínio (por exemplo, `CreditoInsuficiente`). Um único conjunto de handlers em `api/` traduz exceção → status + `erro`.
4. **503 só para o cliente.** 503 indica que a máquina está indisponível para o cliente (MANUTENCAO ou AGUARDANDO_LIMPEZA). Operação do operador no estado errado gera 409 `ESTADO_INVALIDO` (decisão 4f).
5. **Estado atualizado antes da decisão.** Preparo vencido é concluído antes de verificar o estado (RN04), para que um pedido feito após o término não receba `MAQUINA_OCUPADA`.
6. **Ordem das verificações.** Em `POST /pedidos`: formato e açúcar (400) → bebida existe (404) → estado (409/503) → crédito (402) → estoque (409), na ordem em que RN02 lista as condições. Em `POST /credito`: formato e denominação (400) → estado (409/503) → limite de R$ 50 (400).

## Mapeamento
| Situação | Rotas | HTTP | `erro` | Fonte |
|---|---|---|---|---|
| Bebida inexistente | `POST /pedidos`, `PUT /operador/produtos/{id}/preco` | 404 | `PRODUTO_NAO_ENCONTRADO` | PDF |
| Pedido inexistente | `GET /pedidos/{id}`, `POST /pedidos/{id}/cancelar` | 404 | `PEDIDO_NAO_ENCONTRADO` | PDF, por analogia |
| Rota inexistente | qualquer | 404 | `NAO_ENCONTRADO` | envelope |
| Dados inválidos: açúcar fora de 0–3, valor fora das denominações, mais de duas casas decimais, preço ≤ 0, campo ausente ou de tipo errado, `from`/`to` ausente ou inválido | várias | 400 | `DADOS_INVALIDOS` | PDF; decisões 4c e 4e |
| Inserção que levaria o crédito acima de R$ 50,00 (rejeitada inteira) | `POST /credito` | 400 (proposto) | `LIMITE_CREDITO_EXCEDIDO` (proposto) | PDF "valor de crédito não aceito"; decisão 4b |
| Crédito insuficiente | `POST /pedidos` | 402 | `CREDITO_INSUFICIENTE` | PDF |
| Estoque ou copo insuficiente | `POST /pedidos` | 409 | `ESTOQUE_INSUFICIENTE` | PDF |
| Máquina PREPARANDO | `POST /pedidos`, `POST /credito` | 409 | `MAQUINA_OCUPADA` | PDF; decisão 4a |
| Máquina em MANUTENCAO | `POST /pedidos`, `POST /credito` | 503 | `MAQUINA_EM_MANUTENCAO` | PDF; decisões 4a e 4f |
| Máquina AGUARDANDO_LIMPEZA | `POST /pedidos`, `POST /credito` | 503 | `LIMPEZA_PENDENTE` | PDF; decisões 4a e 4f |
| Token ausente, inválido ou expirado | `/operador/*`, exceto login | 401 | `NAO_AUTORIZADO` | PDF; decisão 4d |
| Usuário ou senha incorretos | `POST /operador/login` | 401 | `CREDENCIAIS_INVALIDAS` | [ADR 0004](0004-autenticacao-operador-jwt.md) |
| Operador no estado errado: reabastecer ou limpar fora de MANUTENCAO; entrar em manutenção fora de PRONTA/AGUARDANDO_LIMPEZA; sair sem estar em MANUTENCAO | `/operador/estoque/reabastecer`, `/operador/limpeza`, `/operador/manutencao` | 409 | `ESTADO_INVALIDO` | decisão 4f |
| Reabastecimento acima da capacidade | `POST /operador/estoque/reabastecer` | 422 | `CAPACIDADE_EXCEDIDA` | PDF |
| Cancelar pedido que não está EM_PREPARO | `POST /pedidos/{id}/cancelar` | 409 (proposto) | `PEDIDO_NAO_CANCELAVEL` (proposto) | questão em aberto |

`POST /troco` não tem erro de estado: RN06 permite o troco a qualquer momento. A alteração de preço não tem restrição de estado, porque RN10 não define nenhuma.

## Consequências
- Handlers de exceção em `api/` e uma hierarquia pequena de exceções de domínio.
- `test_error_contract` (#18) verifica envelope, status e `erro` de cada linha da tabela.
- Cada rota declara suas respostas de erro no OpenAPI (`responses=` do FastAPI), com exemplo (#21).
- O README resume esta tabela; mudanças aqui exigem atualizar README e OpenAPI no mesmo PR.

## Alternativas consideradas
| Alternativa | Motivo da rejeição |
|---|---|
| Padrão do FastAPI (422 e `detail`) | Contradiz o 400 do PDF e o formato `erro`/`mensagem` dos exemplos |
| RFC 9457 (`application/problem+json`) | Acrescenta campos sem ganho para o escopo; diverge dos exemplos do PDF |
| 503 também para o operador no estado errado | Rejeitado pela decisão 4f: o operador controla o estado; 503 fica para indisponibilidade ao cliente |
| 409 para crédito em qualquer estado diferente de PRONTA | Permitido pela decisão 4a, mas a resposta diferiria de `POST /pedidos` no mesmo estado; preferida a consistência |
