from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from tasks.models import ToDo


class ToDoTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.todo = ToDo.objects.create(title="Test Task", description="Test Description", user=self.user)

    def test_create_todo(self):
        data = {'title': 'New Task'}
        response = self.client.post('/api/todos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_todos(self):
        response = self.client.get('/api/todos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo(self):
        data = {'title': 'Updated Task', 'description': 'Updated Description'}
        response = self.client.put(f'/api/todos/{self.todo.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_todo(self):
        response = self.client.delete(f'/api/todos/{self.todo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
