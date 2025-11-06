# Basic health monitoring script
#!/bin/bash

# Health check endpoints
BACKEND_URL="https://listacross.eu/api/v1/admin/health/"
FRONTEND_URL="https://listacross.eu/"
MAINTENANCE_URL="https://listacross.eu/api/v1/core/maintenance-status/"

# Check backend
if curl -f -s "$BACKEND_URL" > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend is down!"
    # Send alert (email, Slack, etc.)
fi

# Check frontend
if curl -f -s "$FRONTEND_URL" > /dev/null; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend is down!"
fi

# Check maintenance mode
MAINTENANCE=$(curl -s "$MAINTENANCE_URL" | jq -r '.maintenance_mode')
if [ "$MAINTENANCE" = "true" ]; then
    echo "🔧 Site is in maintenance mode"
else
    echo "✅ Site is operational"
fi