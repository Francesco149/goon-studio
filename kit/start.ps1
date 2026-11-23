# start.ps1 - start ComfyUI (hidden) if needed, start the Goon Studio page, open the browser.
#
#   powershell -ExecutionPolicy Bypass -File kit\start.ps1
#   ... -NoBrowser   do not open the browser
#   ... -Stop        stop the Studio page and the engine started from this kit
#   ... -RestartEngine  kill and restart only ComfyUI
#
# Settings live in my\settings.json:
#   { "comfy_url": "http://127.0.0.1:8188",
#     "engine_dir": "D:\\GoonStudio\\ComfyUI_windows_portable",  # ComfyUI folder with python_embeded
#     "models_dir": "D:\\GoonStudio\\models",   # every model file (tools/models/store.py wire)
#     "data_dir": "C:\\Users\\you\\Documents\\goon-studio\\gallery",
#     "extra_flags": "" }
param([switch]$NoBrowser, [switch]$Stop, [switch]$RestartEngine)
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$SettingsPath = Join-Path $Repo "my\settings.json"
if (-not (Test-Path $SettingsPath)) {
    Write-Host "No my\settings.json yet: copy my\settings.example.json and fill in engine_dir." -ForegroundColor Red
    exit 2
}
$S = Get-Content $SettingsPath -Raw | ConvertFrom-Json
$Engine = $S.engine_dir
$Py = if ($S.python) { $S.python } else { Join-Path $Engine "python_embeded\python.exe" }
$Data = if ($S.data_dir) { $S.data_dir } else { Join-Path $Repo "gallery" }
$Logs = Join-Path $Data "logs"
New-Item -ItemType Directory -Force $Logs | Out-Null

function Up($url) {
    try { Invoke-WebRequest -UseBasicParsing -TimeoutSec 3 $url | Out-Null; return $true } catch { return $false }
}

function Q($list) {
    return @($list | ForEach-Object { if ("$_" -match '\s') { '"' + $_ + '"' } else { "$_" } })
}

function Launch($exe, $arglist, $wd, $out, $err) {
    # detached (WMI): not a child of this shell, survives the agent's command ending
    $line = 'cmd.exe /s /c ""' + $exe + '" ' + ((Q $arglist) -join " ") + ' 1>"' + $out + '" 2>"' + $err + '""'
    $si = New-CimInstance -ClassName Win32_ProcessStartup -ClientOnly -Property @{ ShowWindow = [uint16]0 }
    $r = Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{ CommandLine = $line; CurrentDirectory = $wd; ProcessStartupInformation = $si }
    if ($r.ReturnValue -ne 0) { throw ("could not start " + $exe + " (WMI error " + $r.ReturnValue + ")") }
}

function Stop-Ours {
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
        Where-Object { $_.ExecutablePath -eq $Py } |
        ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    Start-Sleep -Seconds 2
}

if ($Stop) { Stop-Ours; Write-Host "stopped"; exit 0 }
if ($RestartEngine) {
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
        Where-Object { $_.ExecutablePath -eq $Py -and $_.CommandLine -like "*main.py*" -and $_.CommandLine -notlike "*--port 8189*" } |
        ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    $t0 = Get-Date
    while ((Up "http://127.0.0.1:8188/system_stats") -and ((Get-Date) - $t0).TotalSeconds -lt 15) { Start-Sleep -Milliseconds 300 }
}

# The engine is always the ComfyUI on this PC (127.0.0.1; the port from comfy_url, default 8188).
$Url = "http://127.0.0.1:8188"
if ("$($S.comfy_url)" -match '^https?://(127\.0\.0\.1|localhost)(:\d+)?/?$') { $Url = "$($S.comfy_url)".TrimEnd("/") }
$Port = if ($Url -match ':(\d+)$') { $Matches[1] } else { "8188" }

