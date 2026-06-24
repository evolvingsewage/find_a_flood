# Creates a Python virtual environment and installs requirements.txt into it.
# Usage (from repo root or anywhere): .\windows\setup.ps1

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $RepoRoot "venv"
$RequirementsFile = Join-Path $RepoRoot "requirements.txt"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    Write-Error "Python launcher 'py' not found. Install Python from https://python.org and ensure it's on PATH."
}

if (-not (Test-Path $VenvPath)) {
    py -m venv $VenvPath
} else {
    Write-Warning "Virtual environment already exists at $VenvPath"
}

& "$VenvPath\Scripts\python.exe" -m pip install --upgrade pip
& "$VenvPath\Scripts\pip.exe" install -r $RequirementsFile

Write-Host "Setup complete. Run the tool with: .\windows\run.ps1 <city> <state> <radius>"
