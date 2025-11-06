#!/usr/bin/env python3
"""
WSGI config for ListAcross EU on CyberPanel.
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).resolve().parent.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Load environment variables
from dotenv import load_dotenv
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listacrosseu_project.settings_cyberpanel')

from django.core.wsgi import application

# Activate virtual environment
activate_this = '/home/listacross.eu/venv/bin/activate_this.py'
if Path(activate_this).exists():
    exec(open(activate_this).read(), {'__file__': activate_this})

# Application callable
app = application