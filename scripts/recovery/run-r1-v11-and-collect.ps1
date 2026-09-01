[CmdletBinding()]
param(
    [string]$Repository = 'C:\Users\Shehr\OneDrive\Desktop\Fehrest',
    [string]$PackagePath = '',
    [string]$EvidenceOut = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedHead = 'ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c'
$ExpectedPackageSha256 = '92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89'
$ExpectedPackageName = 'FEHREST-R1-X1-REPLACEMENT-V11.zip'
$ExpectedSupervisorSha256 = 'c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7'
$ExpectedResultName = 'FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt'
$ExpectedRawName = 'variance-pilot-raw.tar.gz'
$ExpectedFiles = @('RUN_THIS_NOW.cmd', 'replacement.ps1', 'supervisor.py')

function Fail([string]$Message) {
    Write-Host "FAIL_CLOSED=$Message" -ForegroundColor Red
    exit 1
}

function Pass([string]$Message) {
    Write-Host "PASS=$Message" -ForegroundColor Green
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Get-ResultField([string]$Text, [string]$Name) {
    $pattern = '(?m)^' + [Regex]::Escape($Name) + '=(.*)$'
    $m = [Regex]::Match($Text, $pattern)
    if (-not $m.Success) { return $null }
    return $m.Groups[1].Value.Trim()
}

Write-Host '=== Fehrest R1 V11 exact-gate runner ==='
Write-Host 'This wrapper does not score, unblind, run power analysis, or modify sealed R1 semantics.'

if (-not (Test-Path -LiteralPath $Repository -PathType Container)) {
    Fail "REPOSITORY_NOT_FOUND path=$Repository"
}

$git = Get-Command git.exe -ErrorAction SilentlyContinue
if (-not $git) { $git = Get-Command git -ErrorAction SilentlyContinue }
if (-not $git) { Fail 'GIT_NOT_FOUND' }

$head = (& $git.Source -C $Repository rev-parse HEAD 2>&1).ToString().Trim()
if ($LASTEXITCODE -ne 0) { Fail 'GIT_HEAD_READ_FAILED' }
if ($head -ne $ExpectedHead) {
    Fail "SEALED_HEAD_MISMATCH expected=$ExpectedHead actual=$head"
}
Pass "EXACT_SEALED_HEAD_PRECHECK head=$head"

$status = (& $git.Source -C $Repository status --porcelain=v1 --untracked-files=all 2>&1 | Out-String).Trim()
if ($LASTEXITCODE -ne 0) { Fail 'GIT_STATUS_FAILED' }
if ($status.Length -ne 0) { Fail 'REPOSITORY_WORKTREE_NOT_CLEAN' }
Pass 'REPOSITORY_WORKTREE_CLEAN'

try {
    $active = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
        $_.CommandLine -and $_.CommandLine -match 'r1_runner\.py' -and $_.CommandLine -match '\brun\b'
    })
} catch {
    Fail "WINDOWS_CIM_PROCESS_INSPECTION_FAILED $($_.Exception.Message)"
}
if ($active.Count -ne 0) { Fail "ACTIVE_R1_RUNNER_PROCESSES_BEFORE_START count=$($active.Count)" }
Pass 'ACTIVE_R1_RUNNER_PROCESSES_BEFORE_START=0'

if ([string]::IsNullOrWhiteSpace($PackagePath)) {
    $candidates = @(
        (Join-Path ([Environment]::GetFolderPath('Desktop')) $ExpectedPackageName),
        (Join-Path $env:USERPROFILE "Downloads\$ExpectedPackageName"),
        (Join-Path (Get-Location).Path $ExpectedPackageName)
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) }
    if ($candidates.Count -eq 0) {
        Fail "V11_PACKAGE_NOT_FOUND expected_name=$ExpectedPackageName; place the canonical package on Desktop/Downloads or pass -PackagePath"
    }
    $PackagePath = $candidates[0]
}

if (-not (Test-Path -LiteralPath $PackagePath -PathType Leaf)) {
    Fail "V11_PACKAGE_NOT_FOUND path=$PackagePath"
}

