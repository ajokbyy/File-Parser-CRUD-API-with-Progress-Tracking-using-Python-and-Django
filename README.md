

File Parser CRUD API with Progress Tracking
A Django-based backend application for uploading, parsing, and managing files with real-time progress tracking. Supports CSV, Excel, and PDF files with asynchronous processing using Celery and Redis.

🚀 Features
File Upload with progress tracking

Multiple Format Support: CSV, Excel (XLSX), and PDF files

Asynchronous Processing with Celery and Redis

RESTful API with JWT authentication

Real-time Progress Updates via WebSocket

CRUD Operations for file management

Admin Interface for easy management

🛠️ Tech Stack
Backend: Django 4.2.7, Django REST Framework 3.14.0

Task Queue: Celery 5.3.4 with Redis broker

Database: SQLite (development), PostgreSQL (production-ready)

Real-time: Django Channels 4.0.0 with WebSocket support

Authentication: JWT with djangorestframework-simplejwt

File Parsing: pandas, openpyxl, pdfplumber

📦 Installation
Prerequisites
Python 3.8+

Redis server

Virtual environment

1. Clone and Setup
bash
# Clone the repository
git clone <repository-url>
cd file-parser-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
2. Install Dependencies
bash
pip install -r requirements.txt
3. Database Setup
bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
4. Install and Start Redis
Windows:

Download Redis from https://github.com/tporadowski/redis/releases

Install and add to PATH

Start Redis service:

cmd
redis-server --service-install
redis-server --service-start
Ubuntu/Debian:

bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
macOS:

bash
brew install redis
brew services start redis
5. Start Services
Terminal 1 - Celery Worker:

bash
celery -A file_parser worker --loglevel=info
Terminal 2 - Django Server:

bash
python manage.py runserver
🔑 API Usage
Authentication
First, obtain JWT tokens:

bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
Response:

json
{
  "refresh": "your_refresh_token",
  "access": "your_access_token"
}
API Endpoints
1. Upload File
bash
curl -X POST http://localhost:8000/api/files/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@your_file.csv"
2. List Files
bash
curl -X GET http://localhost:8000/api/files/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
3. Get File Details
bash
curl -X GET http://localhost:8000/api/files/{file_id}/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
4. Check Progress
bash
curl -X GET http://localhost:8000/api/files/{file_id}/progress/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
5. Delete File
bash
curl -X DELETE http://localhost:8000/api/files/{file_id}/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
📋 API Responses
File Upload Response
json
{
  "id": "uuid",
  "name": "filename.csv",
  "status": "uploading",
  "progress": 0,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:00:00Z"
}
Progress Response
json
{
  "file_id": "uuid",
  "status": "processing",
  "progress": 42
}
File Details Response (When ready)
json
{
  "id": "uuid",
  "name": "filename.csv",
  "status": "ready",
  "progress": 100,
  "parsed_data": [
    {"column1": "value1", "column2": "value2"},
    {"column1": "value3", "column2": "value4"}
  ],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:01:30Z"
}
🧪 Testing
Run Tests
bash
python manage.py test
Test File Upload
bash
# Create test file
echo "name,age,email" > test.csv
echo "John Doe,30,john@example.com" >> test.csv
echo "Jane Smith,25,jane@example.com" >> test.csv

# Upload test file
curl -X POST http://localhost:8000/api/files/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@test.csv"
🔧 Configuration
Environment Variables
Create a .env file for production:

env
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
Django Settings
Key settings in file_parser/settings.py:

python
# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# File upload settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
🌐 WebSocket Support
For real-time progress updates, connect via WebSocket:

javascript
const socket = new WebSocket('ws://localhost:8000/ws/files/{file_id}/progress/');

socket.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Progress:', data.progress);
  console.log('Status:', data.status);
};
📁 Project Structure
text
file-parser-api/
├── file_parser/          # Django project
│   ├── settings.py       # Project settings
│   ├── urls.py          # URL routing
│   ├── celery.py         # Celery configuration
│   └── asgi.py          # ASGI for WebSocket
├── files/               # Django app
│   ├── models.py        # Database models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── tasks.py         # Celery tasks
│   └── consumers.py     # WebSocket consumers
├── media/               # Uploaded files
├── requirements.txt     # Dependencies
└── manage.py           # Django management
🚀 Deployment
Production Checklist
Set DEBUG = False in settings

Generate a secure secret key

Set up PostgreSQL database

Configure production Redis

Set up static file serving

Configure allowed hosts

Set up SSL/HTTPS

Configure logging

Docker Deployment
dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "file_parser.asgi:application", "-k", "uvicorn.workers.UvicornWorker"]
🐛 Troubleshooting
Common Issues
Redis connection failed

Check Redis is running: redis-cli ping

Verify Redis URL in settings

Celery worker not processing tasks

Check worker is running: celery -A file_parser worker --loglevel=info

Verify Redis connection

File upload errors

Check MEDIA_ROOT directory exists and is writable

JWT authentication failed

Verify username/password

Check token expiration

Debug Mode
When DEBUG = True, detailed error pages are shown. For production, set DEBUG = False and configure proper error handling.

📄 License
This project is licensed under the MIT License.

🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Add tests

Submit a pull request

📞 Support
For support and questions:

Create an issue in the GitHub repository

Check the Django documentation

Refer to Celery and Redis documentation

Note: This is a development setup. For production deployment, ensure proper security measures, database configuration, and environment setup.
