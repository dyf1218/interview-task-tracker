from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task

User = get_user_model()


class TaskTests(APITestCase):
    """Tests for Task endpoints."""

    def setUp(self):
        """Set up test data."""
        # Create users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='TestPass123'
        )
        
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='TestPass123'
        )

        # Create tasks for user1
        self.task1 = Task.objects.create(
            owner=self.user1,
            title='Task 1',
            description='Description 1',
            status='todo',
            priority='high',
        )
        self.task2 = Task.objects.create(
            owner=self.user1,
            title='Task 2 Django',
            description='Description 2',
            status='in_progress',
            priority='medium',
        )

        # Create task for user2
        self.task3 = Task.objects.create(
            owner=self.user2,
            title='Task 3',
            description='Description 3',
            status='done',
            priority='low',
        )

        # URLs
        self.list_url = reverse('task-list')
        self.detail_url = lambda pk: reverse('task-detail', kwargs={'pk': pk})

        # Login URLs
        self.login_url = reverse('login')

    def get_token(self, user):
        """Helper to get JWT token for a user."""
        response = self.client.post(
            self.login_url,
            {'username': user.username, 'password': 'TestPass123'},
            format='json'
        )
        return response.data['access']

    def test_unauthenticated_user_cannot_access_task_list(self):
        """Test that unauthenticated user cannot access task list."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_create_task(self):
        """Test that authenticated user can create a task."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'todo',
            'priority': 'high',
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(response.data['owner_id'], self.user1.id)

    def test_authenticated_user_only_sees_own_tasks(self):
        """Test that authenticated user only sees their own tasks."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        # Check that user1's tasks are returned
        task_ids = [task['id'] for task in response.data['results']]
        self.assertIn(self.task1.id, task_ids)
        self.assertIn(self.task2.id, task_ids)
        self.assertNotIn(self.task3.id, task_ids)

    def test_user_cannot_update_another_users_task(self):
        """Test that user cannot update another user's task."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Try to update user2's task
        data = {'title': 'Hacked Task'}
        response = self.client.patch(self.detail_url(self.task3.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_filter_tasks_by_status(self):
        """Test that user can filter tasks by status."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.list_url, {'status': 'todo'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 1')

    def test_user_can_search_tasks_by_title(self):
        """Test that user can search tasks by title."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.list_url, {'search': 'Django'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'Task 2 Django')

    def test_user_can_delete_own_task(self):
        """Test that user can delete their own task."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.detail_url(self.task1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_user_cannot_delete_another_users_task(self):
        """Test that user cannot delete another user's task."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.delete(self.detail_url(self.task3.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=self.task3.id).exists())

    def test_user_can_update_own_task(self):
        """Test that user can update their own task."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        data = {'title': 'Updated Task 1', 'status': 'done'}
        response = self.client.patch(self.detail_url(self.task1.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task 1')
        self.assertEqual(response.data['status'], 'done')

    def test_pagination_works(self):
        """Test that pagination works correctly."""
        token = self.get_token(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.list_url, {'page_size': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertIsNotNone(response.data['next'])