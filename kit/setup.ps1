# setup.ps1 - installs Goon Studio's engine on this PC and writes my\settings.json. Safe to run again.
#
#   powershell -ExecutionPolicy Bypass -File kit\setup.ps1 -Check                 # GPU, driver, RAM, drives only
#   powershell -ExecutionPolicy Bypass -File kit\setup.ps1 -DataDir "D:\GoonStudio"
#   ... -EngineDir <ComfyUI_windows_portable>   use this engine folder (default: Love Live Studio's, if it is
#                                               installed next to this repo; else the pinned build is installed)
#   ... -GalleryDir <folder>   where pictures go (default: the repo's gallery\ folder)
#   ... -NoShortcut  -NoStart  -StopOther / -KeepOther (passed to start.ps1: another app's engine is running)
#
# Big files live in -DataDir: downloads\, engine\ (unless shared), models\ (the model store). Models are fetched
# afterwards, template by template: kit\py.cmd tools\models\store.py fetch <template> (AGENTS.md section 1a).
# Exit codes: 0 ok, 10 driver too old, 11 no data folder / not enough space, 12 no NVIDIA GPU, 13 download or unpack
# failed, 14 the engine did not start, 5 another app's engine is running (ask the user, rerun with -StopOther/-KeepOther).
param([string]$DataDir, [string]$EngineDir, [string]$GalleryDir, [switch]$Check, [switch]$NoShortcut, [switch]$NoStart,
      [switch]$StopOther, [switch]$KeepOther)
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$Repo = Split-Path -Parent $PSScriptRoot
$My = Join-Path $Repo "my"
$SettingsPath = Join-Path $My "settings.json"
$Pin = Get-Content (Join-Path $PSScriptRoot "engine.json") -Raw | ConvertFrom-Json
New-Item -ItemType Directory -Force $My | Out-Null
try { Start-Transcript -Path (Join-Path $My "setup.log") -Append | Out-Null } catch {}

function Say($m) { Write-Host ("[setup] " + $m) }
function Fail($code, $m) { Write-Host ("[setup] PROBLEM: " + $m) -ForegroundColor Red; exit $code }
function Run-Native {
    $old = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    try { & $args[0] @($args | Select-Object -Skip 1) } finally { $ErrorActionPreference = $old }
}
function Download($url, $dest, $size, $sha) {
    New-Item -ItemType Directory -Force (Split-Path -Parent $dest) | Out-Null
    $okFile = $dest + ".ok"
    if ((Test-Path $dest) -and (Test-Path $okFile)) { Say ("ok (already verified): " + (Split-Path -Leaf $dest)); return }
    for ($try = 1; $try -le 3; $try++) {
        if (-not (Test-Path $dest) -or (Get-Item $dest).Length -lt $size) {
            Say ("downloading {0} ({1:n1} GB) ..." -f (Split-Path -Leaf $dest), ($size / 1GB))
            Run-Native curl.exe -L --fail --retry 5 --retry-delay 5 -C - -o $dest $url
            if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne 33) { Say "download interrupted, retrying"; continue }
        }
        if ((Get-Item $dest).Length -ne $size) { Say "wrong size: starting this file again"; Remove-Item $dest -Force; continue }
        Say ("checking " + (Split-Path -Leaf $dest) + " ...")
        if ((Get-FileHash -Algorithm SHA256 $dest).Hash.ToLower() -ne $sha) { Say "checksum mismatch: starting again"; Remove-Item $dest -Force; continue }
        Set-Content -Path $okFile -Value "ok" -Encoding ASCII
        return
    }
    Fail 13 ("could not download " + $url)
}

