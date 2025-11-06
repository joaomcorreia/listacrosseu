#!/bin/bash
# CyberPanel deployment script for ListAcross EU on AlmaLinux

set -e

echo "🚀 Deploying ListAcross EU on CyberPanel..."

# CyberPanel paths
DOMAIN="listacross.eu"
SITE_PATH="/home/$DOMAIN/public_html"
BACKEND_PATH="/home/$DOMAIN/backend"
VENV_PATH="/home/$DOMAIN/venv"

# Create directories
sudo mkdir -p $BACKEND_PATH
sudo mkdir -p $VENV_PATH
sudo chown -R cyberpanel:cyberpanel /home/$DOMAIN

echo "📦 Setting up Python virtual environment..."
cd $BACKEND_PATH
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.production.txt

echo "🗃️ Setting up database..."
# CyberPanel usually has MySQL/MariaDB
mysql -u root -p$MYSQL_ROOT_PASSWORD << EOF
CREATE DATABASE IF NOT EXISTS listacrosseu_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'listacrosseu_user'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON listacrosseu_prod.* TO 'listacrosseu_user'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "🔧 Running Django setup..."
export DJANGO_SETTINGS_MODULE=listacrosseu_project.settings_production
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

echo "🌐 Setting up Node.js frontend..."
cd /home/$DOMAIN
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 18
nvm use 18

cd $SITE_PATH
npm ci --only=production
npm run build

echo "✅ CyberPanel deployment complete!"