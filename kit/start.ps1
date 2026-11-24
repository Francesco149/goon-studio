# start.ps1 - start ComfyUI (hidden) if needed, start the Goon Studio page, open the browser.
#
#   powershell -ExecutionPolicy Bypass -File kit\start.ps1
#   ... -NoBrowser   do not open the browser
#   ... -Stop        stop this Studio's page and engine (not Love Live Studio's, not the bench engine)
#   ... -RestartEngine  kill and restart only this Studio's ComfyUI
#   ... -Restart     stop and start this Studio's engine and page again
#   ... -StopOther   another app's engine is running: stop it without asking
#   ... -KeepOther   another app's engine is running: leave it and start ours anyway
#
# Goon Studio's engine is 127.0.0.1:8187 (Love Live Studio keeps 8188, its page 8190). Both studios can
# share one ComfyUI folder, but one 8 GB GPU / 16 GB RAM holds one engine at a time, and an engine
# writes pictures into the outputs of the app that started it - so when another app's engine runs,
# the launcher asks whether to stop it (exit 5 without asking when nobody can answer, e.g. an agent:
# ask the user, then rerun with -StopOther or -KeepOther).
#
# Settings live in my\settings.json:
#   { "comfy_url": "http://127.0.0.1:8187",
#     "engine_dir": "D:\\GoonStudio\\ComfyUI_windows_portable",  # ComfyUI folder with python_embeded
#     "models_dir": "D:\\GoonStudio\\models",   # every model file (tools/models/store.py wire)
#     "data_dir": "C:\\Users\\you\\Documents\\goon-studio\\gallery",
#     "extra_flags": "" }
param([switch]$NoBrowser, [switch]$Stop, [switch]$Restart, [switch]$RestartEngine, [switch]$StopOther, [switch]$KeepOther)
$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$SettingsPath = Join-Path $Repo "my\settings.json"
if (-not (Test-Path $SettingsPath)) {
    Write-Host "No my\settings.json yet: copy my\settings.example.json and fill in engine_dir." -ForegroundColor Red
    exit 2
}
$S = Get-Content $SettingsPath -Raw | ConvertFrom-Json
if ("$($S.comfy_url)".TrimEnd("/") -in @("http://127.0.0.1:8188", "http://localhost:8188")) {
    # installs from before the split used 8188, which is Love Live Studio's engine port: move to 8187
    $raw = Get-Content $SettingsPath -Raw
    $raw = $raw -replace '"comfy_url"\s*:\s*"http://(127\.0\.0\.1|localhost):8188/?"', '"comfy_url": "http://127.0.0.1:8187"'
    [IO.File]::WriteAllText($SettingsPath, $raw, (New-Object Text.UTF8Encoding($false)))
    $S = $raw | ConvertFrom-Json
    Write-Host "moved this Studio's engine to port 8187 (8188 is Love Live Studio's)"
}
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

# The engine is always the ComfyUI on this PC (127.0.0.1; the port from comfy_url, default 8187).
$Url = "http://127.0.0.1:8187"
if ("$($S.comfy_url)" -match '^https?://(127\.0\.0\.1|localhost)(:\d+)?/?$') { $Url = "$($S.comfy_url)".TrimEnd("/") }
$Port = if ($Url -match ':(\d+)$') { $Matches[1] } else { "8187" }
$Outputs = Join-Path $Data "outputs"

function Ask-YesNo($text, $title) {
    # a real dialog on top of everything: the desktop shortcut's console window may be minimized
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $owner = New-Object System.Windows.Forms.Form -Property @{ TopMost = $true }
        $r = [System.Windows.Forms.MessageBox]::Show($owner, $text, $title, "YesNo", "Question")
        $owner.Dispose()
        return ($r -eq "Yes")
    } catch {
        return -not ((Read-Host ($text + " [Y/n]")) -match '^\s*n')
    }
}

function Engines {
    # every ComfyUI on this PC: pid, port, output folder, and whether it is ours. Both studios may run
    # the same python.exe (one shared ComfyUI folder), so ownership is by output folder, not by exe.
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Where-Object { $_.CommandLine -like "*main.py*" } | ForEach-Object {
        $cl = $_.CommandLine
        $p = if ($cl -match '--port\s+"?(\d+)') { $Matches[1] } else { "8188" }
        $o = if ($cl -match '--output-directory\s+("([^"]+)"|(\S+))') { if ($Matches[2]) { $Matches[2] } else { $Matches[3] } } else { "" }
        $mine = $o -and ([IO.Path]::GetFullPath($o).TrimEnd([char]92) -eq [IO.Path]::GetFullPath($Outputs).TrimEnd([char]92))
        [pscustomobject]@{ Pid = $_.ProcessId; Port = $p; Outputs = $o; Mine = [bool]$mine; Bench = ($p -eq "8189") }
    }
}

function Stop-Ours {
    # this Studio's engine (its port, or ours on an old port) and its page; never another app's, never the bench
    Engines | Where-Object { $_.Mine -and -not $_.Bench } | ForEach-Object { try { Stop-Process -Id $_.Pid -Force } catch {} }
    $server = Join-Path $Repo "kit\studio\server.py"
    Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
        Where-Object { $_.CommandLine -like "*$server*" -and $_.CommandLine -notlike "*8291*" } |
        ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    Start-Sleep -Seconds 2
}

if ($Stop -or $Restart) { Stop-Ours; if ($Stop) { Write-Host "stopped"; exit 0 } }
if ($RestartEngine) {
    Engines | Where-Object { $_.Mine -and -not $_.Bench } | ForEach-Object { try { Stop-Process -Id $_.Pid -Force } catch {} }
    $t0 = Get-Date
    while ((Up "$Url/system_stats") -and ((Get-Date) - $t0).TotalSeconds -lt 15) { Start-Sleep -Milliseconds 300 }
}

