import redis

try:
    # Try to connect to Redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    response = r.ping()
    print(f"✓ Redis connection successful: {response}")

    # Test setting and getting a value
    r.set('test_key', 'Hello from Python!')
    value = r.get('test_key')
    print(f"✓ Value retrieved: {value.decode('utf-8')}")

except Exception as e:
    print(f"✗ Redis connection failed: {e}")