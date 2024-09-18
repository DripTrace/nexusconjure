import sys
import os
from pathlib import Path

# Add the project root to the Python path
root_path = Path(__file__).resolve().parent.parent
sys.path.append(str(root_path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpalmdata.settings")

from django.core.wsgi import get_wsgi_application

def application(environ, start_response):
    try:
        django_application = get_wsgi_application()
        return django_application(environ, start_response)
    except Exception as e:
        print(f"Exception in WSGI application: {str(e)}")
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [b"Internal Server Error"]

def handler(event, context):
    print("Event:", event)
    print("Context:", context)
    
    environ = {
        'REQUEST_METHOD': event.get('httpMethod', 'GET'),
        'PATH_INFO': event.get('path', '/'),
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': event.get('body', ''),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }

    # Add headers
    for key, value in event.get('headers', {}).items():
        environ[f'HTTP_{key.upper().replace("-", "_")}'] = value

    def start_response(status, headers):
        nonlocal response
        response['statusCode'] = int(status.split()[0])
        response['headers'] = dict(headers)

    response = {}
    body = b''.join(application(environ, start_response))
    response['body'] = body.decode('utf-8')

    print("Response:", response)
    return response

# This is the important part for Vercel
app = application