[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ExpectedBundleSha256 = "a36639da9731cd4778777e14b980ca04784f9a00890a57d0a3fc10591f54f5f9"
$SealedCommit = "ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c"
$SealedTree = "f7ea7e0f57019c8061a4019ac614730f68750f19"
$DestinationRef = "refs/heads/historical/r1-v1.1"
$RemoteUrl = "https://github.com/TheHalfMoon/Fehrest.git"
$BundleName = "Fehrest-historical-r1-v1.1-ed79.bundle"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BundlePath = Join-Path $ScriptRoot $BundleName
$TempRoot = Join-Path $env:TEMP ("fehrest-history-publish-" + [Guid]::NewGuid().ToString("N"))

function Fail-Closed([string]$Reason) {
    Write-Host "FEHREST_HISTORICAL_PUBLICATION_STATUS=HALTED"
    Write-Host "FAILURE_REASON=$Reason"
    Write-Host "FORCE_PUSH_USED=NO"
    Write-Host "REBASE_USED=NO"
    Write-Host "DESTRUCTIVE_HISTORY_REWRITE_USED=NO"
    throw $Reason
}

function Invoke-Git([string[]]$GitArgs, [switch]$AllowOutput) {
    $output = & git @GitArgs 2>&1
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        $safe = ($output | ForEach-Object { $_.ToString() }) -join " | "
        throw "git failed (exit=$exitCode): git $($GitArgs -join ' ') :: $safe"
    }
    if ($AllowOutput) {
        # The comma operator preserves the array across the function return
        # boundary, so callers index output lines rather than characters of a
        # single-line string (PowerShell unrolls single-element arrays on
        # plain return).
        , @($output | ForEach-Object { $_.ToString() })
    }
}

try {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Fail-Closed "GIT_NOT_FOUND"
    }
    if (-not (Test-Path -LiteralPath $BundlePath -PathType Leaf)) {
        Fail-Closed "BUNDLE_NOT_FOUND:$BundlePath"
    }

    $actualBundleSha = (Get-FileHash -LiteralPath $BundlePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualBundleSha -ne $ExpectedBundleSha256) {
        Fail-Closed "BUNDLE_SHA256_MISMATCH expected=$ExpectedBundleSha256 actual=$actualBundleSha"
    }

    New-Item -ItemType Directory -Force -Path $TempRoot | Out-Null
    $repoPath = Join-Path $TempRoot "repo"

    Invoke-Git @("clone", "--no-checkout", $BundlePath, $repoPath)
    Invoke-Git @("-C", $repoPath, "fsck", "--full", "--strict")

    $head = (Invoke-Git @("-C", $repoPath, "rev-parse", "$SealedCommit^{commit}") -AllowOutput)[0].Trim()
    $tree = (Invoke-Git @("-C", $repoPath, "rev-parse", "$SealedCommit^{tree}") -AllowOutput)[0].Trim()
    if ($head -ne $SealedCommit) {
        Fail-Closed "SEALED_COMMIT_MISMATCH expected=$SealedCommit actual=$head"
    }
    if ($tree -ne $SealedTree) {
        Fail-Closed "SEALED_TREE_MISMATCH expected=$SealedTree actual=$tree"
    }

    # Create only a local source ref. This does not rewrite any remote history.
    Invoke-Git @("-C", $repoPath, "update-ref", "refs/heads/recovered/r1-v1.1", $SealedCommit)

    $before = @(Invoke-Git @("ls-remote", "--heads", $RemoteUrl, $DestinationRef) -AllowOutput)
    if ($before.Count -gt 1) {
        Fail-Closed "REMOTE_REF_AMBIGUOUS:$DestinationRef"
    }
    if ($before.Count -eq 1 -and -not [string]::IsNullOrWhiteSpace($before[0])) {
        $parts = $before[0] -split "\s+"
        $remoteSha = $parts[0].Trim()
        if ($remoteSha -ne $SealedCommit) {
            Fail-Closed "REMOTE_REF_EXISTS_WITH_DIFFERENT_SHA expected=$SealedCommit actual=$remoteSha"
        }

        Write-Host "FEHREST_HISTORICAL_PUBLICATION_STATUS=ALREADY_PRESENT"
        Write-Host "BUNDLE_SHA256=$actualBundleSha"
        Write-Host "SEALED_COMMIT=$SealedCommit"
        Write-Host "SEALED_TREE=$SealedTree"
        Write-Host "DESTINATION_REF=$DestinationRef"
        Write-Host "REMOTE_REF_SHA=$remoteSha"
        Write-Host "FORCE_PUSH_USED=NO"
        Write-Host "REBASE_USED=NO"
        Write-Host "DESTRUCTIVE_HISTORY_REWRITE_USED=NO"
        Write-Host "OPERATIONAL_MAIN_MUTATED=NO"
        Write-Host "NEXT_GATE=CHATGPT_VERIFY_GITHUB_OBJECT_REACHABILITY"
        exit 0
    }

    # Non-force creation of a dedicated archival ref. No main update is attempted.
    Invoke-Git @("-C", $repoPath, "push", $RemoteUrl, "refs/heads/recovered/r1-v1.1:$DestinationRef")

    $after = @(Invoke-Git @("ls-remote", "--heads", $RemoteUrl, $DestinationRef) -AllowOutput)
    if ($after.Count -ne 1 -or [string]::IsNullOrWhiteSpace($after[0])) {
        Fail-Closed "REMOTE_REF_NOT_VISIBLE_AFTER_PUSH:$DestinationRef"
    }
    $afterParts = $after[0] -split "\s+"
    $remoteShaAfter = $afterParts[0].Trim()
    if ($remoteShaAfter -ne $SealedCommit) {
        Fail-Closed "REMOTE_REF_SHA_MISMATCH_AFTER_PUSH expected=$SealedCommit actual=$remoteShaAfter"
    }

    Write-Host "FEHREST_HISTORICAL_PUBLICATION_STATUS=PUBLISHED"
    Write-Host "BUNDLE_SHA256=$actualBundleSha"
    Write-Host "SEALED_COMMIT=$SealedCommit"
    Write-Host "SEALED_TREE=$SealedTree"
    Write-Host "DESTINATION_REF=$DestinationRef"
    Write-Host "REMOTE_REF_SHA=$remoteShaAfter"
    Write-Host "FORCE_PUSH_USED=NO"
    Write-Host "REBASE_USED=NO"
    Write-Host "DESTRUCTIVE_HISTORY_REWRITE_USED=NO"
    Write-Host "OPERATIONAL_MAIN_MUTATED=NO"
    Write-Host "NEXT_GATE=CHATGPT_VERIFY_GITHUB_OBJECT_REACHABILITY"
}
catch {
    $message = $_.Exception.Message
    if ($message -notmatch '^GIT_NOT_FOUND$|^BUNDLE_NOT_FOUND:|^BUNDLE_SHA256_MISMATCH|^SEALED_COMMIT_MISMATCH|^SEALED_TREE_MISMATCH|^REMOTE_REF_') {
        Write-Host "FEHREST_HISTORICAL_PUBLICATION_STATUS=HALTED"
        Write-Host "FAILURE_REASON=$message"
        Write-Host "FORCE_PUSH_USED=NO"
        Write-Host "REBASE_USED=NO"
        Write-Host "DESTRUCTIVE_HISTORY_REWRITE_USED=NO"
    }
    exit 1
}
finally {
    if (Test-Path -LiteralPath $TempRoot) {
        Remove-Item -LiteralPath $TempRoot -Recurse -Force -ErrorAction SilentlyContinue
    }
}
