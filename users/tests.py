from django.test import Client, TestCase
from django.urls import reverse

from .models import CustomUser, UserProfile


class UserLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse("login")
        self.profile_url = reverse("profile")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_successful_login(self):
        """Test that a user can log in with valid credentials."""
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertRedirects(response, self.profile_url)

    def test_invalid_login(self):
        """Test that invalid credentials show an error message."""
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username or password is incorrect.")

    def test_login_page_renders(self):
        """Test that the login page renders correctly."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_missing_credentials(self):
        """Test that login fails when credentials are missing."""
        response = self.client.post(self.login_url, {"username": "", "password": ""})
        self.assertEqual(response.status_code, 200)

    def test_login_inactive_user(self):
        """Test that an inactive user cannot log in."""
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username or password is incorrect.")


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.profile_url = reverse("profile")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_authenticated_user_access(self):
        """Test that an authenticated user can access their profile."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["profile"], self.user_profile)

    def test_unauthenticated_user_access(self):
        """Test that an unauthenticated user is redirected to the login page."""
        response = self.client.get(self.profile_url)
        self.assertRedirects(response, f"{reverse('login')}?next={self.profile_url}")


class EditProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.edit_url = reverse("edit_profile", kwargs={"pk": self.user_profile.pk})

    def test_authenticated_user_edits_own_profile(self):
        """Test that an authenticated user can edit their own profile."""
        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(
            self.edit_url,
            {
                "home_address": "New Address",
                "phone_number": "+911234567890",
                "location": "POINT(1 1)",
            },
        )
        self.assertRedirects(response, reverse("profile"))

        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.home_address, "New Address")

    def test_authenticated_user_edits_another_profile(self):
        """Test that a user cannot edit another user's profile."""
        another_user = CustomUser.objects.create_user(
            username="anotheruser", password="anotherpass123", email="test@gmail.com"
        )
        another_profile = UserProfile.objects.create(user=another_user)
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("edit_profile", kwargs={"pk": another_profile.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_unauthenticated_user_access(self):
        """Test that an unauthenticated user is redirected to the login page."""
        response = self.client.get(self.edit_url)
        self.assertEqual(
            response.content.decode(), "You are not allowed to edit this profile."
        )
 

class UserMapViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.map_url = reverse("admin:admin_user_map")
        self.admin_user = CustomUser.objects.create_superuser(
            username="admin", password="adminpass123", email="admin@gmail.com"
        )
        self.regular_user = CustomUser.objects.create_user(
            username="regularuser", password="regularpass123", email="regular@gmail.com"
        )

    def test_admin_user_access(self):
        """Test that an admin user can access the map."""
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(self.map_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/map.html")

    def test_non_admin_user_access(self):
        """Test that a non-admin user cannot access the map."""
        self.client.login(username="regularuser", password="regularpass123")
        response = self.client.get(self.map_url)
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user_access(self):
        """Test that an unauthenticated user is redirected to the login page."""
        response = self.client.get(self.map_url)
        self.assertEqual(response.status_code, 302)


class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse("logout")
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_authenticated_user_logout(self):
        """Test that an authenticated user can log out."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse("login"))
