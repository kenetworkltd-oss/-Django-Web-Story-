import io
import sys
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

class PostSecurityTest(TestCase):
    def setUp(self):
        # This runs before every test method
        self.client = Client()
        self.create_url = reverse('post_create')

    def test_anonymous_user_cannot_access_create_page(self):
        """Verify that a user who isn't logged in is redirected."""
        response = self.client.get(self.create_url)
        # 302 is the status code for a redirect (to the login page)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_user_can_access_create_page(self):
        """Verify that a logged-in user can see the form."""
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

class PostSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='signaltester', password='password123')

    def test_post_save_signal_logs_message(self):
        """Verify that the signal prints a log message on creation."""
        captured_output = io.StringIO()
        sys.stdout = captured_output

        Post.objects.create(
            title="Test Signal Post",
            content="Testing the automation...",
            author=self.user,
            status="published"
        )

        sys.stdout = sys.__stdout__
        self.assertIn("Standard Log: New content created", captured_output.getvalue())