# ---------------------------------------------------------------- 1. the machine
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 1)
$gpu = $null; $vram = $null; $driver = $null; $cc = $null
$smi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if (-not $smi -and (Test-Path "C:\Windows\System32\nvidia-smi.exe")) { $smi = "C:\Windows\System32\nvidia-smi.exe" }
if ($smi) {
    $line = & $smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader,nounits 2>$null | Select-Object -First 1
    if ($line) { $f = $line.Split(",") | ForEach-Object { $_.Trim() }; $gpu = $f[0]; $vram = [math]::Round([double]$f[1] / 1024, 1); $driver = $f[2]; $cc = $f[3] }
}
Say ("GPU: {0} | VRAM: {1} GB | driver {2} | compute {3} | RAM: {4} GB" -f $gpu, $vram, $driver, $cc, $ram)
foreach ($v in (Get-Volume | Where-Object { $_.DriveLetter -and $_.DriveType -eq "Fixed" -and $_.Size -gt 0 })) {
    Say ("drive {0}: {1} GB free of {2} GB" -f $v.DriveLetter, [math]::Round($v.SizeRemaining / 1GB), [math]::Round($v.Size / 1GB))
}
if (-not $gpu) { Fail 12 "no NVIDIA graphics card found (or its driver is missing). Goon Studio needs an NVIDIA GPU with 8 GB." }
$Build = if ($cc -and [double]$cc -lt 7.5) { "pascal" } else { "modern" }
$B = $Pin.engine.builds.$Build
Say ("engine build: {0} ({1})" -f $Build, $B.for)
if ($driver -and [double]$driver -lt [double]$B.min_driver) {
    Fail 10 ("the NVIDIA driver {0} is too old; this needs {1} or newer: https://www.nvidia.com/Download/index.aspx" -f $driver, $B.min_driver)
}

# ---------------------------------------------------------------- 2. the engine: Love Live Studio's, or the pinned one
$S = if (Test-Path $SettingsPath) { Get-Content $SettingsPath -Raw | ConvertFrom-Json } else { $null }
if (-not $EngineDir -and $S -and $S.engine_dir -and (Test-Path (Join-Path $S.engine_dir "python_embeded\python.exe"))) { $EngineDir = $S.engine_dir }
if (-not $EngineDir) {
    $ll = Join-Path (Split-Path -Parent $Repo) "lovelive-studio\my\settings.json"
    if (Test-Path $ll) {
        $e = (Get-Content $ll -Raw | ConvertFrom-Json).engine_dir
        if ($e -and (Test-Path (Join-Path $e "python_embeded\python.exe"))) { $EngineDir = $e; Say ("using Love Live Studio's engine folder: " + $e) }
    }
}
if ($Check) { if ($EngineDir) { Say ("engine: " + $EngineDir) } else { Say ("engine: not installed yet (about {0:n0} GB download)" -f ($B.size / 1GB)) }; exit 0 }

if (-not $DataDir -and $S -and $S.models_dir) { $DataDir = Split-Path -Parent $S.models_dir }
if (-not $DataDir) { Fail 11 "no -DataDir given. Ask the user which drive to use (AGENTS.md section 1a), then run again with -DataDir." }
$DataDir = [IO.Path]::GetFullPath($DataDir)
$need = if ($EngineDir) { 15 } else { 25 }
$free = [math]::Round((Get-PSDrive $DataDir.Substring(0, 1)).Free / 1GB)
if ($free -lt $need) { Fail 11 ("drive {0} has {1} GB free; at least {2} GB is needed to start (the video models need about 40 GB more)." -f $DataDir.Substring(0, 2), $free, $need) }
foreach ($sub in "downloads", "models") { New-Item -ItemType Directory -Force (Join-Path $DataDir $sub) | Out-Null }

