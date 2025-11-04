# PowerShell test script for assistant API
Write-Host "Testing Assistant API Integration..." -ForegroundColor Green

# Test 1: Valid message
Write-Host "`n1. Testing valid message..." -ForegroundColor Yellow
try {
    $body1 = @{message="Hello, can you help me with ListAcross EU?"} | ConvertTo-Json
    $response1 = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/assistant/api/ask/" -ContentType "application/json" -Body $body1
    Write-Host "✓ SUCCESS: $($response1.status)" -ForegroundColor Green
    Write-Host "Reply: $($response1.reply)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ FAILED: $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Empty message
Write-Host "`n2. Testing empty message..." -ForegroundColor Yellow
try {
    $body2 = @{message=""} | ConvertTo-Json
    $response2 = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/assistant/api/ask/" -ContentType "application/json" -Body $body2
    Write-Host "✓ RESPONSE: $($response2.status)" -ForegroundColor Green
    Write-Host "Reply: $($response2.reply)" -ForegroundColor Cyan
} catch {
    Write-Host "✓ EXPECTED ERROR: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 3: GET method (should fail)
Write-Host "`n3. Testing GET method (should fail)..." -ForegroundColor Yellow
try {
    $response3 = Invoke-RestMethod -Method Get -Uri "http://localhost:8000/assistant/api/ask/"
    Write-Host "✗ UNEXPECTED SUCCESS: $($response3)" -ForegroundColor Red
} catch {
    Write-Host "✓ EXPECTED ERROR: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Test 4: Invalid JSON (should fail)
Write-Host "`n4. Testing invalid JSON (should fail)..." -ForegroundColor Yellow
try {
    $response4 = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/assistant/api/ask/" -ContentType "application/json" -Body "invalid json"
    Write-Host "✗ UNEXPECTED SUCCESS: $($response4)" -ForegroundColor Red
} catch {
    Write-Host "✓ EXPECTED ERROR: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`nAssistant API testing complete!" -ForegroundColor Green
Write-Host "Frontend is running at: http://localhost:3001" -ForegroundColor Cyan
Write-Host "Backend is running at: http://localhost:8000" -ForegroundColor Cyan