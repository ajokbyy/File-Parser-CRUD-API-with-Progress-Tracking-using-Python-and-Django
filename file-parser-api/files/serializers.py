from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'status', 'progress', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'progress', 'created_at', 'updated_at']


class FileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'status', 'progress', 'parsed_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'progress', 'parsed_data', 'created_at', 'updated_at']


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        # Validate file size (e.g., 100MB limit)
        max_size = 100 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError(f"File size exceeds the limit of {max_size} bytes.")
        return value


class ProgressSerializer(serializers.Serializer):
    file_id = serializers.UUIDField()
    status = serializers.CharField()
    progress = serializers.IntegerField()