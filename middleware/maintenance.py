from django.http import HttpResponse
from django.template import Template, Context
from django.conf import settings
from core.models import SiteSettings

class MaintenanceModeMiddleware:
    """
    Middleware to show maintenance page when maintenance mode is enabled.
    Allows admin users and API endpoints to continue working.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip maintenance mode for certain paths
        exempt_paths = [
            '/admin/',
            '/api/',
            '/django-admin/',
            '/static/',
            '/media/',
        ]
        
        # Skip if path is exempt
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        # Skip if user is admin
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)
        
        # Check if maintenance mode is enabled
        try:
            if SiteSettings.is_maintenance_mode():
                return self.maintenance_response(request)
        except Exception:
            # If there's any error checking settings, continue normally
            pass
        
        return self.get_response(request)
    
    def maintenance_response(self, request):
        """Return maintenance mode page"""
        
        maintenance_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Site Maintenance - ListAcross EU</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .maintenance-container {
            text-align: center;
            padding: 2rem;
            max-width: 600px;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .logo {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .maintenance-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        p {
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 1rem;
            opacity: 0.9;
        }
        
        .status-message {
            background: rgba(255, 255, 255, 0.2);
            padding: 1rem;
            border-radius: 10px;
            margin: 2rem 0;
        }
        
        .contact-info {
            margin-top: 2rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .spinning {
            animation: spin 3s linear infinite;
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .maintenance-container {
                margin: 1rem;
                padding: 1.5rem;
            }
            
            .logo {
                font-size: 2rem;
            }
            
            h1 {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="maintenance-container">
        <div class="logo">ListAcross EU</div>
        <div class="maintenance-icon">🔧</div>
        <h1>We're Making Things Better!</h1>
        
        <div class="status-message">
            <p><strong>Maintenance in Progress</strong></p>
            <p>Our team is working hard to improve your experience. We'll be back online shortly!</p>
        </div>
        
        <p>We're updating our systems to serve you better. This maintenance is necessary to ensure optimal performance and security.</p>
        
        <p><span class="spinning">⚙️</span> Expected downtime: Minimal</p>
        
        <div class="contact-info">
            <p>Need immediate assistance?</p>
            <p>📧 <strong>support@listacrosseu.com</strong></p>
            <p>Thank you for your patience!</p>
        </div>
    </div>
    
    <script>
        // Auto-refresh every 30 seconds to check if maintenance is over
        setTimeout(function() {
            window.location.reload();
        }, 30000);
    </script>
</body>
</html>
        """
        
        return HttpResponse(maintenance_html, status=503)