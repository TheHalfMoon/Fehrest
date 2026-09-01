$ErrorActionPreference = "Stop"

$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
$SupervisorSource = Join-Path $Here "supervisor.py"
$Repo = "C:\Users\Shehr\OneDrive\Desktop\Fehrest"
$Base = "$env:LOCALAPPDATA\Fehrest\R1-X1"
$RuntimeRoot = Join-Path $Base "replacement-runtime-v11"
$RuntimeVenv = Join-Path $RuntimeRoot "python-venv"
$SupervisorRuntime = Join-Path $RuntimeRoot "supervisor.py"

$Desktop = "C:\Users\Shehr\OneDrive\Desktop"
if (-not (Test-Path $Desktop)) { $Desktop = [Environment]::GetFolderPath("Desktop") }
$Result = Join-Path $Desktop "FEHREST-R1-X1-REPLACEMENT-PILOT-RESULT.txt"
$LauncherLog = Join-Path $Desktop "FEHREST-R1-X1-REPLACEMENT-LAUNCHER.txt"

function Log([string]$s) {
    Write-Host $s
    Add-Content -LiteralPath $LauncherLog -Value $s -Encoding UTF8
}

Set-Content -LiteralPath $LauncherLog -Value "=== FEHREST R1-X1 REPLACEMENT LAUNCHER V11 ===" -Encoding UTF8
Log "LAUNCHER_STARTED=YES"
Log "EXECUTOR_VERSION=11"
Log "SCORING_AUTHORIZED=NO"
Log "UNBLINDING_AUTHORIZED=NO"
Log "CONFIRMATORY_AUTHORIZED=NO"
Log "PACKAGE_DIR=$Here"

