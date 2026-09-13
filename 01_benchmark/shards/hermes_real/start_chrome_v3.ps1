# Phase 3 Benchmark Chrome v3 Startup Script
# Execute this in PowerShell as Administrator

$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$profile = "C:\workspace\AI_Media_Matrix\browser_profiles\douyin_benchmark_v3"

Write-Host "Starting Benchmark Chrome v3..."
Write-Host "Profile: $profile"
Write-Host "Port: 9223"
Write-Host ""

Start-Process -FilePath $chrome -ArgumentList @(
    "--remote-debugging-port=9223",
    "--remote-debugging-address=127.0.0.1",
    "--user-data-dir=$profile",
    "--no-first-run",
    "--no-default-browser-check",
    "--remote-allow-origins=*",
    "https://www.douyin.com"
)

Write-Host "Chrome starting... Please wait 5 seconds."
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Verifying CDP..."
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:9223/json/version" -TimeoutSec 5
    Write-Host "CDP HTTP: PASS"
    Write-Host "Browser: $($response.Browser)"
} catch {
    Write-Host "CDP HTTP: FAIL - $_"
}

Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Complete Douyin login in the new Chrome window"
Write-Host "2. Complete any CAPTCHA/verification"
Write-Host "3. Keep the window open"
Write-Host "4. Reply 'Chrome v3 ready' when done"
