from django.test import TestCase
from django.urls import reverse

from accounts.forms import UserCreationForm
from accounts.models import User


class TestSignUpModel(TestCase):
    def test_create_user(self):
        User.objects.create_user("test", password="check0123")
        self.assertTrue(User.objects.filter(username="test").exists())


class TestSignUpForm(TestCase):
    def test_signup_form_with_valid_data(self):
        form_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "check0123",
            "password2": "check0123",
        }
        form = UserCreationForm(form_data)
        self.assertTrue(form.is_valid())

    def test_signup_form_with_invalid_data(self):
        form_data = {
            "username": "invalid",
            "email": "test@example.com",
            "password1": "check0123",
            "password2": "incorrect",
        }
        form = UserCreationForm(form_data)
        self.assertFalse(form.is_valid())


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "check0123",
            "password2": "check0123",
        }

    def test_success_get(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

    def test_use_template(self):
        res = self.client.get(self.url)
        self.assertTemplateUsed(res, "accounts/signup.html")

    def test_signup_successfully(self):
        self.client.post(self.url, self.valid_data)
        self.assertTrue(
            User.objects.filter(username=self.valid_data["username"]).exists()
        )

    def test_signup_redirect(self):
        res = self.client.post(self.url, self.valid_data)
        self.assertRedirects(res, reverse("accounts:home"))

    def test_signup_failed_with_invalid_data(self):
        data = self.valid_data
        data["username"] = ""
        res = self.client.post(self.url, data)
        errors = res.context["form"].errors
        self.assertListEqual(errors.get("username"), ["このフィールドは必須です。"])
