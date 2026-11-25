# ADR 0005 — Representação monetária

Data: 25/11/2026. Status: **Aceito** (decisão 4e do responsável).
Requisitos: RN01, RN03, RN05, RN06, RN10, RN12, ENG-API. Issues: #18, #7, #9, #16, #17, #21.

## Contexto
Os exemplos do PDF usam reais com duas casas em números JSON (`{"valor": 10.00}`, `"preco": 6.50`). Aritmética em ponto flutuante binário produz erros de arredondamento (0,1 + 0,2 ≠ 0,3), inaceitáveis para crédito, troco e faturamento.

## Decisão
- **Internamente, centavos inteiros** em domínio, serviços e persistência (colunas INTEGER). Nenhuma operação monetária usa `float`.
- **No JSON, reais como número.**
  - Entrada: até duas casas decimais (`10`, `10.5` e `10.50` são aceitos; `10.505` → 400 `DADOS_INVALIDOS`).
  - Saída: sempre exatamente duas casas (`4.50`, `0.00`).
- **Conversão só na fronteira da API** (schemas em `api/`): o valor é lido como `Decimal` sem passar por aritmética de ponto flutuante, verificado quanto às casas decimais e multiplicado por 100. Na saída, centavos viram `Decimal` quantizado em `0.01`.
- O codificador JSON padrão do Python e do FastAPI transforma `Decimal("4.50")` em `4.5`. A API usa uma classe de resposta JSON própria que escreve o número com duas casas. Os testes verificam o texto bruto do corpo (por exemplo, `"preco": 6.50`).
- **OpenAPI:** campos monetários com `type: number`, `multipleOf: 0.01`, descrição "Valor em reais com duas casas decimais" e exemplo. `POST /credito` documenta os valores aceitos: 0.50, 1.00, 2.00, 5.00, 10.00 e 20.00.
- Nomes de campos seguem os exemplos do PDF: `valor`, `credito`, `preco`, `creditoRestante`, `valorDevolvido`.

## Consequências
- Um único ponto de conversão, coberto por testes de limite: 0.5, 10.50, 10.505, 49.99, 50.00, valores negativos e zero.
- Clientes que comparam texto veem sempre duas casas; clientes que leem números recebem o mesmo valor.
- O relatório (RN12) soma centavos e só converte na resposta.

## Alternativas consideradas
| Alternativa | Benefícios | Motivo da rejeição |
|---|---|---|
| Centavos inteiros também no JSON | Sem ambiguidade nem conversão | Rejeitada pela decisão 4e; diverge dos exemplos do PDF |
| String `"4.50"` | Texto exato sem codificador próprio | Exemplos do PDF usam números; clientes teriam de converter |
| `float` internamente | Nenhuma conversão | Erros de arredondamento binário |

## Referências
- [Python: `decimal`](https://docs.python.org/3.12/library/decimal.html)
- [OpenAPI 3.1: Schema Object](https://spec.openapis.org/oas/v3.1.0#schema-object)
