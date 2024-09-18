import sys
import os
from pathlib import Path

# Print current directory and Python path for debugging
print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

print("Updated Python path:", sys.path)

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("Django application loaded successfully")
except ImportError as e:
    print(f"ImportError: {e}")
    print("Contents of rpalmdata directory:", os.listdir(root_path / 'rpalmdata'))

# This is the important part for Vercel
app = application