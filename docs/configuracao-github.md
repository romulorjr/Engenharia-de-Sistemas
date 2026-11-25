# Configuração administrativa do GitHub

## Estado em 25/11/2026
| Item | Situação | Como foi feito |
|---|---|---|
| Issues #1–#24 | Criadas em 14/10/2026 | Conector |
| Milestones M1–M5 | **Criados** em 25/11/2026 (números 1–5 no GitHub) | `gh api` pelo agente |
| Vínculo issue → milestone | **Aplicado** em 25/11/2026 para #1–#21, #23, #24 e #27; #22 sem milestone | `gh api` pelo agente |
| Branch `develop` | **Arquivada** como tag `archive/develop` (ce5eca4) e removida em 25/11/2026 | `git push` pelo agente |
| Proteção de `main` | **Pendente.** HTTP 403 em `PUT /branches/main/protection` e em `POST /rulesets`: a integração do agente não tem permissão de administração | Manual, [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) |
| CI obrigatória | Pendente: não existe workflow | Após a #3 (passo 2 da #27) |
| Labels do plano | Não aplicadas; não solicitadas na decisão de 25/11 | Script opcional abaixo |

Vencimentos no GitHub: M1 27/11, M2 01/12, M3 03/12, M4 06/12, M5 09/12/2026. O GitHub guarda só a data (`T00:00:00Z`); o prazo vale até o fim do dia no horário de Brasília.

## Proteção de `main` (decisão de 25/11/2026)
Configuração versionada em [branch-protection-main.json](../.github/branch-protection-main.json):
- PR obrigatório com 1 aprovação de outro integrante; aprovações descartadas após novo push;
- conversas resolvidas antes do merge;
- regras valendo também para administradores (`enforce_admins`);
- sem force push e sem exclusão;
- `required_status_checks: null` até existir o workflow da #3.

Aplicar com uma conta administradora e GitHub CLI autenticado, na raiz do repositório:

```bash
gh api -X PUT repos/romulorjr/Engenharia-de-Sistemas/branches/main/protection --input .github/branch-protection-main.json
gh api repos/romulorjr/Engenharia-de-Sistemas/branches/main/protection --jq '{admins: .enforce_admins.enabled, aprovacoes: .required_pull_request_reviews.required_approving_review_count, conversas: .required_conversation_resolution.enabled, force_push: .allow_force_pushes.enabled}'
```

Resultado esperado: `{"admins":true,"aprovacoes":1,"conversas":true,"force_push":false}`.

Quando o workflow da #3 passar, trocar `required_status_checks` por `{"strict": true, "contexts": ["<nome do job>"]}` e repetir o comando. Não cadastrar checks que ainda não existem: isso bloquearia todos os merges.

## Script completo (labels, milestones, proteção)
[repository-setup.json](../.github/repository-setup.json) define dez labels, os milestones M1–M5 e o vínculo de cada issue. [configure-github.ps1](../scripts/configure-github.ps1) aplica a configuração com PowerShell 7 e GitHub CLI autenticado por conta autorizada. Não colocar tokens nos arquivos.

```powershell
# Apenas mostra o plano; não precisa de autenticação.
pwsh -File scripts/configure-github.ps1
# Aplicar labels e milestones (preserva milestones já criados e vínculos existentes).
pwsh -File scripts/configure-github.ps1 -Apply
# Aplicar também proteção de main.
pwsh -File scripts/configure-github.ps1 -Apply -ProtectBranches
```

O script pode ser retomado: preserva labels e milestones existentes, adiciona labels às issues sem remover outras, não troca milestone já atribuído, ignora issues sem milestone planejado e não substitui proteções existentes. Falhas interrompem a execução.

## Histórico
- 14/10/2026: issues criadas; labels, milestones (Fases 1–6) e proteção de `main`/`develop` planejados, não aplicados.
- 25/11/2026: Fases 1–6 substituídas por M1–M5; `develop` abandonada; milestones e vínculos aplicados; proteção pendente na #27.
