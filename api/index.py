import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyEcomStoreNew.settings')

# Import Django
import django
from django.core.wsgi import get_wsgi_application

# Configure Django
django.setup()

# Get the WSGI application
application = get_wsgi_application()

# Vercel/Netlify handler
def handler(event, context):
    return application(event, context)