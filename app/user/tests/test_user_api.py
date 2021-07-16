from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the user API (public)."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating a user with valid payload is successful."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123456',
            'name': 'Test Name',
        }
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**resp.data)

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', resp.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123456',
        }
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'pwd',
        }
        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123456',
        }
        resp = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123456',
        }
        create_user(**payload)
        payload['password'] = 'wrong'
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist."""

        payload = {
            'email': 'test@gmail.com',
            'password': 'test123456',
        }
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required."""

        payload = {
            'email': 'one',
            'password': '',
        }
        resp = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
