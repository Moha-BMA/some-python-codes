param(
    [int]$CheckIntervalMinutes = 60
)

$mutexCreated = $false
$mutex = New-Object System.Threading.Mutex($true, "Local\\SomePythonCodesDailyPublishWatcher", [ref]$mutexCreated)

if (-not $mutexCreated) {
    Write-Host "The daily publish watcher is already running."
    exit 0
}

$repoRoot = $PSScriptRoot
$runnerScript = Join-Path $repoRoot "run_daily_publish.ps1"

if (-not (Test-Path $runnerScript)) {
    $mutex.ReleaseMutex()
    $mutex.Dispose()
    throw "Runner script not found at $runnerScript"
}

$lastAttemptDate = ""

try {
    while ($true) {
        $today = Get-Date -Format "yyyy-MM-dd"

        if ($today -ne $lastAttemptDate) {
            & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $runnerScript
            $lastAttemptDate = $today
        }

        Start-Sleep -Seconds ($CheckIntervalMinutes * 60)
    }
}
finally {
    $mutex.ReleaseMutex()
    $mutex.Dispose()
}
