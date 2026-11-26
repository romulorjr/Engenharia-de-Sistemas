# Configuração administrativa do GitHub

## Estado em 25/11/2026
| Item | Situação | Como foi feito |
|---|---|---|
| Issues #1–#24 | Criadas em 14/10/2026 | Conector |
| Milestones M1–M5 | **Criados** em 25/11/2026 (números 1–5 no GitHub) | `gh api` pelo agente |
| Vínculo issue → milestone | **Aplicado** em 25/11/2026 para #1–#21, #23, #24 e #27; #22 sem milestone | `gh api` pelo agente |
| Branch `develop` | **Arquivada** como tag `archive/develop` (ce5eca4) e removida em 25/11/2026 | `git push` pelo agente |
| Proteção de `main` | **Aguardando execução pelo administrador.** HTTP 403 em `PUT /branches/main/protection` e em `POST /rulesets`: a integração do agente não tem permissão de administração | Manual pelo responsável, [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27), passo (a) |
| CI obrigatória | Pendente: não existe workflow | Após a #3, [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) passo (b) |
| Labels do plano | Não aplicadas | `configure-github.ps1 -Apply`, a executar pelo responsável |
| Script `configure-github.ps1` | Alterado em 25/11, **não executado**: PowerShell indisponível no ambiente do agente | Responsável executa localmente e registra o resultado aqui |

Vencimentos no GitHub: M1 27/11, M2 01/12, M3 03/12, M4 06/12, M5 09/12/2026. O GitHub guarda só a data (`T00:00:00Z`); o prazo vale até o fim do dia no horário de Brasília.

## Como executar
Pré-requisitos:
- [GitHub CLI](https://cli.github.com/) instalado e autenticado (`gh auth login`) com uma conta de papel **Admin** no repositório. Conferir:
  ```bash
  gh auth status
  gh api repos/romulorjr/Engenharia-de-Sistemas --jq .permissions.admin
  ```
  A segunda linha deve imprimir `true`. Com token clássico, o escopo `repo` é necessário; com token de acesso granular, a permissão "Administration: Read and write" do repositório.
- Para o script: **PowerShell 7 ou mais recente** (`pwsh`), em Windows, Linux ou macOS. O script declara `#Requires -Version 7.0`; o Windows PowerShell 5.1 que vem com o Windows não serve. No Windows, instalar o PowerShell 7 (por exemplo, `winget install --id Microsoft.PowerShell`) e executar `pwsh`, não `powershell`.
- Diretório de trabalho: raiz de um checkout do repositório que contenha os arquivos do PR #26 (a branch `docs/governanca-documentacao-kiro`, ou `main` depois do merge).

Comandos, nesta ordem:
```powershell
# 1. Ver o plano; não altera nada e não precisa de autenticação.
pwsh -File scripts/configure-github.ps1
# 2. Criar as labels e aplicá-las às issues; preserva milestones e vínculos existentes.
pwsh -File scripts/configure-github.ps1 -Apply
```
```bash
# 3. Proteger main (#27, passo a) e conferir.
gh api -X PUT repos/romulorjr/Engenharia-de-Sistemas/branches/main/protection --input .github/branch-protection-main.json
gh api repos/romulorjr/Engenharia-de-Sistemas/branches/main/protection --jq '{admins: .enforce_admins.enabled, aprovacoes: .required_pull_request_reviews.required_approving_review_count, conversas: .required_conversation_resolution.enabled, force_push: .allow_force_pushes.enabled}'
```
O passo 3 também pode ser feito com `pwsh -File scripts/configure-github.ps1 -Apply -ProtectBranches`, que aplica as mesmas regras; o comando `gh api` é preferível porque usa o arquivo versionado. Depois de executar, registrar a data e a saída da verificação na tabela "Estado" acima e comentar na #27.

## Proteção de `main` (decisão de 25/11/2026)
Configuração versionada em [branch-protection-main.json](../.github/branch-protection-main.json):
- PR obrigatório com 1 aprovação de outro integrante; aprovações descartadas após novo push;
- conversas resolvidas antes do merge;
- regras valendo também para administradores (`enforce_admins`);
- sem force push e sem exclusão;
- `required_status_checks: null` até existir o workflow da #3.

Aplicação: passo 3 de [Como executar](#como-executar). Resultado esperado da verificação: `{"admins":true,"aprovacoes":1,"conversas":true,"force_push":false}`.

Passo (b) da #27: quando o workflow da #3 passar pela primeira vez, trocar `required_status_checks` por `{"strict": true, "contexts": ["<nome do job>"]}` e repetir o comando do passo 3. O nome do job é definido na spec da #3. Não cadastrar checks que ainda não existem: isso bloquearia todos os merges.

## Script completo (labels, milestones, proteção)
[repository-setup.json](../.github/repository-setup.json) define dez labels, os milestones M1–M5 e o vínculo de cada issue. [configure-github.ps1](../scripts/configure-github.ps1) aplica a configuração com PowerShell 7 e GitHub CLI autenticado por conta autorizada. Não colocar tokens nos arquivos.

Comandos e pré-requisitos em [Como executar](#como-executar).

O script pode ser retomado: preserva labels e milestones existentes, adiciona labels às issues sem remover outras, não troca milestone já atribuído, ignora issues sem milestone planejado e não substitui proteções existentes. Falhas interrompem a execução.

## Histórico
- 14/10/2026: issues criadas; labels, milestones (Fases 1–6) e proteção de `main`/`develop` planejados, não aplicados.
- 25/11/2026: Fases 1–6 substituídas por M1–M5; `develop` abandonada; milestones e vínculos aplicados; proteção pendente na #27.
- 26/11/2026: o responsável assumiu a execução da proteção (#27) e do script; seção "Como executar" adicionada.
