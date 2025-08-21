import os
import tempfile
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import File


class FileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Get JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_file_upload(self):
        # Create a test file
        test_file = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        test_file.write(b'name,age\nJohn,30\nJane,25')
        test_file.close()

        with open(test_file.name, 'rb') as file:
            response = self.client.post(reverse('file-list'), {'file': file}, format='multipart')

        os.unlink(test_file.name)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_get_files_list(self):
        # Create a test file record
        File.objects.create(name='test.csv', status='ready')

        response = self.client.get(reverse('file-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_file_progress(self):
        file_obj = File.objects.create(name='test.csv', status='processing', progress=50)

        response = self.client.get(reverse('file-progress', kwargs={'pk': file_obj.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['progress'], 50)
        self.assertEqual(response.data['status'], 'processing')

    def test_delete_file(self):
        file_obj = File.objects.create(name='test.csv', status='ready')

        response = self.client.delete(reverse('file-detail', kwargs={'pk': file_obj.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the file was deleted
        self.assertEqual(File.objects.count(), 0)