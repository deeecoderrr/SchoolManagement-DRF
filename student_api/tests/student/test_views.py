from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from .config import STUDENT, STUDENT_UPDATED, USERNAME
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
        response = self.client.get(reverse("student-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Post operation
        response = self.client.post(reverse("student-list"), STUDENT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Get operation
        response = self.client.get("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Put operation
        response = self.client.put("/student/1/", STUDENT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Delete operation
        response = self.client.delete("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_correct_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # List operation
        response = self.client.get(reverse("student-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Post operation
        response = self.client.post(reverse("student-list"), STUDENT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get operation
        response = self.client.get("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Put operation
        response = self.client.put("/student/1/", STUDENT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete operation
        response = self.client.delete("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UnAuthorizedStudentViewTest(APITestCase):
    """
    Without authentication, all the operations should return 403(Forbidden)
    """

    def test_list(self):
        response = self.client.get(reverse("student-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        response = self.client.post(reverse("student-list"), STUDENT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get(self):
        response = self.client.get("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put(self):
        response = self.client.put("/student/1/", STUDENT)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.client.delete("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthorizedStudentViewTest(APITestCase):
    """
    With Token Authentication, all the endpoint should be accessible and output data should be correct
    """

    def setUp(cls) -> None:
        cls.client = APIClient()

        cls.user = User.objects.create_user(**USERNAME)
        token = cls.client.post("/auth/", USERNAME).json().get("token")
        cls.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        cls.client.post(reverse("student-list"), STUDENT)

        return super().setUp()

    def test_list(self):
        response = self.client.get(reverse("student-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(len(response.json()), 0)

    def test_post(self):
        # correct data
        response = self.client.post(reverse("student-list"), STUDENT)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # wrong data
        response = self.client.post(
            reverse("student-list"),
            {key: value for key, value in STUDENT.items() if key != "name"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"name": ["This field is required."]})

    def test_get(self):
        # with data
        response = self.client.get("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("name"), "Harshit")
        self.assertEqual(data.get("dob"), "2012-08-18")
        self.assertEqual(data.get("gender"), "Male")

        # without data
        response = self.client.get("/student/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})

    def test_put(self):
        # with data
        response = self.client.put("/student/1/", STUDENT_UPDATED)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("dob"), STUDENT_UPDATED["dob"])

        # without data
        response = self.client.put("/student/100/", STUDENT_UPDATED)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})

    def test_delete(self):
        # with data
        response = self.client.delete("/student/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # without data
        response = self.client.delete("/student/100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(response.json(), {"detail": "Not found."})


class StudentViewFieldTest(APITestCase):
    """
    Verify the validations for each field
    """

    def setUp(cls) -> None:
        cls.client = APIClient()

        cls.user = User.objects.create_user(**USERNAME)
        token = cls.client.post("/auth/", USERNAME).json().get("token")
        cls.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

        cls.client.post(reverse("student-list"), STUDENT)

        return super().setUp()

    def test_name(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value
                if key != "name"
                else "verylongnamethathasmorethan30charectors"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"name": ["Ensure this field has no more than 30 characters."]},
        )

    def test_dob(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "dob" else "anything_except_datatime"
                for key, value in STUDENT.items()
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
            reverse("student-list"),
            {key: value if key != "gender" else "" for key, value in STUDENT.items()},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"gender": ['"" is not a valid choice.']})

    def test_father_name(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value
                if key != "father_name"
                else "verylongnamethathasmorethan30charectors"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"father_name": ["Ensure this field has no more than 30 characters."]},
        )

    def test_mother_name(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value
                if key != "mother_name"
                else "verylongnamethathasmorethan30charectors"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"mother_name": ["Ensure this field has no more than 30 characters."]},
        )

    def test_sibilings(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "sibilings" else "not_an_integer"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"sibilings": ["A valid integer is required."]}
        )

    def test_parent_mobile(self):

        # string in mobile number
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "parent_mobile" else "not_an_integer"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"parent_mobile": ["A valid integer is required."]}
        )

        # 10 digit required
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "parent_mobile" else 123456789012
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"parent_mobile": ["Enter valid 10 digit mobile number."]}
        )

    def test_date_of_joining(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "date_of_joining" else "not_a_datetime"
                for key, value in STUDENT.items()
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

    def test_mode_of_stay(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "mode_of_stay" else ""
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"mode_of_stay": ['"" is not a valid choice.']}
        )

    def test_fees(self):
        response = self.client.post(
            reverse("student-list"),
            {
                key: value if key != "fees" else "not_an_integer"
                for key, value in STUDENT.items()
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"fees": ["A valid integer is required."]}
        )
