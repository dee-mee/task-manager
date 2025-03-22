import os
import sys
import webbrowser
import threading
import time
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

def run_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
    application = get_wsgi_application()
    execute_from_command_line(['manage.py', 'runserver', '--noreload'])

def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    # Start Django server in a separate thread
    server_thread = threading.Thread(target=run_django)
    server_thread.daemon = True
    server_thread.start()

    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()

    try:
        # Keep the main thread running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)
