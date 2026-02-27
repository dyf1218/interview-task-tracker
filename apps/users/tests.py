from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthTests(APITestCase):
    """Tests for authentication endpoints."""

    def setUp(self):
        """Set up test data."""
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.me_url = reverse('me')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'TestPass123',
            'password_confirm': 'TestPass123',
        }

    def test_user_can_register_successfully(self):
        """Test that a user can register successfully."""
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')  # type: ignore[union-attr]
        self.assertEqual(response.data['email'], 'test@example.com')  # type: ignore[union-attr]
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_can_login_and_receive_tokens(self):
        """Test that a user can login and receive JWT tokens."""
        # First register the user
        self.client.post(self.register_url, self.user_data, format='json')

        # Then login
        login_data = {
            'username': 'testuser',
            'password': 'TestPass123',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # type: ignore[arg-type]
        self.assertIn('refresh', response.data)  # type: ignore[arg-type]

    def test_authenticated_user_can_fetch_me(self):
        """Test that an authenticated user can fetch /me/ endpoint."""
        # Register and login
        self.client.post(self.register_url, self.user_data, format='json')
        login_response = self.client.post(
            self.login_url,
            {'username': 'testuser', 'password': 'TestPass123'},
            format='json'
        )
        access_token = login_response.data['access']  # type: ignore[union-attr]

        # Fetch /me/ with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')  # type: ignore[attr-defined]
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')  # type: ignore[union-attr]
        self.assertEqual(response.data['email'], 'test@example.com')  # type: ignore[union-attr]

    def test_register_with_mismatched_passwords(self):
        """Test registration fails with mismatched passwords."""
        data = self.user_data.copy()
        data['password_confirm'] = 'DifferentPass123'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_username(self):
        """Test registration fails with existing username."""
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_user_cannot_access_me(self):
        """Test that unauthenticated user cannot access /me/."""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)