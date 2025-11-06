#!/bin/bash
# Update script for ListAcross EU on CyberPanel

set -e

echo "🔄 Updating ListAcross EU..."

# Configuration
DOMAIN="listacross.eu"
BACKEND_PATH="/home/$DOMAIN/backend"
FRONTEND_PATH="/home/$DOMAIN/public_html"
VENV_PATH="/home/$DOMAIN/venv"
BACKUP_PATH="/home/$DOMAIN/backups/$(date +%Y%m%d_%H%M%S)"

# Create backup directory
mkdir -p $BACKUP_PATH

echo "📦 Creating backup..."
# Backup database
mysqldump -u listacrosseu_user -p$DB_PASSWORD listacrosseu_prod > $BACKUP_PATH/database.sql

# Backup media files
cp -r $FRONTEND_PATH/media $BACKUP_PATH/

# Backup current code
cp -r $BACKEND_PATH $BACKUP_PATH/backend_old

echo "⬇️ Pulling latest changes..."
cd $BACKEND_PATH
git pull origin main

echo "📦 Updating Python dependencies..."
source $VENV_PATH/bin/activate
pip install -r requirements.cyberpanel.txt --upgrade

echo "🗃️ Running database migrations..."
export DJANGO_SETTINGS_MODULE=listacrosseu_project.settings_cyberpanel
python manage.py migrate --no-input

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "🌐 Building frontend..."
cd $FRONTEND_PATH
npm ci --only=production
npm run build

echo "🔄 Restarting services..."
# Restart Python app in CyberPanel
sudo systemctl restart lscpd  # LiteSpeed restart
sudo systemctl reload openlitespeed  # Or OpenLiteSpeed reload

# Restart Node.js app if using PM2
if command -v pm2 &> /dev/null; then
    pm2 restart listacross-frontend || echo "PM2 app not running"
fi

echo "🧹 Cleanup old files..."
find $BACKEND_PATH -name "*.pyc" -delete
find $BACKEND_PATH -name "__pycache__" -type d -exec rm -rf {} +

echo "✅ Update completed successfully!"
echo "🔙 Backup stored at: $BACKUP_PATH"

# Health check
echo "🔍 Running health check..."
sleep 5
if curl -f -s https://listacross.eu/api/v1/admin/health/ > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
fi

if curl -f -s https://listacross.eu/ > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
fi