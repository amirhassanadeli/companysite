from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AuthTest(TestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

        self.user_data = {
            "email": "test@example.com",
            "password": "12345678",
            "confirm_password": "12345678",
        }

    # ✅ تست ثبت‌نام موفق
    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    # ✅ تست ثبت‌نام با ایمیل تکراری
    def test_register_duplicate_email(self):
        User.objects.create_user(email="test@example.com", password="12345678")
        response = self.client.post(self.register_url, self.user_data)

        self.assertContains(response, "قبلاً ثبت شده است")

    # ✅ تست لاگین موفق
    def test_login_success(self):
        User.objects.create_user(email="test@example.com", password="12345678")

        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "12345678"
        })

        self.assertEqual(response.status_code, 302)

    # ✅ تست لاگین با پسورد اشتباه
    def test_login_wrong_password(self):
        User.objects.create_user(email="test@example.com", password="12345678")

        response = self.client.post(self.login_url, {
            "email": "test@example.com",
            "password": "wrongpass"
        })

        self.assertContains(response, "ایمیل یا رمز عبور اشتباه است")

    # ✅ تست خروج از حساب
    def test_logout(self):
        user = User.objects.create_user(email="test@example.com", password="12345678")
        self.client.login(email="test@example.com", password="12345678")

        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
