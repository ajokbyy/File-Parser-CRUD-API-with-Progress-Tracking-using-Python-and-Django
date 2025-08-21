# test_simple_celery.py
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
django.setup()

# Now import Celery
from celery import current_app


def test_basic():
    print("Testing basic Celery setup...")
    print(f"Broker URL: {current_app.conf.broker_url}")
    print(f"Result Backend: {current_app.conf.result_backend}")

    # Create a simple task
    @current_app.task
    def add_numbers(x, y):
        return x + y

    # Test sending a task
    result = add_numbers.delay(5, 3)
    print(f"Task ID: {result.id}")

    return True


if __name__ == '__main__':
    test_basic()
    print("✓ Basic Celery test completed")