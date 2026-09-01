# Fehrest repository artifact verifier (fail-closed)
#
# Verifies that every load-bearing artifact mirrored into the repository
# matches its canonical identity exactly:
#   1. exact file size and SHA-256 for each authority binary;
#   2. sealed supervisor byte identity for the browseable V11 mirror;
#   3. package member identity: the browseable supervisor.py must be
#      byte-identical to the supervisor.py member inside the V11 zip;
#   4. exact Git blob identities for every mirrored path.
#
# Any mismatch halts with a non-zero exit code. This script never mutates
# repository content, never scores anything, and never touches R1 semantics.

# Run from a repository checkout root (or pass -RepoRoot explicitly).
[CmdletBinding()]
param(
    [string]$RepoRoot = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
    $RepoRoot = (Get-Location).Path
}

$expected = @(
    @{
        Path   = "artifacts/r1/v11/FEHREST-R1-X1-REPLACEMENT-V11.zip"
        Role   = "ACTIVE_R1_EXECUTOR_PACKAGE"
        Size   = 10257
        Sha256 = "92ee711067d65bd7d68a0204becc916d3e9322fa975d815d8da6126e8c31dd89"
        Blob   = "c64f2ea918f0d431533bad30c792a51eca98bb1e"
    },
    @{
        Path   = "artifacts/r1/v11/browseable/RUN_THIS_NOW.cmd"
        Role   = "V11_LAUNCHER_ENTRYPOINT_BROWSEABLE"
        Size   = 1194
        Blob   = "49b52a89367d18d6d9334fcafaa64a3ab303648f"
    },
    @{
        Path   = "artifacts/r1/v11/browseable/replacement.ps1"
        Role   = "V11_LAUNCHER_PLUMBING_BROWSEABLE"
        Size   = 10925
        Blob   = "3034959f91be14a4deda996435032ec80d049d0f"
    },
    @{
        Path   = "artifacts/r1/v11/browseable/supervisor.py"
        Role   = "V11_SEALED_SUPERVISOR_BROWSEABLE"
        Size   = 20042
        Sha256 = "c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7"
        Blob   = "67fa65c71c8e509b6f16b3426cda29c71b5b7f9f"
    },
    @{
        Path   = "artifacts/r1/evidence-collector/FEHREST-R1-X1-REPLACEMENT-EVIDENCE-COLLECTOR-V3.zip"
        Role   = "REPOSITORY_OWNED_EVIDENCE_COLLECTOR_PACKAGE"
        Size   = 5247
        Sha256 = "eb2207e9f155c29789d75ef708c1aaa81b2a21d61303b0660fb820ea18646bbb"
        Blob   = "f30e37a2644e04eed0a52b48aa4c635845193b9a"
    },
    @{
        Path   = "artifacts/r1/evidence-collector/browseable/COLLECT_EVIDENCE_NOW.cmd"
        Role   = "EVIDENCE_COLLECTOR_ENTRYPOINT_BROWSEABLE"
        Size   = 290
        Blob   = "fadb994d37df7236d4c57841779bfefea75a4b6f"
    },
    @{
        Path   = "artifacts/r1/evidence-collector/browseable/collect-r1-evidence.ps1"
        Role   = "EVIDENCE_COLLECTOR_SCRIPT_BROWSEABLE"
        Size   = 14313
        Blob   = "9dad6c91288390db9f0e6ea7e2a4c3232c1b103b"
    },
    @{
        Path   = "artifacts/r1/evidence-collector/browseable/README.txt"
        Role   = "EVIDENCE_COLLECTOR_README_BROWSEABLE"
        Size   = 1110
        Blob   = "4783a7fc26bc47eea3a1083c7ee7b82260708273"
    },
    @{
        Path   = "artifacts/recovery/historical-r1-v1.1/Fehrest-historical-r1-v1.1-ed79.bundle"
        Role   = "HISTORICAL_GIT_OBJECT_AUTHORITY_BUNDLE"
        Size   = 823833
        Sha256 = "a36639da9731cd4778777e14b980ca04784f9a00890a57d0a3fc10591f54f5f9"
        Blob   = "fba4aa77a6e4a87a9a23a73962cc5ef0b308855c"
    },
    @{
        Path   = "scripts/recovery/publish-historical-objects.ps1"
        Role   = "HISTORICAL_BUNDLE_PUBLISHER_TOOL"
        Size   = 5903
        Blob   = "c1f3edac481a8b3fab7c54cb77f117e12ae0595f"
    }
)

