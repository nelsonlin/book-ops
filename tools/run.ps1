param(
    [Parameter(Mandatory = $true)]
    [string]$BookName,

    [ValidateSet("table", "json", "tsv")]
    [string]$Format = "table",

    [string[]]$Sites = @()
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$python = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "Virtual environment not found. Run .\tools\setup.ps1 first."
}

$args = @("bookops.py", $BookName, "--format", $Format)
if ($Sites.Count -gt 0) {
    $args += "--sites"
    $args += $Sites
}
