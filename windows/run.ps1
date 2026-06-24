# Runs find_a_flood.py using the project's virtual environment.
# Usage: .\windows\run.ps1 <city> <state> <radius> [--category <category>] [--refresh_data]

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPython = Join-Path $RepoRoot "venv\Scripts\python.exe"
$ScriptPath = Join-Path $RepoRoot "python\find_a_flood.py"

if (-not (Test-Path $VenvPython)) {
    Write-Error "Virtual environment not found. Run .\windows\setup.ps1 first."
}

& $VenvPython $ScriptPath @args
