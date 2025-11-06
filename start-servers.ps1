# ListAcross EU Development Server Starter
# Ensures clean startup of both Django and Next.js servers

Write-Host "🚀 Starting ListAcross EU Development Servers..." -ForegroundColor Green

# Kill any existing processes to prevent conflicts
Write-Host "🧹 Cleaning up existing processes..." -ForegroundColor Yellow
taskkill /F /IM python.exe 2>$null
taskkill /F /IM node.exe 2>$null

# Wait a moment for processes to fully terminate
Start-Sleep -Seconds 2

# Check if ports are free
Write-Host "🔍 Checking ports..." -ForegroundColor Yellow
$port8000 = netstat -ano | Select-String ":8000" | Select-String "LISTENING"
$port3000 = netstat -ano | Select-String ":3000" | Select-String "LISTENING"

if ($port8000) {
    Write-Host "⚠️  Port 8000 is still in use. You may need to manually kill the process." -ForegroundColor Red
}

if ($port3000) {
    Write-Host "⚠️  Port 3000 is still in use. You may need to manually kill the process." -ForegroundColor Red
}

# Navigate to project root
Set-Location "C:\projects\listacrosseu"

# Start Django server in background
Write-Host "🐍 Starting Django server on http://127.0.0.1:8000..." -ForegroundColor Blue
Start-Process powershell -ArgumentList "-NoProfile", "-Command", "Set-Location 'C:\projects\listacrosseu'; python manage.py runserver 127.0.0.1:8000" -WindowStyle Minimized

# Wait for Django to start
Start-Sleep -Seconds 3

# Navigate to frontend and start Next.js
Write-Host "⚛️  Starting Next.js server on http://localhost:3000..." -ForegroundColor Cyan
Set-Location "C:\projects\listacrosseu\frontend"
Start-Process powershell -ArgumentList "-NoProfile", "-Command", "Set-Location 'C:\projects\listacrosseu\frontend'; npm run dev" -WindowStyle Minimized

# Wait for Next.js to start
Start-Sleep -Seconds 5

# Verify servers are running
Write-Host "✅ Checking server status..." -ForegroundColor Green

$djangoRunning = netstat -ano | Select-String ":8000" | Select-String "LISTENING"
$nextjsRunning = netstat -ano | Select-String ":3000" | Select-String "LISTENING"

if ($djangoRunning) {
    Write-Host "✅ Django server: RUNNING on http://127.0.0.1:8000" -ForegroundColor Green
} else {
    Write-Host "❌ Django server: NOT RUNNING" -ForegroundColor Red
}

if ($nextjsRunning) {
    Write-Host "✅ Next.js server: RUNNING on http://localhost:3000" -ForegroundColor Green
} else {
    Write-Host "❌ Next.js server: NOT RUNNING" -ForegroundColor Red
}

Write-Host "`n🎉 Server startup complete!" -ForegroundColor Green
Write-Host "📝 Django Admin: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "🌐 Frontend: http://localhost:3000/" -ForegroundColor White
Write-Host "`n💡 To stop servers: run stop-servers.ps1" -ForegroundColor Yellow