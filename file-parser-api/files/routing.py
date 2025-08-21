from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/files/(?P<file_id>[^/]+)/progress/$', consumers.FileProgressConsumer.as_asgi()),
]