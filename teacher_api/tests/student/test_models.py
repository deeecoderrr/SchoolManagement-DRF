from teacher.models import Teacher
from rest_framework.test import APITestCase
from .config import TEACHER


class TeacherModelTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.teacher = Teacher.objects.create(**TEACHER)
        return super().setUpClass()

    def test_teacher_object(self):
        self.assertEqual(self.teacher.__str__(), TEACHER["name"])

    def test_teacher_instance(self):
        self.assertIsInstance(self.teacher, Teacher)

    def test_teacher_details(self):
        self.assertEqual(self.teacher.name, TEACHER["name"])
        self.assertEqual(self.teacher.dob, TEACHER["dob"])
        self.assertEqual(self.teacher.gender, TEACHER["gender"])
        self.assertEqual(self.teacher.phone_number, TEACHER["phone_number"])
        self.assertEqual(self.teacher.email, TEACHER["email"])
        self.assertEqual(self.teacher.address, TEACHER["address"])
        self.assertEqual(self.teacher.date_of_joining, TEACHER["date_of_joining"])
        self.assertEqual(self.teacher.salary, TEACHER["salary"])
        self.assertEqual(self.teacher.subject, TEACHER["subject"])
        self.assertEqual(
            self.teacher.previous_organization, TEACHER["previous_organization"]
        )

    def tearDown(self) -> None:
        self.teacher.delete()
        return super().tearDown()
