import sys
import os
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")

from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler
from io import BytesIO

django_application = get_wsgi_application()

def handler(event, context):
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'HTTP_HOST': event.get('headers', {}).get('host', 'vercel'),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(event.get('body', '').encode('utf-8')),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers
    for key, value in event.get('headers', {}).items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value

    response = {}
    
    def start_response(status, headers, exc_info=None):
        response['statusCode'] = int(status.split()[0])
        response['headers'] = dict(headers)

    body = b''.join(django_application(environ, start_response))
    response['body'] = body.decode('utf-8')

    return response

# This is important for Vercel
app = WSGIHandler()