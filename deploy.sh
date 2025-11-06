#!/bin/bash
# Production deployment script for listacross.eu

set -e  # Exit on any error

echo "🚀 Deploying ListAcross EU to production..."

# Set environment
export NODE_ENV=production
export DJANGO_SETTINGS_MODULE=listacrosseu_project.settings_production

# Load environment variables
if [ -f .env.production ]; then
    export $(grep -v '^#' .env.production | xargs)
fi

echo "📦 Installing Python dependencies..."
pip install -r requirements.production.txt

echo "📦 Installing Node.js dependencies..."
cd frontend
npm ci
npm run build
cd ..

echo "🗃️ Running database migrations..."
python manage.py migrate --no-input

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "👤 Creating superuser (if not exists)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@listacross.eu', 'change-this-password')
"

echo "🔧 Starting services with Docker Compose..."
docker-compose -f docker-compose.production.yml up -d

echo "🏃 Running health checks..."
sleep 10
curl -f http://localhost:8000/api/v1/admin/health/ || echo "⚠️ Backend health check failed"
curl -f http://localhost:3000/ || echo "⚠️ Frontend health check failed"

echo "✅ Deployment complete!"
echo "🌍 Your site should be available at https://listacross.eu"
echo "🔐 Admin panel: https://listacross.eu/admin/"
echo "📊 Don't forget to:"
echo "   - Configure DNS records"
echo "   - Setup SSL certificates"
echo "   - Configure email settings"
echo "   - Setup monitoring"