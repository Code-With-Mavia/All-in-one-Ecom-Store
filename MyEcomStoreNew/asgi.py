import os
import sys
from django.core.asgi import get_asgi_application

# Add your project root to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyEcomStoreNew.settings')

application = get_asgi_application()

handler = application
