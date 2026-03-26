param(
    [string]$LogDirectory = ".publish_logs"
)

$repoRoot = $PSScriptRoot
$publisherScript = Join-Path $repoRoot "daily_github_pusher.py"
$logRoot = Join-Path $repoRoot $LogDirectory

if (-not (Test-Path $publisherScript)) {
    throw "Publisher script not found at $publisherScript"
}

New-Item -ItemType Directory -Force -Path $logRoot | Out-Null

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logFile = Join-Path $logRoot "publish_$timestamp.log"

$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
$python = Get-Command python -ErrorAction SilentlyContinue

Push-Location $repoRoot
try {
    if ($pyLauncher) {
        & $pyLauncher.Source -3 $publisherScript *>&1 | Tee-Object -FilePath $logFile
        exit $LASTEXITCODE
    }

    if ($python) {
        & $python.Source $publisherScript *>&1 | Tee-Object -FilePath $logFile
        exit $LASTEXITCODE
    }

    throw "Neither py nor python was found in PATH."
}
finally {
    Pop-Location
}
