# ListAcross EU Development Server Stopper
# Cleanly stops both Django and Next.js servers

Write-Host "🛑 Stopping ListAcross EU Development Servers..." -ForegroundColor Red

# Kill Django processes
Write-Host "🐍 Stopping Django servers..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force
    Write-Host "✅ Django processes terminated" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No Django processes found" -ForegroundColor Gray
}

# Kill Node.js processes  
Write-Host "⚛️  Stopping Next.js servers..." -ForegroundColor Yellow
$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    $nodeProcesses | Stop-Process -Force
    Write-Host "✅ Next.js processes terminated" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No Next.js processes found" -ForegroundColor Gray
}

# Wait for processes to terminate
Start-Sleep -Seconds 2

# Verify ports are free
Write-Host "🔍 Verifying ports are free..." -ForegroundColor Yellow
$port8000 = netstat -ano | Select-String ":8000" | Select-String "LISTENING"
$port3000 = netstat -ano | Select-String ":3000" | Select-String "LISTENING"

if (-not $port8000) {
    Write-Host "✅ Port 8000: FREE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Port 8000: STILL IN USE" -ForegroundColor Red
}

if (-not $port3000) {
    Write-Host "✅ Port 3000: FREE" -ForegroundColor Green
} else {
    Write-Host "⚠️  Port 3000: STILL IN USE" -ForegroundColor Red
}

Write-Host "`n🎉 Servers stopped successfully!" -ForegroundColor Green