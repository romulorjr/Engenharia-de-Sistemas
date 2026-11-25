# ADR 0004 — Autenticação do operador por JWT

Data: 25/11/2026. Status: **Aceito** (decisão 4d do responsável).
Requisitos: RN11. Issues: #12, #6, #13, #14, #15, #16, #17.

## Contexto
RN11: as operações do operador exigem autenticação por token; usuário e senha fixos em variável de ambiente bastam. O exemplo 8 do PDF responde 401 `NAO_AUTORIZADO` sem token.

## Decisão
- **Credenciais** em variáveis de ambiente: `OPERADOR_USUARIO`, `OPERADOR_SENHA`. **Segredo** de assinatura em `JWT_SECRET` (mínimo de 32 bytes aleatórios). Nenhum valor real no repositório; `.env.example` terá apenas marcadores e `.env` já é ignorado pelo Git.
- Sem essas variáveis, a aplicação não inicia e informa qual falta. Não há credencial padrão no código.
- `POST /operador/login` recebe `{"usuario": "...", "senha": "..."}`. A comparação usa `hmac.compare_digest`. Sucesso: 200 `{"token": "<jwt>", "tipo": "Bearer", "expiraEm": "<ISO 8601>"}`. Falha: 401 `CREDENCIAIS_INVALIDAS`.
- **Token** JWT HS256 com `sub` (usuário), `iat` e `exp = iat + 3600 s` (1 hora). Sem refresh token: após expirar, o operador faz login de novo.
- Rotas `/operador/*` (exceto login) exigem `Authorization: Bearer <token>`. Token ausente, malformado, com assinatura inválida, com algoritmo diferente de HS256 ou expirado → 401 `NAO_AUTORIZADO`, com cabeçalho `WWW-Authenticate: Bearer`.
- **Biblioteca:** PyJWT. A decodificação fixa `algorithms=["HS256"]` e exige a claim `exp`. A dependência é acrescentada à stack do ADR 0001 na #12.
- No FastAPI, usar `HTTPBearer(auto_error=False)` para o Swagger exibir o botão "Authorize"; a ausência de token é tratada pela aplicação e gera 401 no envelope do [ADR 0003](0003-modelo-de-erros.md).
- Relógio injetável: os testes de expiração geram tokens com `exp` no passado ou avançam o relógio, sem esperar uma hora.
- Senha, segredo e token nunca aparecem em logs ou mensagens de erro.

## Consequências
- Sem estado no servidor: o token sobrevive a reinicializações e não precisa de tabela.
- Não há logout nem revogação; um token vazado vale até expirar (no máximo 1 hora). Trocar `JWT_SECRET` invalida todos os tokens.
- Testes (#12): login correto e incorreto; rota protegida sem token, com token adulterado, com algoritmo `none`, expirado e válido.

## Alternativas consideradas
| Alternativa | Benefícios | Motivo da rejeição |
|---|---|---|
| Token opaco aleatório guardado em memória ou banco | Revogável | Exige armazenamento; em memória se perde ao reiniciar |
| HTTP Basic em cada requisição | Mais simples | RN11 pede token |
| Fluxo OAuth2 password do FastAPI (`OAuth2PasswordBearer`) | Integração pronta com Swagger | Login por formulário, diferente do corpo JSON usado no restante da API |

## Referências
- [PyJWT](https://pyjwt.readthedocs.io/en/stable/)
- [FastAPI: segurança com JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [RFC 7519 (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
