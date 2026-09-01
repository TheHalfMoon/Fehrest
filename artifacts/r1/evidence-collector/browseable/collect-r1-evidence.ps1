$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ExpectedHead = "ed79d8ecee08e4ce4dd384edaffc4a27cfd6d37c"
$ExpectedV11Digest = "5463bfddcf076b930e35c3fe5a208b94f0af720e935a3dc8ae5b88432709f6e2"
$ExpectedRunnerDigest = "30b5e5937d5d103acf58727652a90cab6b253aa5f1dbe633922f242082d5b89f"
$ExpectedExternalBundle = "17934f84a07afef08e469b0526d343d26e5597ea3455e575b5f9c46ae91c321e"
$ExpectedSourceArming = "2e360072931ac2adfbdbba94da20d9198f8b24474852429545bcd14cd8653205"
$ExpectedSeed = "r1-x1-f10c4a673c44d412adb9c4f5a495d4c38265ce38301a778128b0fab622ed8a04"
$ExpectedRunnerVersion = "r1-external-runner/1.1.0"
$ExpectedModel = "gpt-5.6-terra"

function Fail([string]$Reason) {
    Write-Host "EVIDENCE_COLLECTION_STATUS=HALTED"
    Write-Host "FAILURE_REASON=$Reason"
    Write-Host "SOURCE_EVIDENCE_MUTATED=NO"
    exit 1
}

function Require-Leaf([string]$Path, [string]$Reason) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { Fail $Reason }
}

function Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-ResultField([string[]]$Lines, [string]$Name) {
    $Prefix = "$Name="
    $Matches = @($Lines | Where-Object { $_.StartsWith($Prefix, [System.StringComparison]::Ordinal) })
    if ($Matches.Count -ne 1) { Fail "RESULT_FIELD_CARDINALITY_$Name" }
    return $Matches[0].Substring($Prefix.Length)
}

function Get-LogField([string]$Path, [string]$Name) {
    Require-Leaf $Path "LOG_FILE_NOT_FOUND_$Name"
    $Prefix = "$Name="
    $Matches = @(Get-Content -LiteralPath $Path -Encoding UTF8 | Where-Object { $_.StartsWith($Prefix, [System.StringComparison]::Ordinal) })
    if ($Matches.Count -ne 1) { Fail "LOG_FIELD_CARDINALITY_$Name" }
    return $Matches[0].Substring($Prefix.Length)
}

function Require-JsonField($Object, [string]$Name, $Expected) {
    $Prop = $Object.PSObject.Properties[$Name]
    if ($null -eq $Prop) { Fail "JSON_FIELD_MISSING_$Name" }
    if ($Prop.Value -ne $Expected) { Fail "JSON_FIELD_MISMATCH_$Name" }
}

$Desktop = [Environment]::GetFolderPath("Desktop")
if (-not (Test-Path -LiteralPath $Desktop -PathType Container)) { Fail "DESKTOP_NOT_FOUND" }

$Result = Join-Path $Desktop "FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt"
Require-Leaf $Result "RESULT_FILE_NOT_FOUND"
$Lines = @(Get-Content -LiteralPath $Result -Encoding UTF8)

