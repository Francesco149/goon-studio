@echo off
rem Runs a repo script with the engine's Python (no Python install needed), e.g.:  kit\py.cmd tools\models\store.py check anime_pov
set "STUDIO_PY="
for /f "usebackq delims=" %%i in (`powershell -NoProfile -Command "try { $s = Get-Content -Raw '%~dp0..\my\settings.json' | ConvertFrom-Json; if ($s.python) { $s.python } else { Join-Path $s.engine_dir 'python_embeded\python.exe' } } catch {}"`) do set "STUDIO_PY=%%i"
if not exist "%STUDIO_PY%" (
  echo Goon Studio is not set up yet: run kit\setup.ps1 first.
  exit /b 2
)
"%STUDIO_PY%" -s "%~dp0pyrun.py" %*
