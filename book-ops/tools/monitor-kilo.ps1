# Monitor-Kilo.ps1
# Usage: .\tools\monitor-kilo.ps1 -TaskName "phase2" -PrNumber 3

param (
    [Parameter(Mandatory=$true)]
    [string]$TaskName,
    
    [Parameter(Mandatory=$true)]
    [int]$PrNumber,
    
    [int]$TimeoutSeconds = 600,
    [int]$IntervalSeconds = 30
)

$completionFile = ".ai\handoff\$TaskName-completion.md"
$startTime = Get-Date
$endTime = $startTime.AddSeconds($TimeoutSeconds)

Write-Host "Monitoring for task: $TaskName (PR #$PrNumber)" -ForegroundColor Cyan
Write-Host "Waiting for completion file: $completionFile"

while ((Get-Date) -lt $endTime) {
    $fileExists = Test-Path $completionFile
    
    if ($fileExists) {
        Write-Host "`nFound completion file!" -ForegroundColor Green
        
        # Now check GitHub PR status
        Write-Host "Checking GitHub Actions status for PR #$PrNumber..."
        $checks = gh pr checks $PrNumber --json state,name
        
        $allPassed = $true
        $allFinished = $true
        
        $checksObj = $checks | ConvertFrom-Json
        foreach ($check in $checksObj) {
            # Use state to determine if finished (anything not PENDING is finished)
            if ($check.state -eq "PENDING") { $allFinished = $false }
            
            # Check for success (SUCCESS or NEUTRAL)
            if ($check.state -ne "SUCCESS" -and $check.state -ne "NEUTRAL") { 
                if ($check.state -ne "PENDING") {
                    $allPassed = $false 
                }
            }
            
            $color = if ($check.state -eq "SUCCESS") { "Green" } elseif ($check.state -eq "FAILING") { "Red" } else { "Yellow" }
            Write-Host "  - $($check.name): $($check.state)" -ForegroundColor $color
        }
        
        if ($allFinished -and $allPassed) {
            Write-Host "`n[SUCCESS] Task '$TaskName' is complete and verified by CI." -ForegroundColor Green
            exit 0
        } elseif ($allFinished -and -not $allPassed) {
            Write-Host "`n[FAILURE] CI failed for PR #$PrNumber. Task needs fix." -ForegroundColor Red
            exit 1
        } else {
            Write-Host "Waiting for CI to finish..."
        }
    } else {
        Write-Host "." -NoNewline
    }
    
    Start-Sleep -Seconds $IntervalSeconds
}

Write-Host "`n[TIMEOUT] Monitoring timed out after $TimeoutSeconds seconds." -ForegroundColor Yellow
exit 2