if ((Get-ResultField $Lines "R1_VARIANCE_PILOT_FINAL_STATUS") -ne "EXECUTION_COMPLETE_UNSCORED_REPLACEMENT") { Fail "RESULT_NOT_SUCCESSFUL_REPLACEMENT" }
if ((Get-ResultField $Lines "SOURCE_BATCH_DISPOSITION") -ne "INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE") { Fail "SOURCE_BATCH_DISPOSITION_INVALID" }
if ((Get-ResultField $Lines "SECRET_SCAN") -ne "PASS") { Fail "SECRET_SCAN_NOT_PASS" }
if ((Get-ResultField $Lines "RAW_SEAL_STATUS") -ne "PASS") { Fail "RAW_SEAL_STATUS_NOT_PASS" }
if ((Get-ResultField $Lines "RAW_SEAL_REPRODUCIBILITY") -ne "PASS") { Fail "RAW_SEAL_REPRODUCIBILITY_NOT_PASS" }
if ((Get-ResultField $Lines "OPENAI_API_KEY_CLEARED_FROM_SUPERVISOR") -ne "YES") { Fail "API_KEY_CLEARANCE_NOT_CONFIRMED" }
if ((Get-ResultField $Lines "SCORING_STATUS") -ne "NOT_STARTED") { Fail "SCORING_ALREADY_STARTED" }
if ((Get-ResultField $Lines "UNBLINDING_STATUS") -ne "NOT_STARTED") { Fail "UNBLINDING_ALREADY_STARTED" }
if ((Get-ResultField $Lines "POWER_ANALYSIS_STATUS") -ne "NOT_PERFORMED") { Fail "POWER_ANALYSIS_ALREADY_PERFORMED" }
if ((Get-ResultField $Lines "CONFIRMATORY_STATUS") -ne "NOT_STARTED") { Fail "CONFIRMATORY_ALREADY_STARTED" }
if ((Get-ResultField $Lines "NEXT_GATE") -ne "FOUNDER_REVIEW_BEFORE_BLINDED_SCORING") { Fail "NEXT_GATE_UNEXPECTED" }

foreach ($Field in @("DUPLICATE_RECORD_IDS","DUPLICATE_ORDER_IDS","ORPHAN_RAW_COUNT","RECORD_MISSING_RAW_COUNT","ORDER_WITHOUT_RECORD_COUNT","RECORD_WITHOUT_ORDER_COUNT")) {
    if ((Get-ResultField $Lines $Field) -ne "0") { Fail "NONZERO_$Field" }
}
$Records = [int](Get-ResultField $Lines "TRANSPORT_ATTEMPT_RECORDS")
$RawFiles = [int](Get-ResultField $Lines "RAW_FILES")
$OrderEntries = [int](Get-ResultField $Lines "EXECUTION_ORDER_ENTRIES")
if (-not ($Records -eq $RawFiles -and $RawFiles -eq $OrderEntries)) { Fail "RECORD_RAW_ORDER_CARDINALITY_MISMATCH" }

$ModelReturned = Get-ResultField $Lines "MODEL_RETURNED_VALUES"
if ($ModelReturned -ne "" -and $ModelReturned -ne $ExpectedModel) { Fail "MODEL_RETURNED_VALUES_UNEXPECTED" }

$ReplacementRoot = Get-ResultField $Lines "REPLACEMENT_ROOT"
if (-not (Test-Path -LiteralPath $ReplacementRoot -PathType Container)) { Fail "REPLACEMENT_ROOT_NOT_FOUND" }
$IncidentSha = (Get-ResultField $Lines "INCIDENT_SHA256").ToLowerInvariant()
if ($IncidentSha -notmatch '^[0-9a-f]{64}$') { Fail "INCIDENT_SHA256_FORMAT_INVALID" }
$RecordedRawSha = (Get-ResultField $Lines "R1_VARIANCE_PILOT_RAW_SHA256").ToLowerInvariant()
if ($RecordedRawSha -notmatch '^[0-9a-f]{64}$') { Fail "RAW_SHA256_FORMAT_INVALID" }

$Base = Join-Path $env:LOCALAPPDATA "Fehrest\R1-X1"
$Control = Join-Path $Base "replacement-current.json"
$SourceRoot = Join-Path $Base "variance-pilot-599054280a96"
$SourceArming = Join-Path $SourceRoot "ARMING-MANIFEST.json"
$SourcePreflight = Join-Path $SourceRoot "preflight.json"
$ReplacementArming = Join-Path $ReplacementRoot "REPLACEMENT-ARMING-MANIFEST.json"
$ReplacementPreflight = Join-Path $ReplacementRoot "preflight.json"
$Logs = Join-Path $ReplacementRoot "supervisor-logs"
$Raw = Join-Path $ReplacementRoot "runs\variance-pilot-raw.tar.gz"
$Incident = Join-Path (Join-Path $Base "incidents") ("R1-X1-INCIDENT-" + $IncidentSha.Substring(0,12) + ".json")

