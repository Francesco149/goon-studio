# bench_engine.ps1 - start/stop a private ComfyUI on :8189 for the 8 GB optimization pass.
# Leaves the user's engine on :8187 (and Love Live Studio's on :8188) alone. All paths are explicit so nothing in my/settings.json
# changes.
#
#   powershell -File tools\experiments\bench_engine.ps1 -Action start
#   powershell -File tools\experiments\bench_engine.ps1 -Action start -Flags "--fast-disk --use-ck-attention"
#   powershell -File tools\experiments\bench_engine.ps1 -Action stop
#   powershell -File tools\experiments\bench_engine.ps1 -Action status
param(
    [ValidateSet("start", "stop", "status", "restart")]
    [string]$Action = "start",
    [string]$Flags = "",
    [int]$Port = 8189
)
$ErrorActionPreference = "Stop"
# The engine folder comes from my\settings.json (engine_dir); bench files go to <data_dir>\bench.
$Repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$S = Get-Content (Join-Path $Repo "my\settings.json") -Raw | ConvertFrom-Json
$Engine = $S.engine_dir
$Py = if ($S.python) { $S.python } else { Join-Path $Engine "python_embeded\python.exe" }
$Data = Join-Path $(if ($S.data_dir) { $S.data_dir } else { Join-Path $Repo "gallery" }) "bench"
New-Item -ItemType Directory -Force $Data | Out-Null
$Log = Join-Path $Data "comfyui-bench.log"
$Err = Join-Path $Data "comfyui-bench.err.log"
$PidFile = Join-Path $Data "comfyui-bench.pid"
$Url = "http://127.0.0.1:$Port"

function Up { try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 "$Url/system_stats" | Out-Null; $true } catch { $false } }
function OurProcess {
    if (Test-Path $PidFile) {
        $old = Get-Content $PidFile -ErrorAction SilentlyContinue
        if ($old) { Get-CimInstance Win32_Process -Filter "ProcessId = $old" -ErrorAction SilentlyContinue }
    }
}

if ($Action -eq "stop" -or $Action -eq "restart") {
    $p = OurProcess
    if ($p) { Write-Host "stopping bench engine $($p.ProcessId)"; Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue }
    Remove-Item $PidFile -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    if ($Action -eq "stop") { Write-Host "stopped"; exit 0 }
}

if ($Action -eq "status") {
    if (Up) { Write-Host "bench engine up on $Url"; (Invoke-RestMethod "$Url/system_stats").system.argv } else { Write-Host "bench engine down" }
    exit 0
}

if (Up) { Write-Host "bench engine already up on $Url (stop it first to change flags)"; exit 0 }

New-Item -ItemType Directory -Force "$Data\outputs", "$Data\inputs" | Out-Null
$args = @("-s", "ComfyUI\main.py", "--windows-standalone-build", "--listen", "127.0.0.1", "--port", "$Port",
          "--output-directory", "$Data\outputs", "--input-directory", "$Data\inputs",
          "--disable-auto-launch", "--preview-method", "none", "--disable-assets")
if ($Flags.Trim()) { $args += $Flags.Trim() -split '\s+' }
Write-Host "starting bench engine: $Py $($args -join ' ')"
$p = Start-Process -FilePath $Py -ArgumentList $args -WorkingDirectory $Engine -PassThru `
    -RedirectStandardOutput $Log -RedirectStandardError $Err -WindowStyle Hidden
Set-Content -Path $PidFile -Value $p.Id
$t0 = Get-Date
while (-not (Up)) {
    if ($p.HasExited) { Write-Host "engine exited $($p.ExitCode); tail:"; Get-Content $Err -Tail 30; exit 1 }
    if (((Get-Date) - $t0).TotalSeconds -gt 240) { Write-Host "engine did not start; tail:"; Get-Content $Err -Tail 30; exit 1 }
    Start-Sleep -Seconds 2
}
Write-Host "bench engine up on $Url (pid $($p.Id))"