try {
    Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue

    if (-not (Test-Path $SupervisorSource)) {
        throw "FAIL_CLOSED: supervisor.py missing beside replacement.ps1"
    }
    if (-not (Test-Path $Repo)) {
        throw "FAIL_CLOSED: repository not found at $Repo"
    }

    $Runners = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object {
        $_.CommandLine -and
        $_.CommandLine -match 'r1_runner\.py' -and
        $_.CommandLine -match '\brun\b'
    })
    if ($Runners.Count -ne 0) {
        throw "FAIL_CLOSED: EXISTING_R1_RUNNER_PROCESS count=$($Runners.Count)"
    }
    Log "ACTIVE_R1_RUNNERS=0"

    $BasePy = "C:\Users\Shehr\AppData\Roaming\uv\python\cpython-3.11-windows-x86_64-none\python.exe"
    if (-not (Test-Path $BasePy)) {
        throw "FAIL_CLOSED: PYTHON_3_11_BASE_NOT_FOUND"
    }
    Log "PYTHON_BASE_FOUND=YES"

    New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null
    Copy-Item -LiteralPath $SupervisorSource -Destination $SupervisorRuntime -Force

    # Syntax check before any possible API call.
    $Syntax = Start-Process -FilePath $BasePy `
        -ArgumentList @("-m","py_compile",$SupervisorRuntime) `
        -WorkingDirectory $Repo `
        -PassThru -Wait
    if ($Syntax.ExitCode -ne 0) {
        throw "FAIL_CLOSED: SUPERVISOR_PYTHON_SYNTAX_CHECK_FAILED"
    }
    Log "SUPERVISOR_SYNTAX=PASS"

    # Prepare/incident declaration is no-API and must pass before credential capture.
    $PrepOut = Join-Path $RuntimeRoot "prepare-output.txt"
    $PrepErr = Join-Path $RuntimeRoot "prepare-error.txt"
    $Prep = Start-Process -FilePath $BasePy `
        -ArgumentList @($SupervisorRuntime, "prepare") `
        -WorkingDirectory $Repo `
        -RedirectStandardOutput $PrepOut `
        -RedirectStandardError $PrepErr `
        -PassThru -Wait

    if (Test-Path $PrepOut) {
        Get-Content $PrepOut | ForEach-Object { Log $_ }
    }
    if ($Prep.ExitCode -ne 0) {
        if (Test-Path $PrepErr) {
            Get-Content $PrepErr | ForEach-Object { Log $_ }
        }
        throw "FAIL_CLOSED: REPLACEMENT_PREPARE_FAILED exit=$($Prep.ExitCode)"
    }
    Log "NO_API_PREPARE_GATE=PASS"

    # V11 runtime bootstrap deliberately uses uv instead of `python -m venv`.
    # The exact Python base is a uv-managed CPython build; uv owns creation of the
    # isolated environment and installation of the pinned SDK. This changes only
    # launcher/runtime bootstrap, never sealed R1 experiment inputs or runner code.
    $UvExe = $null
    try {
        $UvCommand = Get-Command uv.exe -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($UvCommand) { $UvExe = $UvCommand.Source }
    } catch {}
    if (-not $UvExe) {
        $UvCandidates = @(
            (Join-Path $env:USERPROFILE ".local\bin\uv.exe"),
            (Join-Path $env:USERPROFILE ".cargo\bin\uv.exe"),
            (Join-Path $env:LOCALAPPDATA "Programs\uv\uv.exe")
        )
        foreach ($Candidate in $UvCandidates) {
            if (Test-Path -LiteralPath $Candidate -PathType Leaf) { $UvExe = $Candidate; break }
        }
    }
    if (-not $UvExe -or -not (Test-Path -LiteralPath $UvExe -PathType Leaf)) {
        throw "FAIL_CLOSED: UV_EXECUTABLE_NOT_FOUND"
    }
    Log "UV_EXECUTABLE_FOUND=YES"
    Log "UV_EXECUTABLE=$UvExe"

    $Py = Join-Path $RuntimeVenv "Scripts\python.exe"
    if (-not (Test-Path -LiteralPath $Py -PathType Leaf)) {
        Log "CREATING_ISOLATED_PYTHON_RUNTIME=YES"
        $VenvOut = Join-Path $RuntimeRoot "uv-venv-stdout.txt"
        $VenvErr = Join-Path $RuntimeRoot "uv-venv-stderr.txt"
        $VenvProc = Start-Process -FilePath $UvExe `
            -ArgumentList @("venv","--clear","--python",$BasePy,$RuntimeVenv) `
            -WorkingDirectory $Repo `
            -RedirectStandardOutput $VenvOut `
            -RedirectStandardError $VenvErr `
            -PassThru -Wait
        if (Test-Path $VenvOut) { Get-Content -LiteralPath $VenvOut | ForEach-Object { Log ("UV_VENV_STDOUT=" + $_) } }
        if (Test-Path $VenvErr) { Get-Content -LiteralPath $VenvErr | ForEach-Object { Log ("UV_VENV_STDERR=" + $_) } }
        if ($VenvProc.ExitCode -ne 0) {
            throw "FAIL_CLOSED: UV_VENV_CREATION_FAILED exit=$($VenvProc.ExitCode)"
        }
    }
    if (-not (Test-Path -LiteralPath $Py -PathType Leaf)) {
        throw "FAIL_CLOSED: ISOLATED_PYTHON_NOT_CREATED"
    }
    Log "ISOLATED_PYTHON_RUNTIME=READY"

    # V11 avoids PowerShell Start-Process -ArgumentList quoting for Python -c.
    # A tiny runtime-local probe file is written with UTF-8 without BOM and then
    # executed as a normal script path. This changes only SDK verification plumbing.
    $SdkProbe = Join-Path $RuntimeRoot "verify-openai-sdk.py"
    $Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($SdkProbe, "import openai`nprint(openai.__version__)`n", $Utf8NoBom)
    Log "SDK_VERIFY_PROBE_FILE=READY"

    $SdkCheckOut = Join-Path $RuntimeRoot "sdk-check-stdout.txt"
    $SdkCheckErr = Join-Path $RuntimeRoot "sdk-check-stderr.txt"
    $SdkCheck = Start-Process -FilePath $Py `
        -ArgumentList @($SdkProbe) `
        -WorkingDirectory $Repo `
        -RedirectStandardOutput $SdkCheckOut `
        -RedirectStandardError $SdkCheckErr `
        -PassThru -Wait
    $Sdk = ""
    if ($SdkCheck.ExitCode -eq 0 -and (Test-Path $SdkCheckOut)) {
        $Sdk = ((Get-Content -LiteralPath $SdkCheckOut -Raw).Trim())
    }
    if ($Sdk -ne "3.3.0") {
        Log "INSTALLING_PINNED_OPENAI_SDK=3.3.0"
        $InstallOut = Join-Path $RuntimeRoot "uv-pip-stdout.txt"
        $InstallErr = Join-Path $RuntimeRoot "uv-pip-stderr.txt"
        $Install = Start-Process -FilePath $UvExe `
            -ArgumentList @("pip","install","--python",$Py,"openai==3.3.0") `
            -WorkingDirectory $Repo `
            -RedirectStandardOutput $InstallOut `
            -RedirectStandardError $InstallErr `
            -PassThru -Wait
        if (Test-Path $InstallOut) { Get-Content -LiteralPath $InstallOut | ForEach-Object { Log ("UV_PIP_STDOUT=" + $_) } }
        if (Test-Path $InstallErr) { Get-Content -LiteralPath $InstallErr | ForEach-Object { Log ("UV_PIP_STDERR=" + $_) } }
        if ($Install.ExitCode -ne 0) {
            throw "FAIL_CLOSED: OPENAI_SDK_INSTALL_FAILED exit=$($Install.ExitCode)"
        }
    }

    $VerifyOut = Join-Path $RuntimeRoot "sdk-verify-stdout.txt"
    $VerifyErr = Join-Path $RuntimeRoot "sdk-verify-stderr.txt"
    $Verify = Start-Process -FilePath $Py `
        -ArgumentList @($SdkProbe) `
        -WorkingDirectory $Repo `
        -RedirectStandardOutput $VerifyOut `
        -RedirectStandardError $VerifyErr `
        -PassThru -Wait
    if ($Verify.ExitCode -ne 0) {
        if (Test-Path $VerifyErr) { Get-Content -LiteralPath $VerifyErr | ForEach-Object { Log ("SDK_VERIFY_STDERR=" + $_) } }
        throw "FAIL_CLOSED: OPENAI_SDK_IMPORT_FAILED exit=$($Verify.ExitCode)"
    }
    $Sdk = ((Get-Content -LiteralPath $VerifyOut -Raw).Trim())
    if ($Sdk -ne "3.3.0") {
        throw "FAIL_CLOSED: OPENAI_SDK_VERSION_MISMATCH observed=$Sdk"
    }
    Log "OPENAI_SDK_VERSION=$Sdk"
    Log "REPLACEMENT_MODEL_CALLS_EXECUTED=0"
    Log "WAITING_FOR_REPLACEMENT_PILOT_API_KEY=YES"
    Log "ACTION=CLICK_COPY_ON_SECURE_OPENAI_KEY_WIDGET_ONLY"
    Log "DO_NOT_TYPE_OR_PASTE_THE_KEY_HERE"

    $Deadline = (Get-Date).AddMinutes(3)
    $Key = $null
    while ((Get-Date) -lt $Deadline) {
        try {
            $Clip = Get-Clipboard -Raw -ErrorAction SilentlyContinue
            if ($Clip) {
                $Candidate = $Clip.Trim()
                if ($Candidate -match '^sk-' -and
                    $Candidate -notmatch '\*' -and
                    $Candidate -notmatch '\s' -and
                    $Candidate.Length -ge 40) {
                    $Key = $Candidate
                    break
                }
            }
        } catch {}
        Start-Sleep -Milliseconds 400
    }
    if (-not $Key) {
        throw "FAIL_CLOSED: NO_VALID_API_KEY_CAPTURED_WITHIN_3_MINUTES"
    }

    $env:OPENAI_API_KEY = $Key
    $Key = $null
    try { Set-Clipboard -Value "FEHREST_API_KEY_CAPTURED_REDACTED" } catch {}
    Log "API_KEY_CAPTURED_FROM_CLIPBOARD=YES"
    Log "API_KEY_VALUE=REDACTED"
    Log "REPLACEMENT_PILOT_EXECUTION_STARTING=YES"

    try {
        $Proc = Start-Process -FilePath $Py `
            -ArgumentList @($SupervisorRuntime, "run") `
            -WorkingDirectory $Repo `
            -PassThru -Wait
        $Rc = $Proc.ExitCode
    } finally {
        Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
    }

    Log "REPLACEMENT_SUPERVISOR_EXIT_CODE=$Rc"
    Log "OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES"
    Log "RESULT_FILE=$Result"

    if (Test-Path $Result) {
        Get-Content -LiteralPath $Result | ForEach-Object { Log $_ }
        try { Start-Process notepad.exe -ArgumentList "`"$Result`"" } catch {}
    } else {
        Log "RESULT_FILE_MISSING=YES"
    }
    exit $Rc
}
catch {
    Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
    Log "LAUNCHER_STATUS=FAIL"
    Log ("FAILURE_TYPE=" + $_.Exception.GetType().FullName)
    Log ("FAILURE_REASON=" + $_.Exception.Message)
    if ($_.ScriptStackTrace) { Log ("FAILURE_SCRIPT_STACK=" + ($_.ScriptStackTrace -replace "`r?`n", " | ")) }
    Log "OPENAI_API_KEY_CLEARED_FROM_POWERSHELL=YES"
    Log "MODEL_CALLS_STARTED_AFTER_FAILURE=NO"
    Log "LAUNCHER_LOG=$LauncherLog"
    try { Start-Process notepad.exe -ArgumentList "`"$LauncherLog`"" } catch {}
    exit 1
}
