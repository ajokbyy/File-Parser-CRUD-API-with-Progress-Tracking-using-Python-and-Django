import os
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import File
from .serializers import FileSerializer, FileDetailSerializer, FileUploadSerializer, ProgressSerializer
from .tasks import process_file


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FileDetailSerializer
        return FileSerializer

    def create(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']

            # Create file record
            file_obj = File.objects.create(
                name=uploaded_file.name,
                original_file=uploaded_file,
                status='uploading'
            )

            # Start processing task
            process_file.delay(str(file_obj.id))

            return Response(
                FileSerializer(file_obj).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        file_obj = get_object_or_404(File, id=pk)
        serializer = ProgressSerializer({
            'file_id': file_obj.id,
            'status': file_obj.status,
            'progress': file_obj.progress
        })
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.status != 'ready':
            return Response(
                {"message": "File upload or processing in progress. Please try again later."},
                status=status.HTTP_202_ACCEPTED
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from django.shortcuts import render

# Create your views here.
