import sys
import os
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# This is the important part for Vercel
app = application