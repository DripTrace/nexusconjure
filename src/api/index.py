import sys
import os
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")

from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

class VercelHandler(WSGIHandler):
    def __call__(self, environ, start_response):
        try:
            return super().__call__(environ, start_response)
        except Exception as e:
            status = '500 Internal Server Error'
            response_headers = [('Content-type', 'text/plain')]
            start_response(status, response_headers)
            return [str(e).encode()]

application = VercelHandler()

def handler(event, context):
    return application(event, context)