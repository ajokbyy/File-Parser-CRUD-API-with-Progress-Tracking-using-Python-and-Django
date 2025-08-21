import os
import django
from celery import Celery

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
django.setup()

# Test Celery connection
app = Celery('file_parser')
app.config_from_object('django.conf:settings', namespace='CELERY')

if __name__ == '__main__':
    # Test basic Celery functionality
    print("Testing Celery connection to Redis...")


    # Try to send a simple task
    @app.task
    def test_task(x, y):
        return x + y


    # Send task to Redis queue
    result = test_task.delay(4, 6)
    print(f"✓ Task sent to Redis with ID: {result.id}")

    # Try to get result (after a short delay)
    import time

    time.sleep(2)

    if result.ready():
        print(f"✓ Task completed successfully: {result.get()}")
    else:
        print("Task still processing...")