foreach ($Pair in @(
    @($Control,"CONTROL_NOT_FOUND"),
    @($SourceArming,"SOURCE_ARMING_NOT_FOUND"),
    @($SourcePreflight,"SOURCE_PREFLIGHT_NOT_FOUND"),
    @($ReplacementArming,"REPLACEMENT_ARMING_NOT_FOUND"),
    @($ReplacementPreflight,"REPLACEMENT_PREFLIGHT_NOT_FOUND"),
    @($Raw,"RAW_ARCHIVE_NOT_FOUND"),
    @($Incident,"INCIDENT_NOT_FOUND")
)) { Require-Leaf $Pair[0] $Pair[1] }
if (-not (Test-Path -LiteralPath $Logs -PathType Container)) { Fail "SUPERVISOR_LOGS_NOT_FOUND" }

if ((Sha256 $Raw) -ne $RecordedRawSha) { Fail "RAW_SHA256_MISMATCH" }
if ((Sha256 $SourceArming) -ne $ExpectedSourceArming) { Fail "SOURCE_ARMING_SHA256_MISMATCH" }
if ((Sha256 $Incident) -ne $IncidentSha) { Fail "INCIDENT_SHA256_MISMATCH" }
if ((Sha256 $SourcePreflight) -ne (Sha256 $ReplacementPreflight)) { Fail "REPLACEMENT_PREFLIGHT_NOT_BYTE_IDENTICAL" }

$ControlJson = Get-Content -LiteralPath $Control -Raw -Encoding UTF8 | ConvertFrom-Json
Require-JsonField $ControlJson "incident_sha256" $IncidentSha
Require-JsonField $ControlJson "replacement_root" $ReplacementRoot
Require-JsonField $ControlJson "seed" $ExpectedSeed
Require-JsonField $ControlJson "replacement_arming_manifest_sha256" (Sha256 $ReplacementArming)

$ArmingJson = Get-Content -LiteralPath $ReplacementArming -Raw -Encoding UTF8 | ConvertFrom-Json
Require-JsonField $ArmingJson "canonical_commit" $ExpectedHead
Require-JsonField $ArmingJson "r1_v1_1_digest" $ExpectedV11Digest
Require-JsonField $ArmingJson "runner_fileset_sha256" $ExpectedRunnerDigest
Require-JsonField $ArmingJson "external_bundle_sha256" $ExpectedExternalBundle
Require-JsonField $ArmingJson "randomization_seed" $ExpectedSeed
Require-JsonField $ArmingJson "runner_version" $ExpectedRunnerVersion
Require-JsonField $ArmingJson "model_requested" $ExpectedModel
Require-JsonField $ArmingJson "reasoning_effort" "medium"
Require-JsonField $ArmingJson "max_output" 1024
Require-JsonField $ArmingJson "maintenance_sessions" 168
Require-JsonField $ArmingJson "continuation_sessions" 720
Require-JsonField $ArmingJson "total_sessions" 888
Require-JsonField $ArmingJson "model_calls_at_replacement_seal" 0
Require-JsonField $ArmingJson "scoring_status" "NOT_STARTED"
Require-JsonField $ArmingJson "unblinding_status" "NOT_STARTED"
Require-JsonField $ArmingJson "confirmatory_status" "NOT_STARTED"
Require-JsonField $ArmingJson "preflight_record_sha256" (Sha256 $ReplacementPreflight)

