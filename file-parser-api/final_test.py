# final_test.py
import os
import django
import redis
import time
from datetime import datetime

print("🚀 Running Final Comprehensive Test")
print("=" * 60)


def print_status(step, success, message):
    status = "✓" if success else "✗"
    print(f"{status} {step}: {message}")


# Test 1: Redis Connection
try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    redis_ok = r.ping()
    print_status("Redis Connection", redis_ok, "Connected successfully")
except Exception as e:
    print_status("Redis Connection", False, f"Failed: {e}")
    redis_ok = False

# Test 2: Django Setup
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
    django.setup()
    print_status("Django Setup", True, "Initialized successfully")
    django_ok = True
except Exception as e:
    print_status("Django Setup", False, f"Failed: {e}")
    django_ok = False

# Test 3: Celery Configuration
try:
    from celery import current_app

    broker = current_app.conf.broker_url
    backend = current_app.conf.result_backend
    print_status("Celery Config", True, f"Broker: {broker}, Backend: {backend}")
    celery_ok = True
except Exception as e:
    print_status("Celery Config", False, f"Failed: {e}")
    celery_ok = False

# Test 4: Database Connection
try:
    from django.db import connection

    connection.ensure_connection()
    print_status("Database Connection", True, "Connected successfully")
    db_ok = True
except Exception as e:
    print_status("Database Connection", False, f"Failed: {e}")
    db_ok = False

# Test 5: Models Import
try:
    from files.models import File

    print_status("Models Import", True, "Models imported successfully")
    models_ok = True
except Exception as e:
    print_status("Models Import", False, f"Failed: {e}")
    models_ok = False

# Test 6: Tasks Import
try:
    from files.tasks import process_file

    print_status("Tasks Import", True, "Tasks imported successfully")
    tasks_ok = True
except Exception as e:
    print_status("Tasks Import", False, f"Failed: {e}")
    tasks_ok = False

# Test 7: Create Test Task
try:
    from celery import current_app


    @current_app.task
    def test_final_task():
        return "Final test successful!"


    result = test_final_task.delay()
    time.sleep(2)  # Give it time to process

    if result.ready():
        print_status("Task Execution", True, f"Result: {result.get()}")
        task_ok = True
    else:
        print_status("Task Execution", False, "Task not processed (is worker running?)")
        task_ok = False
except Exception as e:
    print_status("Task Execution", False, f"Failed: {e}")
    task_ok = False

print("=" * 60)

# Summary
all_tests = [redis_ok, django_ok, celery_ok, db_ok, models_ok, tasks_ok, task_ok]
success_count = sum(all_tests)
total_count = len(all_tests)

if all(all_tests):
    print("🎉 ALL TESTS PASSED! Your system is fully operational!")
    print("\nNext steps:")
    print("1. Keep Redis running")
    print("2. Start Celery worker in a new terminal:")
    print("   celery -A file_parser worker --loglevel=info")
    print("3. Start Django server:")
    print("   python manage.py runserver")
    print("4. Test file uploads via API")
else:
    print(f"⚠️  {success_count}/{total_count} tests passed")
    if not task_ok:
        print("   Note: Task execution test requires Celery worker to be running")

print("=" * 60)