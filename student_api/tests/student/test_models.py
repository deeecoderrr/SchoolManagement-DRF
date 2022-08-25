from student.models import Student
from rest_framework.test import APITestCase
from .config import STUDENT


class StudentModelTest(APITestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.student = Student.objects.create(**STUDENT)
        return super().setUpClass()

    def test_student_object(self):
        self.assertEqual(self.student.__str__(), STUDENT["name"])

    def test_student_instance(self):
        self.assertIsInstance(self.student, Student)

    def test_student_details(self):
        self.assertEqual(self.student.name, STUDENT["name"])
        self.assertEqual(self.student.dob, STUDENT["dob"])
        self.assertEqual(self.student.gender, STUDENT["gender"])
        self.assertEqual(self.student.father_name, STUDENT["father_name"])
        self.assertEqual(self.student.mother_name, STUDENT["mother_name"])
        self.assertEqual(self.student.sibilings, STUDENT["sibilings"])
        self.assertEqual(self.student.address, STUDENT["address"])
        self.assertEqual(self.student.parent_mobile, STUDENT["parent_mobile"])
        self.assertEqual(self.student.date_of_joining, STUDENT["date_of_joining"])
        self.assertEqual(self.student.mode_of_stay, STUDENT["mode_of_stay"])
        self.assertEqual(self.student.fees, STUDENT["fees"])

    def tearDown(self) -> None:
        self.student.delete()
        return super().tearDown()
