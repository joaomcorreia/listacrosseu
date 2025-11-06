# Quick update commands for ListAcross EU on CyberPanel

# 1. Simple code update (no database changes)
quick_update() {
    cd /home/listacross.eu/backend
    git pull origin main
    source /home/listacross.eu/venv/bin/activate
    python manage.py collectstatic --no-input
    sudo systemctl reload openlitespeed
}

# 2. Full update with migrations
full_update() {
    cd /home/listacross.eu/backend
    git pull origin main
    source /home/listacross.eu/venv/bin/activate
    pip install -r requirements.cyberpanel.txt
    python manage.py migrate --no-input
    python manage.py collectstatic --no-input --clear
    sudo systemctl restart openlitespeed
}

# 3. Frontend only update
frontend_update() {
    cd /home/listacross.eu/public_html
    git pull origin main
    npm ci --only=production
    npm run build
}

# 4. Maintenance mode toggle
maintenance_on() {
    cd /home/listacross.eu/backend
    source /home/listacross.eu/venv/bin/activate
    python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = True; s.save(); print('Maintenance mode ON')"
}

maintenance_off() {
    cd /home/listacross.eu/backend
    source /home/listacross.eu/venv/bin/activate
    python manage.py shell -c "from core.models import SiteSettings; s = SiteSettings.get_settings(); s.maintenance_mode = False; s.save(); print('Maintenance mode OFF')"
}

# 5. Database backup
backup_db() {
    BACKUP_DIR="/home/listacross.eu/backups"
    mkdir -p $BACKUP_DIR
    mysqldump -u listacrosseu_user -p listacrosseu_prod > "$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"
    echo "Database backed up to $BACKUP_DIR"
}

# 6. View logs
view_logs() {
    tail -f /home/listacross.eu/logs/django.log
}

# 7. Check status
status_check() {
    echo "Backend status:"
    curl -s https://listacross.eu/api/v1/admin/health/ | jq
    
    echo "Maintenance status:"
    curl -s https://listacross.eu/api/v1/core/maintenance-status/ | jq
}

# Usage examples:
# source update_commands.sh
# quick_update
# maintenance_on
# full_update
# maintenance_off