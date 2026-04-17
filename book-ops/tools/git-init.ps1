param(
    [string]$Remote = "https://github.com/nelsonlin/book-ops.git"
)

$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

git init
git branch -M main
git remote remove origin 2>$null
git remote add origin $Remote
git add .
git commit -m "Initial book-ops starter"
Write-Host "Push with: git push -u origin main"
