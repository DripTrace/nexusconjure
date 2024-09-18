from django.core.wsgi import get_wsgi_application
import os
import sys
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")

application = get_wsgi_application()

def handler(event, context):
    print("Received event:", event)
    
    # Convert Vercel event to WSGI environ
    environ = {
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': event.get('queryStringParameters', '') or '',
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'HTTP_HOST': event.get('headers', {}).get('host', 'vercel'),
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', '').encode('utf-8'),
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

    # Call the WSGI application
    response_body = []
    def start_response(status, headers, exc_info=None):
        nonlocal response_body
        response_body = []
        return response_body.append

    body = application(environ, start_response)
    response_body.extend(body)

    # Convert WSGI response to Vercel response format
    return {
        'statusCode': int(response_body[0].decode().split()[0]),
        'headers': dict(response_body[1]),
        'body': b''.join(response_body[2:]).decode(),
    }