if (-not $EngineDir) {
    $vc = Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" -ErrorAction SilentlyContinue
    if (-not $vc -or $vc.Installed -ne 1) {
        Say "installing the Microsoft Visual C++ runtime (Windows may ask for permission: click Yes) ..."
        $vcexe = Join-Path $DataDir "downloads\vc_redist.x64.exe"
        Run-Native curl.exe -L --fail -o $vcexe "https://aka.ms/vs/17/release/vc_redist.x64.exe"
        Start-Process -FilePath $vcexe -ArgumentList "/install", "/quiet", "/norestart" -Verb RunAs -Wait
    }
    $archive = Join-Path $DataDir ("downloads\" + $B.file)
    Download $B.url $archive ([int64]$B.size) $B.sha256
    $root = Join-Path $DataDir "engine"
    $EngineDir = Join-Path $root "ComfyUI_windows_portable"
    if (-not (Test-Path (Join-Path $EngineDir "python_embeded\python.exe"))) {
        New-Item -ItemType Directory -Force $root | Out-Null
        Say "unpacking the engine (about a minute) ..."
        Run-Native tar.exe -xf $archive -C $root
        if (-not (Test-Path (Join-Path $EngineDir "python_embeded\python.exe"))) {
            Say "Windows' own unpacker can't open this archive here; using 7-Zip instead"
            if (Test-Path $EngineDir) { Remove-Item -Recurse -Force $EngineDir }
            $t = $Pin.tools."7zr"; $sz = Join-Path $DataDir "downloads\7zr.exe"
            Download $t.url $sz ([int64]$t.size) $t.sha256
            Run-Native $sz x $archive ("-o" + $root) -y | Out-Null
        }
        if (-not (Test-Path (Join-Path $EngineDir "python_embeded\python.exe"))) { Fail 13 "unpacking the engine failed" }
    }
    Say ("engine: " + $EngineDir)
}

# ---------------------------------------------------------------- 3. settings (port 8187: Love Live Studio keeps 8188)
$flags = if ($S -and $S.extra_flags) { "$($S.extra_flags)" } elseif ($Build -eq "modern") { "--use-ck-attention --fast fp16_accumulation" } else { "" }
$settings = [ordered]@{
    comfy_url = "http://127.0.0.1:8187"
    engine_dir = $EngineDir
    models_dir = (Join-Path $DataDir "models")
    data_dir = $(if ($GalleryDir) { [IO.Path]::GetFullPath($GalleryDir) } elseif ($S -and $S.data_dir) { $S.data_dir } else { Join-Path $Repo "gallery" })
    extra_flags = $flags
    gpu = $gpu; vram_gb = $vram; ram_gb = $ram; engine_build = $Build
}
[IO.File]::WriteAllText($SettingsPath, ($settings | ConvertTo-Json), (New-Object Text.UTF8Encoding($false)))
Say ("settings saved: " + $SettingsPath)

# ---------------------------------------------------------------- 4. point the engine at the model store
& (Join-Path $PSScriptRoot "py.cmd") (Join-Path $Repo "tools\models\store.py") wire
if ($LASTEXITCODE -ne 0) { Fail 13 "could not connect the engine to the models folder" }

# ---------------------------------------------------------------- 5. desktop shortcut
if (-not $NoShortcut) {
    $lnk = Join-Path ([Environment]::GetFolderPath("Desktop")) "Goon Studio.lnk"
    $sc = (New-Object -ComObject WScript.Shell).CreateShortcut($lnk)
    $sc.TargetPath = Join-Path $Repo "Goon Studio.cmd"
    $sc.WorkingDirectory = $Repo
    $sc.Save()
    Say ("desktop shortcut: " + $lnk)
}

# ---------------------------------------------------------------- 6. start the engine and the page
if ($NoStart) { Say "done (not started)"; exit 0 }
$sa = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $PSScriptRoot "start.ps1"), "-NoBrowser")
if ($StopOther) { $sa += "-StopOther" }; if ($KeepOther) { $sa += "-KeepOther" }
& powershell @sa
if ($LASTEXITCODE -eq 5) { Fail 5 "another app's engine is running: ask the user whether to stop it, then run setup again with -StopOther (or -KeepOther)" }
if ($LASTEXITCODE -ne 0) { Fail 14 "the engine or the page did not start; see the logs folder in the gallery folder" }
Say "setup finished. Next: download the models for a first template (AGENTS.md section 1a step 5)."
exit 0
