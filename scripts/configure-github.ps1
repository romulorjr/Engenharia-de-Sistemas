#Requires -Version 7.0
[CmdletBinding()]
param(
    [switch]$Apply,
    [switch]$ProtectBranches,
    [string[]]$RequiredChecks = @()
)
$ErrorActionPreference = 'Stop'
$configPath = Join-Path $PSScriptRoot '../.github/repository-setup.json'
$config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
if (-not $Apply) {
    Write-Output ("Plano para {0}: {1} labels, {2} milestones, {3} issues." -f $config.repository, $config.labels.Count, $config.milestones.Count, $config.issues.Count)
    Write-Output 'Use -Apply para aplicar labels e milestones. Acrescente -ProtectBranches para proteger main/develop.'
    Write-Output 'Proteções existentes serão preservadas. RequiredChecks só deve conter nomes reais de checks já executados.'
    exit 0
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'Instale GitHub CLI e execute gh auth login.' }
& gh auth status
if ($LASTEXITCODE -ne 0) { throw 'Autenticação GitHub CLI indisponível.' }
function Invoke-GitHub {
    param([string]$Method, [string]$Endpoint, $Body = $null)
    $arguments = @('api', '--method', $Method, $Endpoint)
    if ($null -ne $Body) {
        $arguments += @('--input', '-')
        $result = ($Body | ConvertTo-Json -Depth 12 -Compress) | & gh @arguments
    } else {
        $result = & gh @arguments
    }
    if ($LASTEXITCODE -ne 0) { throw "Falha em $Method $Endpoint. Operação interrompida; pode ser retomada." }
    if ($result) { return (($result -join "`n") | ConvertFrom-Json) }
}
function Get-GitHubCollection {
    param([string]$Endpoint)
    $page = 1
    $items = @()
    do {
        $batch = @(Invoke-GitHub GET ("${Endpoint}?per_page=100&page=$page"))
        $items += $batch
        $page++
    } while ($batch.Count -eq 100)
    return $items
}
$prefix = "repos/$($config.repository)"
$existingLabels = @(Get-GitHubCollection "$prefix/labels")
foreach ($label in $config.labels) {
    if ($existingLabels.name -contains $label.name) {
        Write-Output "Label preservada: $($label.name)"
    } else {
        Invoke-GitHub POST "$prefix/labels" $label | Out-Null
        Write-Output "Label criada: $($label.name)"
    }
}
$existingMilestones = @(Get-GitHubCollection "$prefix/milestones") # Abertos.
# Consultar fechados separadamente sem mudar sua situação.
$closed = @()
$page = 1
do {
    $batch = @(Invoke-GitHub GET "$prefix/milestones?state=closed&per_page=100&page=$page")
    $closed += $batch
    $page++
} while ($batch.Count -eq 100)
$existingMilestones += $closed
$milestoneNumbers = @{}
foreach ($milestone in $config.milestones) {
    $found = @($existingMilestones | Where-Object title -eq $milestone.title)
    if ($found.Count -gt 1) { throw "Milestone duplicado: $($milestone.title)" }
    if ($found.Count -eq 1) {
        $milestoneNumbers[$milestone.title] = $found[0].number
        Write-Output "Milestone preservado: $($milestone.title)"
    } else {
        $created = Invoke-GitHub POST "$prefix/milestones" $milestone
        $milestoneNumbers[$milestone.title] = $created.number
        Write-Output "Milestone criado: $($milestone.title)"
    }
}
foreach ($item in $config.issues) {
    $issue = Invoke-GitHub GET "$prefix/issues/$($item.number)"
    Invoke-GitHub POST "$prefix/issues/$($item.number)/labels" @{ labels = @($item.labels) } | Out-Null
    $target = $milestoneNumbers[$item.milestone]
    if ($null -eq $issue.milestone) {
        Invoke-GitHub PATCH "$prefix/issues/$($item.number)" @{ milestone = $target } | Out-Null
    } elseif ($issue.milestone.number -ne $target) {
        Write-Warning "Issue #$($item.number) já tem outro milestone; preservado."
    }
}
if ($ProtectBranches) {
    foreach ($branchName in @('main', 'develop')) {
        $branch = Invoke-GitHub GET "$prefix/branches/$branchName"
        if ($branch.protected) {
            Write-Warning "Proteção de $branchName já existe; preservada. Revise manualmente checks e regras."
            continue
        }
        $statusChecks = $null
        if ($RequiredChecks.Count -gt 0) {
            $statusChecks = @{ strict = $true; contexts = @($RequiredChecks) }
        }
        $protection = @{
            required_status_checks = $statusChecks
            enforce_admins = $true
            required_pull_request_reviews = @{
                dismiss_stale_reviews = $true
                require_code_owner_reviews = $false
                required_approving_review_count = 1
            }
            restrictions = $null
            required_conversation_resolution = $true
            allow_force_pushes = $false
            allow_deletions = $false
        }
        Invoke-GitHub PUT "$prefix/branches/$branchName/protection" $protection | Out-Null
        $verified = Invoke-GitHub GET "$prefix/branches/$branchName"
        if (-not $verified.protected) { throw "Proteção não confirmada em $branchName." }
        Write-Output "Proteção confirmada: $branchName"
    }
}
Write-Output 'Configuração concluída. Confira labels, milestones e issues no GitHub.'
