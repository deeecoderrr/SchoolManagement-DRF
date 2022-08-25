from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from http import HTTPStatus
from django.contrib.auth.models import User
from .config import HTML_MAP, USER1, USER2


class RegisterTest(TestCase):
    def test_get_register(self):
        get_register = self.client.get(reverse("register"))
        self.assertTemplateUsed(get_register, HTML_MAP["register"])
        self.assertEqual(get_register.status_code, HTTPStatus.OK.value)
        self.assertFalse(User.objects.filter(username=USER1["username"]))

    def test_post_register(self):
        post_register = self.client.post(reverse("register"), USER1)
        self.assertEqual(post_register.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(post_register.url, reverse("login"))
        register_user = User.objects.get(username=USER1["username"])
        self.assertFalse(register_user.is_active)
        self.assertEqual(register_user.username, USER1["username"])
        self.assertEqual(register_user.email, USER1["email"])
        self.assertNotEqual(register_user.password, USER1["password1"])


class AccountActivationTest(TestCase):
    def test_correct_credential(self):
        post_register = self.client.post(reverse("register"), USER2)
        for dicts in post_register.context:
            if "token" in dicts.keys():
                token = dicts["token"]
                uidb64 = dicts["uid"]
                break
        token = token if token else None
        uidb64 = uidb64 if uidb64 else None

        response = self.client.get(
            reverse("account_activation", kwargs={"token": token, "uidb64": uidb64})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertEqual(
            response.content,
            b"Thank you for your email confirmation. Now you can login your account.",
        )

    def test_wrong_credential(self):
        wrong_response = self.client.get(
            reverse(
                "account_activation",
                kwargs={"token": "wrong token", "uidb64": "wrong uid64"},
            )
        )
        self.assertEqual(wrong_response.status_code, HTTPStatus.OK.value)
        self.assertEqual(wrong_response.content, b"Activation link is invalid!")


class LoginTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            **{
                "username": USER2["username"],
                "password": USER2["password1"],
            }
        )
        return super().setUpClass()

    def test_correct_login(self):
        login = self.client.post(
            reverse("login"),
            {
                "username": USER2["username"],
                "password": USER2["password1"],
            },
        )
        self.assertEqual(login.status_code, HTTPStatus.FOUND.value)
        self.assertEqual(login.url, reverse("home"))

        # view any page that requires login
        new_content = self.client.get(reverse("student"))
        self.assertEqual(new_content.status_code, HTTPStatus.OK.value)

    def test_wrong_username(self):
        wrong_username = self.client.post(
            reverse("login"),
            {
                "username": "wrong",
                "password": USER2["password1"],
            },
        )
        self.assertNotEqual(wrong_username.status_code, HTTPStatus.FOUND.value)

        # view any page that requires login
        new_content = self.client.get(reverse("teacher"))
        self.assertNotEqual(new_content.status_code, HTTPStatus.OK.value)

    def test_wrong_password(self):
        wrong_password = self.client.post(
            reverse("login"),
            {
                "username": USER2["username"],
                "password": "wrong",
            },
        )
        self.assertNotEqual(wrong_password.status_code, HTTPStatus.FOUND.value)

        # view any page that requires login
        new_content = self.client.get(reverse("home"))
        self.assertNotEqual(new_content.status_code, HTTPStatus.OK.value)