if (-not (Up "$Url/system_stats")) {
    # an engine that holds the port but does not answer (hung, or still loading after a crash) blocks
    # a new one: give it 20 s, then stop that process only (not every python.exe)
    $hold = Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($hold) {
        Write-Host "port $Port is taken by a process that does not answer; waiting 20 s ..."
        $t0 = Get-Date
        while (-not (Up "$Url/system_stats") -and ((Get-Date) - $t0).TotalSeconds -lt 20) { Start-Sleep -Seconds 2 }
        if (-not (Up "$Url/system_stats")) {
            $p = Get-CimInstance Win32_Process -Filter "ProcessId = $($hold.OwningProcess)"
            if ($p -and $p.Name -eq "python.exe" -and $p.CommandLine -like "*main.py*") {
                Write-Host "stopping the stuck engine (pid $($p.ProcessId))" -ForegroundColor Yellow
                Stop-Process -Id $p.ProcessId -Force; Start-Sleep -Seconds 2
            } else {
                Write-Host "port $Port is used by $($p.Name) (pid $($hold.OwningProcess)), not a ComfyUI: close it or change comfy_url" -ForegroundColor Red
                exit 3
            }
        }
    }
}

if (-not (Up "$Url/system_stats")) {
    if (-not (Test-Path $Py)) { Write-Host "python not found: $Py (set engine_dir or python in my\settings.json)" -ForegroundColor Red; exit 2 }
    $cargs = @("-s", "ComfyUI\main.py", "--windows-standalone-build", "--listen", "127.0.0.1", "--port", $Port,
               "--output-directory", (Join-Path $Data "outputs"), "--input-directory", (Join-Path $Data "inputs"),
               "--disable-auto-launch", "--preview-method", "none")
    # extra_flags is one string in settings.json; split it so ComfyUI gets separate arguments
    # (passed whole, Q() quotes it and argparse rejects "--use-ck-attention --fast ...").
    if ($S.extra_flags) { $cargs += @("$($S.extra_flags)".Trim() -split '\s+') }
    Write-Host "starting ComfyUI ..."
    Launch $Py $cargs $Engine (Join-Path $Logs "comfyui.log") (Join-Path $Logs "comfyui.err.log")
    $t0 = Get-Date
    while (-not (Up "$Url/system_stats")) {
        if (((Get-Date) - $t0).TotalSeconds -gt 240) {
            Write-Host "ComfyUI did not start in 4 minutes. Last lines of gallery\logs\comfyui.err.log:" -ForegroundColor Red
            Get-Content (Join-Path $Logs "comfyui.err.log") -Tail 15 -ErrorAction SilentlyContinue
            exit 3
        }
        Start-Sleep -Seconds 2
    }
}
# the page is started through WMI and does not inherit this shell's environment: pass the engine on
# its command line. A page left running from an earlier start that cannot reach the engine is
# restarted so it picks up this one.
function Page-Up { try { return (Invoke-RestMethod -TimeoutSec 3 "http://127.0.0.1:8191/api/state") } catch { return $null } }
$st = Page-Up
if ($st -and -not $st.comfy_up -and (Up "$Url/system_stats")) {
    Write-Host "the running page talks to an engine that is gone: restarting the page"
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
        Where-Object { $_.CommandLine -like "*kit\studio\server.py*" -and $_.CommandLine -notlike "*8291*" } |
        ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    Start-Sleep -Seconds 1
    $st = $null
}
if (-not $st) {
    $server = Join-Path $Repo "kit\studio\server.py"
    Write-Host "starting the Studio page ..."
    Launch $Py @($server, "--engine", $Url, "--port", "8191") (Join-Path $Repo "kit\studio") (Join-Path $Logs "studio.log") (Join-Path $Logs "studio.err.log")
    $t0 = Get-Date
    while (-not (Up "http://127.0.0.1:8191/api/state")) {
        if (((Get-Date) - $t0).TotalSeconds -gt 30) { Write-Host "the page did not start; see gallery\logs\studio.err.log" -ForegroundColor Red; exit 4 }
        Start-Sleep -Milliseconds 400
    }
}
Write-Host "Goon Studio: http://127.0.0.1:8191  (engine $Url)"
if (-not $NoBrowser) { Start-Process "http://127.0.0.1:8191" }
