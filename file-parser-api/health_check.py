# health_check.py
import os
import redis
import requests
import subprocess

def check_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r.ping()
    except:
        return False

def check_django():
    try:
        response = requests.get('http://localhost:8000/api/files/', timeout=2)
        return response.status_code in [200, 401, 403]  # 401/403 means server is up but auth needed
    except:
        return False

def check_celery():
    try:
        # Check if celery process is running
        result = subprocess.run(['celery', '-A', 'file_parser', 'status'],
                              capture_output=True, text=True, timeout=5)
        return 'online' in result.stdout.lower()
    except:
        return False

print("🩺 System Health Check")
print("=" * 30)
print(f"Redis:       {'✓' if check_redis() else '✗'}")
print(f"Django:      {'✓' if check_django() else '✗'}")
print(f"Celery:      {'✓' if check_celery() else '✗'}")
print("=" * 30)