@echo off
echo Setting up Django environment...

REM Set Python home to fix path issues
set PYTHONHOME=C:\Users\joao-\AppData\Local\Programs\Python\Python311
set PYTHONPATH=

echo Installing Django...
"%PYTHONHOME%\python.exe" -m pip install --user django

echo Running Django migrations...
"%PYTHONHOME%\python.exe" manage.py migrate

echo Creating superuser...
echo You'll be prompted to create a superuser account for Django admin access:
"%PYTHONHOME%\python.exe" manage.py createsuperuser

echo Starting Django development server...
"%PYTHONHOME%\python.exe" manage.py runserver

pause