# Configuração administrativa do GitHub

## Estado desta entrega
As 24 issues foram criadas via conector. A branch de documentação e develop foram criadas para iniciar o fluxo. Labels, milestones e proteção **não foram aplicados**: o conector desta sessão não expõe as operações administrativas necessárias e o GitHub CLI não está instalado no ambiente. A permissão informada pelo repositório não significa que todas as operações estejam disponíveis pela ferramenta.

## Configuração reproduzível
[repository-setup.json](../.github/repository-setup.json) define dez labels, sete milestones com datas e vínculos das 24 issues. [configure-github.ps1](../scripts/configure-github.ps1) aplica a configuração com PowerShell 7 e GitHub CLI autenticado por conta autorizada. Não colocar tokens nos arquivos.

Na raiz de um checkout do PR:

```powershell
# Apenas mostra o plano; não precisa de autenticação.
pwsh -File scripts/configure-github.ps1
# Aplicar labels, milestones e vínculos.
pwsh -File scripts/configure-github.ps1 -Apply
# Aplicar também proteção de main e develop.
pwsh -File scripts/configure-github.ps1 -Apply -ProtectBranches
```

O script pode ser retomado: preserva labels e milestones existentes, adiciona labels às issues sem remover outras, não troca milestone já atribuído e não substitui proteções existentes. Falhas interrompem a execução. Confira avisos de divergência e configuração existente manualmente. Milestones internos podem ser ajustados pelo grupo; datas do checkpoint e entrega final permanecem conforme o PDF.

Proteção proposta: uma aprovação, resolução de conversas, descarte de aprovações desatualizadas, aplicação a administradores e bloqueio de force push/exclusão. Requer outro integrante com acesso para revisar.

## Checks obrigatórios
Ainda não há workflow de aplicação. A #3 deve criá-lo, executá-lo com sucesso e então configurar os nomes reais dos checks como obrigatórios, por exemplo pela tela de proteção do GitHub. Não cadastrar checks imaginários que bloqueiem todos os merges. O parâmetro RequiredChecks permite fornecê-los ao criar uma proteção nova; se a proteção já existir, o script a preserva e será necessário atualizá-la pelo GitHub.

## Verificação após aplicação
Conferir labels, sete milestones e seus vencimentos; vínculos nas issues #1–#24; main/develop protegidas; PR exige aprovação e, após #3, CI verde. O script foi validado localmente quanto à sintaxe e modo de planejamento; as escritas administrativas remotas permanecem não executadas nesta entrega.
