from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from .config import TEACHER, TEACHER_UPDATED, USERNAME
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class AuthTokenTest(APITestCase):
    def setUp(cls) -> None:
        cls.client = APIClient()
        cls.user = User.objects.create_user(**USERNAME)
        cls.token = cls.client.post("/auth/", USERNAME).json().get("token")

        return super().setUp()

    def test_wrong_username(self):
        token = self.client.post(
            "/auth/", {"username": "wrongname", "password": USERNAME["password"]}
        )
        self.assertEqual(token.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Unable to log in with provided credentials.",
            token.json().get("non_field_errors"),
        )

    def test_wrong_password(self):
        token = self.client.post(
            "/auth/", {"username": USERNAME["username"], "password": "wrongpass"}
        )
        self.assertEqual(token.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Unable to log in with provided credentials.",
            token.json().get("non_field_errors"),
        )

    def test_wrong_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + "_wrong_token_")

        # List operation
        response = self.client.get(reverse("teacher-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Post operation
        response = self.client.post(reverse("teacher-list"), TEACHER)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Get operation
        response = self.client.get("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Put operation
        response = self.client.put("/teacher/1/", TEACHER)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete operation
        response = self.client.delete("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # List operation
        response = self.client.get(reverse("teacher-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Post operation
        response = self.client.post(reverse("teacher-list"), TEACHER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get operation
        response = self.client.get("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Put operation
        response = self.client.put("/teacher/1/", TEACHER)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete operation
        response = self.client.delete("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UnAuthorizedTeacherViewTest(APITestCase):
    """
    Without authentication, all the operations should return 403(Forbidden)
    """

    def test_list(self):
        response = self.client.get(reverse("teacher-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        response = self.client.post(reverse("teacher-list"), TEACHER)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        response = self.client.get("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        response = self.client.put("/teacher/1/", TEACHER)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.client.delete("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizedTeacherViewTest(APITestCase):
    """
    With Token Authentication, all the endpoint should be accessible and output data should be correct
    """

    def setUp(cls) -> None:
        cls.client = APIClient()

        cls.user = User.objects.create_user(**USERNAME)
        token = cls.client.post("/auth/", USERNAME).json().get("token")
        cls.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        cls.client.post(reverse("teacher-list"), TEACHER)

        return super().setUp()

    def test_list(self):
        response = self.client.get(reverse("teacher-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.json()), 0)

    def test_post(self):
        # correct data
        response = self.client.post(reverse("teacher-list"), TEACHER)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # wrong data
        response = self.client.post(
            reverse("teacher-list"),
            {key: value for key, value in TEACHER.items() if key != "name"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"name": ["This field is required."]})

    def test_get(self):
        # with data
        response = self.client.get("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("name"), "Harshit")
        self.assertEqual(data.get("dob"), "2012-08-18")
        self.assertEqual(data.get("gender"), "Male")

        # without data
        response = self.client.get("/teacher/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})

    def test_put(self):
        # with data
        response = self.client.put("/teacher/1/", TEACHER_UPDATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("dob"), TEACHER_UPDATED["dob"])

        # without data
        response = self.client.put("/teacher/100/", TEACHER_UPDATED)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})

    def test_delete(self):
        # with data
        response = self.client.delete("/teacher/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # without data
        response = self.client.delete("/teacher/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})


class TeacherViewFieldTest(APITestCase):
    """
    Verify the validations for each field
    """

    def setUp(cls) -> None:
        cls.client = APIClient()

        cls.user = User.objects.create_user(**USERNAME)
        token = cls.client.post("/auth/", USERNAME).json().get("token")
        cls.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        cls.client.post(reverse("teacher-list"), TEACHER)
        return super().setUp()

    def test_name(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value
                if key != "name"
                else "verylongnamethathasmorethan30charectors"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"name": ["Ensure this field has no more than 30 characters."]},
        )

    def test_dob(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "dob" else "anything_except_datatime"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "dob": [
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                ]
            },
        )

    def test_gender(self):
        response = self.client.post(
            reverse("teacher-list"),
            {key: value if key != "gender" else "" for key, value in TEACHER.items()},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"gender": ['"" is not a valid choice.']})

    def test_previous_organization(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value
                if key != "previous_organization"
                else "verylongnamethathasmorethan30charectors"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "previous_organization": [
                    "Ensure this field has no more than 30 characters."
                ]
            },
        )

    def test_email(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value
                if key != "email"
                else "verylongnamethathasmorethan30charectors"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"email": ["Enter a valid email address."]}
        )

    def test_address(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value
                if key != "address"
                else "verylongnamethathasmorethan30charectors" * 3
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"address": ["Ensure this field has no more than 100 characters."]},
        )

    def test_phone_number(self):

        # string in mobile number
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "phone_number" else "not_an_integer"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"phone_number": ["A valid integer is required."]}
        )

        # 10 digit required
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "phone_number" else 123456789012
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"phone_number": ["Enter valid 10 digit mobile number."]}
        )

    def test_date_of_joining(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "date_of_joining" else "not_a_datetime"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "date_of_joining": [
                    "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                ]
            },
        )

    def test_subject(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "subject" else "date_of_joining"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"subject": ["Ensure this field has no more than 10 characters."]},
        )

    def test_salary(self):
        response = self.client.post(
            reverse("teacher-list"),
            {
                key: value if key != "salary" else "not_an_integer"
                for key, value in TEACHER.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"salary": ["A valid integer is required."]}
        )
