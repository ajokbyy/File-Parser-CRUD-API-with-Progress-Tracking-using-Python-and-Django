# test_celery.py (in project root - same level as manage.py)
import os
import django
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
django.setup()

from celery import Celery


def test_celery_connection():
    """Test if Celery can connect to Redis"""
    print("Testing Celery connection to Redis...")

    # Create Celery app instance
    app = Celery('file_parser')
    app.config_from_object('django.conf:settings', namespace='CELERY')

    # Test basic Celery functionality
    @app.task
    def simple_add(x, y):
        return x + y

    # Send task to Redis queue
    print("Sending test task to Celery...")
    result = simple_add.delay(4, 6)
    print(f"✓ Task sent to Redis with ID: {result.id}")

    # Wait a bit and check result
    import time
    time.sleep(3)

    if result.ready():
        print(f"✓ Task completed successfully: {result.get()}")
        return True
    else:
        print("✗ Task not processed. Check if Celery worker is running.")
        return False


if __name__ == '__main__':
    success = test_celery_connection()
    if success:
        print("\n🎉 Celery + Redis setup is working correctly!")
    else:
        print("\n❌ There might be an issue with your setup.")