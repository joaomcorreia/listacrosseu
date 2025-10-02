@echo off
REM Django Project Setup Script for Windows

echo Starting ListAcross EU Django Setup...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ and try again
    pause
    exit /b 1
)

echo Python found. Setting up virtual environment...

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
echo Installing Django dependencies...
pip install -r django_requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file with your configuration before continuing.
    echo.
)

REM Check if PostgreSQL is configured
echo.
echo IMPORTANT: Make sure PostgreSQL is installed and running
echo Default database configuration:
echo - Database: listacrosseu
echo - User: postgres
echo - Host: localhost
echo - Port: 5432
echo.

REM Run Django commands
echo Running Django setup commands...
python manage.py makemigrations
python manage.py makemigrations accounts
python manage.py makemigrations businesses
python manage.py makemigrations subscriptions
python manage.py makemigrations websites
python manage.py makemigrations data_import

python manage.py migrate

echo.
echo Creating initial data (subscription plans, categories, countries)...
python setup_initial_data.py

echo.
echo Setup completed successfully!
echo.
echo To start the development server, run:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Admin user created:
echo   Email: admin@listacrosseu.com
echo   Password: admin123
echo.
echo Visit http://localhost:8000/admin/ to access the admin panel.
echo.

pause