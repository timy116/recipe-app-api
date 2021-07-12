from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmai.com',
            password='password'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmai.com',
            password='password',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page."""

        url = reverse('admin:core_user_changelist')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.user.name)
        self.assertContains(resp, self.user.email)
