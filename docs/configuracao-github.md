# Configuração administrativa do GitHub

## Estado atual
Atualizado em 27/11/2026.

| Item | Situação | Como foi feito |
|---|---|---|
| Issues #1–#24 | Criadas em 14/10/2026 | Conector |
| Milestones M1–M5 | **Criados** em 25/11/2026 (números 1–5 no GitHub) | `gh api` pelo agente |
| Vínculo issue → milestone | **Aplicado** em 25/11/2026 para #1–#21, #23, #24 e #27; #22 sem milestone | `gh api` pelo agente |
| Branch `develop` | **Arquivada** como tag `archive/develop` (ce5eca4) e removida em 25/11/2026 | `git push` pelo agente |
| Ruleset "Proteção da Main" (id 28239929) | **Criado pelo responsável em 27/11/2026, mas sem efeito:** a condição `include` está vazia, então não se aplica a nenhuma branch (`GET /rules/branches/main` retorna vazio). Regras atuais: só bloquear exclusão e force push. Bypass "always" para a integração 2331586 | Responsável, pela interface do GitHub |
| Proteção de `main` com PR obrigatório e CI obrigatória | **Aguardando execução pelo administrador.** O agente recebeu HTTP 403 em 27/11 ao atualizar o ruleset (`PUT /rulesets/28239929`) e ao criar proteção clássica (`PUT /branches/main/protection`), mesmo com o bypass: bypass deixa passar pelas regras, mas não dá permissão para editá-las | Responsável, passo 3 de [Como executar](#como-executar); [#27](https://github.com/romulorjr/Engenharia-de-Sistemas/issues/27) |
| Check de CI `testes-e-analise` | **Existe** desde 27/11/2026 (run verde [46014939322](https://github.com/romulorjr/Engenharia-de-Sistemas/actions/runs/46014939322)); publicado pelo app GitHub Actions (id 15368) | Workflow `.github/workflows/ci.yml` (#3) |
| Labels do plano | Não aplicadas | `configure-github.ps1 -Apply`, a executar pelo responsável |
| Script `configure-github.ps1` | Alterado em 25/11, **não executado**: PowerShell indisponível no ambiente do agente | Responsável executa localmente e registra o resultado aqui |

Vencimentos no GitHub: M1 27/11, M2 01/12, M3 03/12, M4 06/12, M5 09/12/2026. O GitHub guarda só a data (`T00:00:00Z`); o prazo vale até o fim do dia no horário de Brasília.

## Proteção de `main`
Decisões de 25/11/2026 (regras) e 27/11/2026 (ruleset e check obrigatório).

Arquivo recomendado: [ruleset-main.json](../.github/ruleset-main.json), para atualizar o ruleset que o responsável já criou:
- aplica-se à branch padrão (`~DEFAULT_BRANCH`, hoje `main`);
- bloqueia exclusão e force push;
- exige PR com 1 aprovação; aprovações descartadas após novo push; conversas resolvidas;
- exige o check `testes-e-analise` do app GitHub Actions (`integration_id` 15368), com a branch atualizada em relação a `main`. Fixar o app impede que um status com o mesmo nome, enviado por outra origem, satisfaça a regra;
- **sem bypass.** Rulesets valem também para administradores, o equivalente ao `enforce_admins` decidido em 25/11. O agente não precisa de bypass: ele trabalha por PR. Com o bypass "always" atual, pushes e merges da integração 2331586 ignorariam as regras, o que contraria a decisão "sem push direto em `main`". Se o responsável preferir manter um bypass, usar o modo "pull_request" (só permite contornar dentro de um PR).

Alternativa equivalente com proteção clássica: [branch-protection-main.json](../.github/branch-protection-main.json). Usar uma das duas; com as duas ativas as regras se somam e ficam mais difíceis de manter.

Efeito esperado: nenhum push direto em `main`, nem do administrador; todo merge precisa de aprovação de outro integrante e do check `testes-e-analise` verde. O único PR aberto em 27/11 que mira `main` (#29) contém o workflow, então já recebe o check. PRs abertos a partir de `main` antes do merge da #29 não terão o workflow e só receberão o check depois de atualizados com `main`.

## Como executar
Pré-requisitos:
- [GitHub CLI](https://cli.github.com/) instalado e autenticado (`gh auth login`) com uma conta de papel **Admin** no repositório. Conferir:
  ```bash
  gh auth status
  gh api repos/romulorjr/Engenharia-de-Sistemas --jq .permissions.admin
  ```
  A segunda linha deve imprimir `true`. Com token clássico, o escopo `repo` é necessário; com token de acesso granular, a permissão "Administration: Read and write" do repositório.
- Para o script: **PowerShell 7 ou mais recente** (`pwsh`), em Windows, Linux ou macOS. O script declara `#Requires -Version 7.0`; o Windows PowerShell 5.1 que vem com o Windows não serve. No Windows, instalar o PowerShell 7 (por exemplo, `winget install --id Microsoft.PowerShell`) e executar `pwsh`, não `powershell`.
- Diretório de trabalho: raiz de um checkout que contenha `.github/ruleset-main.json` (branch `feature/2-3-app-base-ci` ou `main` depois do merge do PR #29).

Comandos, nesta ordem:
```powershell
# 1. Ver o plano; não altera nada e não precisa de autenticação.
pwsh -File scripts/configure-github.ps1
# 2. Criar as labels e aplicá-las às issues; preserva milestones e vínculos existentes.
#    Não usar -ProtectBranches: ele cria proteção clássica, e a proteção fica no ruleset (passo 3).
pwsh -File scripts/configure-github.ps1 -Apply
```
```bash
# 3. Atualizar o ruleset existente (#27, passos a e b juntos) e conferir.
gh api -X PUT repos/romulorjr/Engenharia-de-Sistemas/rulesets/28239929 --input .github/ruleset-main.json
gh api repos/romulorjr/Engenharia-de-Sistemas/rules/branches/main --jq '[.[].type]'
```
Resultado esperado da verificação: `["deletion","non_fast_forward","pull_request","required_status_checks"]`.

Pela interface, o mesmo resultado: Settings → Rules → Rulesets → "Proteção da Main" → Target branches: "Include default branch" → Bypass list: remover a integração (ou trocar para "For pull requests only") → marcar "Require a pull request before merging" (1 aprovação, "Dismiss stale pull request approvals when new commits are pushed", "Require conversation resolution before merging") e "Require status checks to pass" (adicionar `testes-e-analise`, origem GitHub Actions, e "Require branches to be up to date before merging") → manter "Restrict deletions" e "Block force pushes" → Save.

Depois de executar, registrar a data e a saída da verificação na tabela "Estado atual" acima e comentar na #27.

## Script completo (labels, milestones, proteção)
[repository-setup.json](../.github/repository-setup.json) define dez labels, os milestones M1–M5 e o vínculo de cada issue. [configure-github.ps1](../scripts/configure-github.ps1) aplica a configuração com PowerShell 7 e GitHub CLI autenticado por conta autorizada. Não colocar tokens nos arquivos.

O script pode ser retomado: preserva labels e milestones existentes, adiciona labels às issues sem remover outras, não troca milestone já atribuído, ignora issues sem milestone planejado e não substitui proteções existentes. Falhas interrompem a execução.

## Histórico
- 14/10/2026: issues criadas; labels, milestones (Fases 1–6) e proteção de `main`/`develop` planejados, não aplicados.
- 25/11/2026: Fases 1–6 substituídas por M1–M5; `develop` abandonada; milestones e vínculos aplicados; proteção pendente na #27.
- 26/11/2026: o responsável assumiu a execução da proteção (#27) e do script; seção "Como executar" adicionada.
- 27/11/2026: o responsável criou o ruleset "Proteção da Main" com bypass para a integração do agente; o agente continuou sem permissão (HTTP 403) e preparou `ruleset-main.json` com PR obrigatório e o check `testes-e-analise`, que passou a existir neste dia.
