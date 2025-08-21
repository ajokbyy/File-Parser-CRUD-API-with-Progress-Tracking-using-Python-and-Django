# check_setup.py
import os
import sys

# Check if we're in the right directory
if not os.path.exists('manage.py'):
    print("❌ ERROR: Please run this from the project root directory (where manage.py is located)")
    print("Current directory:", os.getcwd())
    sys.exit(1)

print("✓ Running from correct directory")

# Check Redis
try:
    import redis

    r = redis.Redis(host='localhost', port=6379, db=0)
    if r.ping():
        print("✓ Redis connection successful")
    else:
        print("❌ Redis not responding")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")

# Check Celery
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'file_parser.settings')
    import django

    django.setup()

    from celery import current_app

    print(f"✓ Celery configured with broker: {current_app.conf.broker_url}")

except Exception as e:
    print(f"❌ Celery setup failed: {e}")

print("\nSetup check completed!")