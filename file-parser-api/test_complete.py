# test_complete.py
import os
import django
import redis
from datetime import datetime


def test_redis():
    print("1. Testing Redis connection...")
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        if r.ping():
            print("   ✓ Redis connection successful")
            return True
        else:
            print("   ❌ Redis not responding")
            return False
    except Exception as e:
        print(f"   ❌ Redis connection failed: {e}")
        return False


def test_django():
    print("2. Testing Django setup...")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
        django.setup()
        print("   ✓ Django setup successful")
        return True
    except Exception as e:
        print(f"   ❌ Django setup failed: {e}")
        return False


def test_celery():
    print("3. Testing Celery setup...")
    try:
        from celery import current_app
        print(f"   ✓ Celery broker: {current_app.conf.broker_url}")
        print(f"   ✓ Celery backend: {current_app.conf.result_backend}")
        return True
    except Exception as e:
        print(f"   ❌ Celery setup failed: {e}")
        return False


def test_tasks():
    print("4. Testing task discovery...")
    try:
        from files import tasks
        print("   ✓ Tasks module imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ Tasks import failed: {e}")
        return False


if __name__ == '__main__':
    print("Running complete setup test...")
    print("=" * 50)

    results = []
    results.append(test_redis())
    results.append(test_django())
    results.append(test_celery())
    results.append(test_tasks())

    print("=" * 50)
    if all(results):
        print("🎉 ALL TESTS PASSED! Your setup is complete.")
        print("You can now start the Celery worker:")
        print("celery -A file_parser worker --loglevel=info")
    else:
        print("❌ Some tests failed. Please check the errors above.")