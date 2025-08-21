# files/tests/test_celery_integration.py
from django.test import TestCase
from celery import current_app
from django.conf import settings
import time


class CeleryIntegrationTest(TestCase):
    """Test Celery integration with Redis"""

    def test_celery_connection(self):
        """Test that Celery can connect to Redis broker"""
        # Test basic Celery app configuration
        self.assertEqual(current_app.conf.broker_url, settings.CELERY_BROKER_URL)
        self.assertEqual(current_app.conf.result_backend, settings.CELERY_RESULT_BACKEND)

        # Create a simple test task
        @current_app.task
        def test_task(x, y):
            return x * y

        # Send task to queue
        result = test_task.delay(5, 6)

        # Give it some time to process
        time.sleep(2)

        # Check if task was processed
        if result.ready():
            self.assertEqual(result.get(), 30)
            print("✓ Celery task processed successfully")
        else:
            self.fail("Celery task was not processed. Check worker is running.")