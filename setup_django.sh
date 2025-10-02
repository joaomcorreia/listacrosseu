#!/bin/bash
# Django Project Setup Script for Linux/Mac

echo "Starting ListAcross EU Django Setup..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9+ and try again"
    exit 1
fi

echo "Python found. Setting up virtual environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
echo "Installing Django dependencies..."
pip install -r django_requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit .env file with your configuration before continuing."
    echo
fi

# PostgreSQL check
echo
echo "IMPORTANT: Make sure PostgreSQL is installed and running"
echo "Default database configuration:"
echo "- Database: listacrosseu"
echo "- User: postgres"
echo "- Host: localhost"
echo "- Port: 5432"
echo

# Run Django commands
echo "Running Django setup commands..."
python manage.py makemigrations
python manage.py makemigrations accounts
python manage.py makemigrations businesses
python manage.py makemigrations subscriptions
python manage.py makemigrations websites
python manage.py makemigrations data_import

python manage.py migrate

echo
echo "Creating initial data (subscription plans, categories, countries)..."
python setup_initial_data.py

echo
echo "Setup completed successfully!"
echo
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo
echo "Admin user created:"
echo "  Email: admin@listacrosseu.com"
echo "  Password: admin123"
echo
echo "Visit http://localhost:8000/admin/ to access the admin panel."
echo