# Another app's engine (Love Live Studio) holds the GPU and RAM, or sits on our port and would send our
# pictures into its own outputs. Our own engine left on an old port is restarted on the right one.
$all = @(Engines)
$all | Where-Object { $_.Mine -and -not $_.Bench -and $_.Port -ne $Port } | ForEach-Object {
    Write-Host "this Studio's engine is still on the old port $($_.Port): moving it to $Port"
    try { Stop-Process -Id $_.Pid -Force } catch {}
    Start-Sleep -Seconds 2
}
$others = @($all | Where-Object { -not $_.Mine -and -not $_.Bench })
if ($RestartEngine -and -not $StopOther) { $others = @($others | Where-Object { $_.Port -eq $Port }) }
if ($others.Count) {
    foreach ($e in $others) {
        Write-Host ("another app's ComfyUI engine is running: port {0}, pictures to {1} (pid {2})" -f $e.Port, $(if ($e.Outputs) { $e.Outputs } else { "its default folder" }), $e.Pid) -ForegroundColor Yellow
    }
    $onOurPort = @($others | Where-Object { $_.Port -eq $Port }).Count -gt 0
    $kill = $StopOther
    if (-not $StopOther -and -not $KeepOther) {
        if ([Console]::IsInputRedirected) {
            Write-Host "Ask the user whether to stop it (it ends that app's running jobs), then rerun with -StopOther or -KeepOther." -ForegroundColor Yellow
            exit 5
        }
        $kill = Ask-YesNo ("Another app's image engine is running (for example Love Live Studio).`n`n" +
                           "Both at once can run out of memory on one graphics card. Stop it?`n" +
                           "(Anything it is making right now stops too.)") "Goon Studio"
    }
    if ($kill) {
        foreach ($e in $others) { Write-Host "stopping pid $($e.Pid)"; try { Stop-Process -Id $e.Pid -Force } catch {} }
        Start-Sleep -Seconds 2
    } elseif ($onOurPort) {
        Write-Host "port $Port is held by another app's engine: change comfy_url in my\settings.json or stop it" -ForegroundColor Red
        exit 3
    }
}

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
    # the engine folder may be shared with Love Live Studio, whose setup rewrites extra_model_paths.yaml:
    # put this Studio's models back in before starting
    $yaml = Join-Path $Engine "ComfyUI\extra_model_paths.yaml"
    if ($S.models_dir -and -not ((Test-Path $yaml) -and (Select-String -Path $yaml -Pattern '^goon_studio:' -Quiet))) {
        Write-Host "connecting the engine to this Studio's models folder"
        & $Py -s (Join-Path $Repo "tools\models\store.py") wire | Out-Null
    }
    $cargs = @("-s", "ComfyUI\main.py", "--windows-standalone-build", "--listen", "127.0.0.1", "--port", $Port,
               "--output-directory", $Outputs, "--input-directory", (Join-Path $Data "inputs"),
               "--disable-auto-launch", "--preview-method", "none",
               # its own database: two engines started from one ComfyUI folder (Love Live Studio's) would
               # otherwise fight over ComfyUI\user\comfyui.db and the second one would not start
               "--database-url", ("sqlite:///" + ((Join-Path $Data "engine.db") -replace '\\', '/')))
    # extra_flags is one string in settings.json; split it so ComfyUI gets separate arguments
    # (passed whole, Q() quotes it and argparse rejects "--use-ck-attention --fast ...").
    if ($S.extra_flags) { $cargs += @("$($S.extra_flags)".Trim() -split '\s+') }
    Write-Host "starting ComfyUI ..."
    Launch $Py $cargs $Engine (Join-Path $Logs "comfyui.log") (Join-Path $Logs "comfyui.err.log")
    $t0 = Get-Date
    while (-not (Up "$Url/system_stats")) {
        if (((Get-Date) - $t0).TotalSeconds -gt 240) {
            Write-Host "ComfyUI did not start in 4 minutes. Last lines of $Logs\comfyui.err.log:" -ForegroundColor Red
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
$server = Join-Path $Repo "kit\studio\server.py"
$page = @(Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" |
    Where-Object { $_.CommandLine -like "*$server*" -and $_.CommandLine -notlike "*8291*" })
# restart a page left running from an earlier start that cannot reach the engine, or that was started
# for another engine (e.g. the old port 8188, which is Love Live Studio's)
$stale = $page | Where-Object { $_.CommandLine -notlike "*--engine $Url*" }
if ($st -and (($stale -and $page) -or (-not $st.comfy_up -and (Up "$Url/system_stats")))) {
    Write-Host "the running page talks to another engine: restarting the page"
    $page | ForEach-Object { try { Stop-Process -Id $_.ProcessId -Force } catch {} }
    Start-Sleep -Seconds 1
    $st = $null
}
if (-not $st) {
    Write-Host "starting the Studio page ..."
    Launch $Py @($server, "--engine", $Url, "--port", "8191") (Join-Path $Repo "kit\studio") (Join-Path $Logs "studio.log") (Join-Path $Logs "studio.err.log")
    $t0 = Get-Date
    while (-not (Up "http://127.0.0.1:8191/api/state")) {
        if (((Get-Date) - $t0).TotalSeconds -gt 30) { Write-Host "the page did not start; see $Logs\studio.err.log" -ForegroundColor Red; exit 4 }
        Start-Sleep -Milliseconds 400
    }
}
Write-Host "Goon Studio: http://127.0.0.1:8191  (engine $Url)"
if (-not $NoBrowser) { Start-Process "http://127.0.0.1:8191" }