$packageSha = Get-Sha256 $PackagePath
if ($packageSha -ne $ExpectedPackageSha256) {
    Fail "V11_PACKAGE_SHA256_MISMATCH expected=$ExpectedPackageSha256 actual=$packageSha"
}
Pass "V11_PACKAGE_SHA256=$packageSha"

$extractRoot = Join-Path $env:TEMP ("fehrest-r1-v11-" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $extractRoot | Out-Null
try {
    Expand-Archive -LiteralPath $PackagePath -DestinationPath $extractRoot -Force

    $actualFiles = @(Get-ChildItem -LiteralPath $extractRoot -File -Recurse)
    $relative = @($actualFiles | ForEach-Object { [IO.Path]::GetRelativePath($extractRoot, $_.FullName).Replace('\\','/') })
    $normalizedExpected = @($ExpectedFiles | Sort-Object)
    $normalizedActual = @($relative | Sort-Object)
    if (($normalizedActual -join '|') -ne ($normalizedExpected -join '|')) {
        Fail "V11_PACKAGE_CONTENTS_MISMATCH expected=$($normalizedExpected -join ',') actual=$($normalizedActual -join ',')"
    }
    Pass 'V11_PACKAGE_CONTENTS=RUN_THIS_NOW.cmd,replacement.ps1,supervisor.py'

    $supervisorPath = Join-Path $extractRoot 'supervisor.py'
    $supervisorSha = Get-Sha256 $supervisorPath
    if ($supervisorSha -ne $ExpectedSupervisorSha256) {
        Fail "V11_SUPERVISOR_SHA256_MISMATCH expected=$ExpectedSupervisorSha256 actual=$supervisorSha"
    }
    Pass "V11_SUPERVISOR_SHA256=$supervisorSha"

    $env:OPENAI_API_KEY = $null

    Write-Host ''
    Write-Host 'Launching canonical V11. Follow its on-screen secure clipboard prompt only.' -ForegroundColor Cyan
    Write-Host 'Do NOT paste credentials into this wrapper, GitHub, chat, or logs.' -ForegroundColor Cyan
    Write-Host ''

    $entry = Join-Path $extractRoot 'RUN_THIS_NOW.cmd'
    & cmd.exe /d /c ('"' + $entry + '"')
    $rc = $LASTEXITCODE
    if ($rc -ne 0) { Fail "V11_EXECUTOR_EXIT_CODE=$rc" }
    Pass 'V11_EXECUTOR_EXIT_CODE=0'

    $roots = @(
        [Environment]::GetFolderPath('Desktop'),
        (Join-Path $env:LOCALAPPDATA 'Fehrest\R1-X1')
    ) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

    $resultCandidates = @()
    foreach ($root in $roots) {
        $resultCandidates += @(Get-ChildItem -LiteralPath $root -Filter $ExpectedResultName -File -Recurse -ErrorAction SilentlyContinue)
    }
    $resultCandidates = @($resultCandidates | Sort-Object LastWriteTimeUtc -Descending)
    if ($resultCandidates.Count -eq 0) { Fail 'RESULT_FILE_NOT_FOUND_AFTER_V11' }
    $resultPath = $resultCandidates[0].FullName
    $resultText = Get-Content -LiteralPath $resultPath -Raw -Encoding UTF8

    $required = [ordered]@{
        R1_VARIANCE_PILOT_FINAL_STATUS = 'EXECUTION_COMPLETE_UNSCORED_REPLACEMENT'
        SOURCE_BATCH_DISPOSITION = 'INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE'
        SECRET_SCAN = 'PASS'
        RAW_SEAL_STATUS = 'PASS'
        RAW_SEAL_REPRODUCIBILITY = 'PASS'
        OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR = 'YES'
        SCORING_STATUS = 'NOT_STARTED'
        UNBLINDING_STATUS = 'NOT_STARTED'
        POWER_ANALYSIS_STATUS = 'NOT_PERFORMED'
        CONFIRMATORY_STATUS = 'NOT_STARTED'
        NEXT_GATE = 'FOUNDER_REVIEW_BEFORE_BLINDED_SCORING'
    }
    foreach ($kv in $required.GetEnumerator()) {
        $actual = Get-ResultField $resultText $kv.Key
        if ($actual -ne $kv.Value) {
            Fail "RESULT_FIELD_MISMATCH field=$($kv.Key) expected=$($kv.Value) actual=$actual"
        }
    }
    Pass 'RESULT_REQUIRED_UNSCORED_FIELDS=PASS'

    $expectedRawSha = Get-ResultField $resultText 'R1_VARIANCE_PILOT_RAW_SHA256'
    if (-not $expectedRawSha -or $expectedRawSha -notmatch '^[0-9a-fA-F]{64}$') {
        Fail 'RESULT_RAW_SHA256_MISSING_OR_INVALID'
    }
    $expectedRawSha = $expectedRawSha.ToLowerInvariant()

    $rawCandidates = @()
    foreach ($root in $roots) {
        $rawCandidates += @(Get-ChildItem -LiteralPath $root -Filter $ExpectedRawName -File -Recurse -ErrorAction SilentlyContinue)
    }
    $rawCandidates = @($rawCandidates | Sort-Object LastWriteTimeUtc -Descending)
    if ($rawCandidates.Count -eq 0) { Fail 'RAW_ARCHIVE_NOT_FOUND_AFTER_V11' }

    $rawPath = $null
    foreach ($candidate in $rawCandidates) {
        if ((Get-Sha256 $candidate.FullName) -eq $expectedRawSha) {
            $rawPath = $candidate.FullName
            break
        }
    }
    if (-not $rawPath) { Fail "RAW_ARCHIVE_SHA256_NO_MATCH expected=$expectedRawSha" }
    Pass "RAW_ARCHIVE_SHA256_MATCHES_RESULT=$expectedRawSha"

    if ([string]::IsNullOrWhiteSpace($EvidenceOut)) {
        $EvidenceOut = Join-Path ([Environment]::GetFolderPath('Desktop')) ('FEHREST-R1-X1-V11-EVIDENCE-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    }
    New-Item -ItemType Directory -Path $EvidenceOut -Force | Out-Null

    $resultCopy = Join-Path $EvidenceOut $ExpectedResultName
    $rawCopy = Join-Path $EvidenceOut $ExpectedRawName
    Copy-Item -LiteralPath $resultPath -Destination $resultCopy
    Copy-Item -LiteralPath $rawPath -Destination $rawCopy

    $manifestPath = Join-Path $EvidenceOut 'COLLECTION-MANIFEST.txt'
    @(
        'COLLECTION_MODE=NON_MUTATING_COPY',
        "SEALED_HEAD=$ExpectedHead",
        "V11_PACKAGE_SHA256=$packageSha",
        "RESULT_FILE_SHA256=$(Get-Sha256 $resultCopy)",
        "RAW_ARCHIVE_SHA256=$(Get-Sha256 $rawCopy)",
        'SCORING_EXECUTED_BY_WRAPPER=NO',
        'UNBLINDING_EXECUTED_BY_WRAPPER=NO',
        'POWER_ANALYSIS_EXECUTED_BY_WRAPPER=NO',
        'CONFIRMATORY_EXECUTION_BY_WRAPPER=NO',
        'SOURCE_EVIDENCE_MUTATION=NO',
        'NEXT_GATE=ISSUE_8_CLOSURE_REVIEW_THEN_ISSUE_11_EXECUTION_INTEGRITY_REVIEW'
    ) | Set-Content -LiteralPath $manifestPath -Encoding utf8NoBOM

    Write-Host ''
    Write-Host 'R1_V11_OPERATOR_BRIDGE=PASS' -ForegroundColor Green
    Write-Host "EVIDENCE_DIRECTORY=$EvidenceOut" -ForegroundColor Green
    Write-Host 'NEXT_ACTION=UPLOAD_OR_PRESERVE_THIS_DIRECTORY_UNCHANGED_FOR_ISSUE_8_REVIEW' -ForegroundColor Green
    exit 0
}
finally {
    if (Test-Path -LiteralPath $extractRoot) {
        Remove-Item -LiteralPath $extractRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