$IncidentJson = Get-Content -LiteralPath $Incident -Raw -Encoding UTF8 | ConvertFrom-Json
Require-JsonField $IncidentJson "source_canonical_commit" $ExpectedHead
Require-JsonField $IncidentJson "source_arming_manifest_sha256" $ExpectedSourceArming
Require-JsonField $IncidentJson "failure_class" "INFRASTRUCTURE_CONCURRENCY_EVIDENCE_BREACH"
Require-JsonField $IncidentJson "disposition" "INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE"
Require-JsonField $IncidentJson "source_raw_count" 109
Require-JsonField $IncidentJson "source_record_count" 109
Require-JsonField $IncidentJson "source_order_entry_count" 112
Require-JsonField $IncidentJson "raw_outputs_preserved_unchanged" $true
Require-JsonField $IncidentJson "scoring_performed" $false
Require-JsonField $IncidentJson "unblinding_performed" $false
Require-JsonField $IncidentJson "confirmatory_performed" $false
Require-JsonField $IncidentJson "replacement_design_change" $false
Require-JsonField $IncidentJson "replacement_seed_change" $false
Require-JsonField $IncidentJson "replacement_model_condition_change" $false
Require-JsonField $IncidentJson "replacement_uses_same_v1_1_protocol" $true

$RunnerStdout = Join-Path $Logs "runner-stdout.txt"
$Seal1Stdout = Join-Path $Logs "seal1-stdout.txt"
$Seal2Stdout = Join-Path $Logs "seal2-stdout.txt"
if ((Get-LogField $RunnerStdout "R1_VARIANCE_PILOT_STATUS") -ne "EXECUTION_COMPLETE_UNSCORED") { Fail "RUNNER_COMPLETE_MARKER_MISSING" }
if ((Get-LogField $RunnerStdout "PLANNED_TOTAL_SESSIONS") -ne "888") { Fail "RUNNER_PLANNED_TOTAL_SESSIONS_CHANGED" }
if ((Get-LogField $Seal1Stdout "R1_VARIANCE_PILOT_RAW_SHA256").ToLowerInvariant() -ne $RecordedRawSha) { Fail "SEAL1_SHA_MISMATCH" }
if ((Get-LogField $Seal2Stdout "R1_VARIANCE_PILOT_RAW_SHA256").ToLowerInvariant() -ne $RecordedRawSha) { Fail "SEAL2_SHA_MISMATCH" }

