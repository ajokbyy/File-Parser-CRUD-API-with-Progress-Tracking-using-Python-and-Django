import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField  # For PostgreSQL


# For SQLite, use: from django.db.models import JSONField

class File(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    original_file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    progress = models.IntegerField(default=0)
    parsed_data = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class FileChunk(models.Model):
    """For handling large file uploads in chunks"""
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='chunks')
    chunk_number = models.IntegerField()
    chunk_file = models.FileField(upload_to='chunks/')
    is_last = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file', 'chunk_number')