$SealedSupervisorSha256 = "c63bca3157068a22c82b95c5613417c745715dc5eb9d54d9a9c92f3b0ab641b7"
$V11ZipRelative = "artifacts/r1/v11/FEHREST-R1-X1-REPLACEMENT-V11.zip"

function Fail-Closed([string]$Reason) {
    Write-Host "FEHREST_ARTIFACT_VERIFICATION_STATUS=FAIL_CLOSED"
    Write-Host "FAILURE_REASON=$Reason"
    exit 1
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot ".git") )) {
    Fail-Closed "REPO_ROOT_NOT_FOUND:$RepoRoot"
}

# 1. Size / SHA-256 / Git blob identity for every mirrored path.
foreach ($item in $expected) {
    $relativePath = $item.Path
    $full = Join-Path $RepoRoot ($item.Path -replace "/", "\")
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        Fail-Closed "ARTIFACT_MISSING:$($item.Path)"
    }
    $actualSize = (Get-Item -LiteralPath $full).Length
    if ($actualSize -ne $item.Size) {
        Fail-Closed "SIZE_MISMATCH:$($item.Path) expected=$($item.Size) actual=$actualSize"
    }
    if ($item.ContainsKey("Sha256")) {
        $actualSha = (Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualSha -ne $item.Sha256) {
            Fail-Closed "SHA256_MISMATCH:$($item.Path) expected=$($item.Sha256) actual=$actualSha"
        }
    }
    # --no-filters guarantees the hash covers the exact stored bytes and is
    # independent of any attribute/clean-filter resolution on the host.
    $blobOut = & git -C $RepoRoot hash-object --no-filters $relativePath
    if ($LASTEXITCODE -ne 0) {
        Fail-Closed "GIT_HASH_OBJECT_FAILED:$($item.Path)"
    }
    $actualBlob = (@($blobOut)[0]).Trim()
    if ($actualBlob -ne $item.Blob) {
        Fail-Closed "GIT_BLOB_MISMATCH:$($item.Path) expected=$($item.Blob) actual=$actualBlob"
    }
    Write-Host "ARTIFACT_OK=$($item.Path)"
}

# 2. Package member identity: supervisor.py inside the V11 zip must be
#    byte-identical to the sealed supervisor and to the browseable mirror.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipPath = Join-Path $RepoRoot ($V11ZipRelative -replace "/", "\")
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entryNames = @($zip.Entries | ForEach-Object { $_.FullName })
    foreach ($required in @("RUN_THIS_NOW.cmd", "replacement.ps1", "supervisor.py")) {
        if ($entryNames -notcontains $required) {
            Fail-Closed "V11_ZIP_MEMBER_MISSING:$required"
        }
    }
    $entry = $zip.Entries | Where-Object { $_.FullName -eq "supervisor.py" }
    if ($entry.Length -ne 20042) {
        Fail-Closed "V11_ZIP_SUPERVISOR_SIZE_MISMATCH expected=20042 actual=$($entry.Length)"
    }
    $stream = $entry.Open()
    $sha = [System.Security.Cryptography.SHA256]::Create()
    $zipSupervisorSha = ([System.BitConverter]::ToString($sha.ComputeHash($stream))).Replace("-", "").ToLowerInvariant()
    $stream.Dispose()
    $sha.Dispose()
    if ($zipSupervisorSha -ne $SealedSupervisorSha256) {
        Fail-Closed "V11_ZIP_SUPERVISOR_SHA256_MISMATCH expected=$SealedSupervisorSha256 actual=$zipSupervisorSha"
    }
}
finally {
    $zip.Dispose()
}

Write-Host "V11_ZIP_SUPERVISOR_IDENTITY=PASS"
Write-Host "FEHREST_ARTIFACT_VERIFICATION_STATUS=PASS"
Write-Host "SCORING_AUTHORIZED=NO"
Write-Host "UNBLINDING_AUTHORIZED=NO"
Write-Host "POWER_ANALYSIS_AUTHORIZED=NO"
Write-Host "CONFIRMATORY_AUTHORIZED=NO"
Write-Host "SPEC_002_ACTIVATED=NO"
exit 0
