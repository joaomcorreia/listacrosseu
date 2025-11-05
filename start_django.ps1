# Django Setup and Admin Access Script
Write-Host "Setting up Django environment..." -ForegroundColor Green

# Clear any problematic environment variables
$env:PYTHONHOME = $null
$env:PYTHONPATH = $null

# Set proper Python home
$pythonPath = "C:\Users\joao-\AppData\Local\Programs\Python\Python311\python.exe"
$env:PYTHONHOME = "C:\Users\joao-\AppData\Local\Programs\Python\Python311"

Write-Host "Installing Django..." -ForegroundColor Yellow
& $pythonPath -m pip install --user django

Write-Host "Running database migrations..." -ForegroundColor Yellow
& $pythonPath manage.py migrate

Write-Host "Creating superuser account..." -ForegroundColor Yellow
Write-Host "You'll be prompted to enter username, email, and password for Django admin access:" -ForegroundColor Cyan
& $pythonPath manage.py createsuperuser

Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "Admin panel will be available at: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
& $pythonPath manage.py runserver