$Stage = Join-Path $env:TEMP ("fehrest-r1-evidence-v3-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $Stage | Out-Null
try {
    $Bindings = Join-Path $Stage "bindings"
    $PackagedLogs = Join-Path $Stage "supervisor-logs"
    New-Item -ItemType Directory -Path $Bindings | Out-Null

    Copy-Item -LiteralPath $Result -Destination (Join-Path $Stage "FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt")
    Copy-Item -LiteralPath $Raw -Destination (Join-Path $Stage "variance-pilot-raw.tar.gz")
    Copy-Item -LiteralPath $Control -Destination (Join-Path $Bindings "replacement-current.json")
    Copy-Item -LiteralPath $ReplacementArming -Destination (Join-Path $Bindings "REPLACEMENT-ARMING-MANIFEST.json")
    Copy-Item -LiteralPath $ReplacementPreflight -Destination (Join-Path $Bindings "replacement-preflight.json")
    Copy-Item -LiteralPath $SourceArming -Destination (Join-Path $Bindings "SOURCE-ARMING-MANIFEST.json")
    Copy-Item -LiteralPath $SourcePreflight -Destination (Join-Path $Bindings "source-preflight.json")
    Copy-Item -LiteralPath $Incident -Destination (Join-Path $Bindings "R1-X1-INCIDENT.json")
    Copy-Item -LiteralPath $Logs -Destination $PackagedLogs -Recurse

    if ((Sha256 (Join-Path $Stage "variance-pilot-raw.tar.gz")) -ne $RecordedRawSha) { Fail "COPIED_RAW_SHA256_MISMATCH" }
    if ((Sha256 (Join-Path $Bindings "SOURCE-ARMING-MANIFEST.json")) -ne $ExpectedSourceArming) { Fail "COPIED_SOURCE_ARMING_SHA256_MISMATCH" }
    if ((Sha256 (Join-Path $Bindings "R1-X1-INCIDENT.json")) -ne $IncidentSha) { Fail "COPIED_INCIDENT_SHA256_MISMATCH" }

    $ManifestPath = Join-Path $Stage "COLLECTION-MANIFEST.txt"
    @(
        "EVIDENCE_PACKAGE_SCHEMA=fehrest-r1-replacement-evidence-collector/3",
        "R1_V1_1_SEALED_COMMIT=$ExpectedHead",
        "R1_V1_1_PREREGISTRATION_DIGEST=$ExpectedV11Digest",
        "R1_X1_RUNNER_FILESET_SHA256=$ExpectedRunnerDigest",
        "R1_EXTERNAL_BUNDLE_SHA256=$ExpectedExternalBundle",
        "SOURCE_ARMING_MANIFEST_SHA256=$ExpectedSourceArming",
        "RANDOMIZATION_SEED=$ExpectedSeed",
        "MODEL=$ExpectedModel",
        "REASONING_EFFORT=medium",
        "TOTAL_SESSIONS=888",
        "RESULT_SHA256=" + (Sha256 (Join-Path $Stage "FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt")),
        "RAW_SHA256=$RecordedRawSha",
        "INCIDENT_SHA256=$IncidentSha",
        "REPLACEMENT_ARMING_MANIFEST_SHA256=" + (Sha256 (Join-Path $Bindings "REPLACEMENT-ARMING-MANIFEST.json")),
        "SOURCE_BATCH_DISPOSITION=INVALIDATED_DO_NOT_SCORE_DO_NOT_USE_FOR_VARIANCE",
        "SECRET_SCAN=PASS",
        "RAW_SEAL_STATUS=PASS",
        "RAW_SEAL_REPRODUCIBILITY=PASS",
        "SCORING_STATUS=NOT_STARTED",
        "UNBLINDING_STATUS=NOT_STARTED",
        "POWER_ANALYSIS_STATUS=NOT_PERFORMED",
        "CONFIRMATORY_STATUS=NOT_STARTED",
        "NEXT_GATE=FOUNDER_REVIEW_BEFORE_BLINDED_SCORING",
        "COLLECTOR_MUTATED_SOURCE_EVIDENCE=NO"
    ) | Set-Content -LiteralPath $ManifestPath -Encoding UTF8

    $Sums = Join-Path $Stage "PACKAGE-SHA256SUMS.txt"
    $RootFull = [System.IO.Path]::GetFullPath($Stage).TrimEnd('\') + '\'
    $Rows = @()
    foreach ($File in Get-ChildItem -LiteralPath $Stage -File -Recurse | Where-Object { $_.FullName -ne $Sums } | Sort-Object FullName) {
        $Relative = $File.FullName.Substring($RootFull.Length).Replace('\','/')
        $Rows += ((Sha256 $File.FullName) + "  " + $Relative)
    }
    $Rows | Set-Content -LiteralPath $Sums -Encoding ASCII

    $Stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $Zip = Join-Path $Desktop ("FEHREST-R1-X1-REPLACEMENT-EVIDENCE-V3-$Stamp.zip")
    if (Test-Path -LiteralPath $Zip) { Fail "OUTPUT_ZIP_ALREADY_EXISTS" }
    $Items = @(Get-ChildItem -LiteralPath $Stage | ForEach-Object { $_.FullName })
    Compress-Archive -LiteralPath $Items -DestinationPath $Zip -CompressionLevel Optimal
    Require-Leaf $Zip "OUTPUT_ZIP_NOT_CREATED"

    Write-Host "EVIDENCE_COLLECTION_STATUS=COMPLETE"
    Write-Host "COLLECTOR_SCHEMA=fehrest-r1-replacement-evidence-collector/3"
    Write-Host "RAW_SHA256=$RecordedRawSha"
    Write-Host "INCIDENT_SHA256=$IncidentSha"
    Write-Host "EVIDENCE_ZIP=$Zip"
    Write-Host ("EVIDENCE_ZIP_SHA256=" + (Sha256 $Zip))
    Write-Host "SOURCE_EVIDENCE_MUTATED=NO"
    Write-Host "NEXT_GATE=UPLOAD_EVIDENCE_ZIP_FOR_ISSUE_11_EXECUTION_REVIEW"
}
finally {
    if (Test-Path -LiteralPath $Stage) { Remove-Item -LiteralPath $Stage -Recurse -Force -ErrorAction SilentlyContinue }
}
