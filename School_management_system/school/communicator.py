import requests
from .config import (
    STUDENT_SERVICE_URL,
    TEACHER_SERVICE_URL,
    TEACHER_ENDPOINT,
    AUTH_ENDPOINT,
    STUDENT_ENDPOINT,
)
import logging

logger = logging.getLogger("django")


class StudentCommunicator:
    def get_token(self) -> None:
        try:
            auth_url = f"{STUDENT_SERVICE_URL}{AUTH_ENDPOINT}"
            res = requests.post(auth_url, {"username": "Groot", "password": "123"})
            logger.info(f"Student auth response: {res}")

            if res.status_code == 200:
                return res.json().get("token")
            return
        except Exception as exe:
            logger.exception(exe)
            return

    def list_student(self):
        try:
            token = self.get_token()
            if token:
                list_url = f"{STUDENT_SERVICE_URL}{STUDENT_ENDPOINT}"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.get(list_url, headers=headers)
                logger.info(res)
                if res.status_code == 200:
                    return res.json()
                return "Something went wrong, please try again in sometime!"

            return "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return "Something went wrong, please try again in sometime!"

    def get_student(self, student_id):
        try:
            token = self.get_token()
            if token:
                list_url = f"{STUDENT_SERVICE_URL}{STUDENT_ENDPOINT}{student_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.get(list_url, headers=headers)
                logger.info(res)
                if res.status_code in (200, 404):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )
            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def delete_student(self, student_id):
        try:
            token = self.get_token()
            if token:
                list_url = f"{STUDENT_SERVICE_URL}{STUDENT_ENDPOINT}{student_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.delete(list_url, headers=headers)
                logger.info(res)
                if res.status_code == 404:
                    return res.status_code, "Student detail not found!"
                elif res.status_code == 204:
                    return res.status_code, "Student deleted sucessfully!"
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )
            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def create_student(self, data):
        try:
            token = self.get_token()
            if token:
                list_url = f"{STUDENT_SERVICE_URL}{STUDENT_ENDPOINT}"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.post(list_url, headers=headers, data=data)
                logger.info(res)
                if res.status_code in (201, 400):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )

            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def edit_student(self, student_id, data):
        try:
            token = self.get_token()
            if token:
                list_url = f"{STUDENT_SERVICE_URL}{STUDENT_ENDPOINT}{student_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.put(list_url, headers=headers, data=data)
                logger.info(res)
                if res.status_code in (200, 404, 400):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )

            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"


class TeacherCommunicator:
    def get_token(self) -> None:
        try:
            auth_url = f"{TEACHER_SERVICE_URL}{AUTH_ENDPOINT}"
            res = requests.post(auth_url, {"username": "Groot", "password": "123"})
            logger.info(res)

            if res.status_code == 200:
                return res.json().get("token")
            return
        except:
            return

    def list_teacher(self):
        try:
            token = self.get_token()
            if token:
                list_url = f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.get(list_url, headers=headers)
                logger.info(res)
                if res.status_code == 200:
                    return res.json()
                return "Something went wrong, please try again in sometime!"

            return "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def get_teacher(self, teacher_id):
        try:
            token = self.get_token()
            if token:
                list_url = f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}{teacher_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.get(list_url, headers=headers)
                logger.info(res)
                if res.status_code in (200, 404):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )

            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def delete_teacher(self, teacher_id):
        try:
            token = self.get_token()
            if token:
                list_url = f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}{teacher_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.delete(list_url, headers=headers)
                logger.info(res)
                if res.status_code == 404:
                    return res.status_code, "Teacher detail not found!"
                elif res.status_code == 204:
                    return res.status_code, "Teacher deleted sucessfully!"
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )
            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def create_teacher(self, data):
        try:
            token = self.get_token()
            if token:
                list_url = f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.post(list_url, headers=headers, data=data)
                logger.info(res)
                print(res.json())
                if res.status_code in (201, 400):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )
            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"

    def edit_teacher(self, teacher_id, data):
        try:
            token = self.get_token()
            if token:
                list_url = f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}{teacher_id}/"
                headers = {"Authorization": f"Bearer {token}"}

                res = requests.put(list_url, headers=headers, data=data)
                logger.info(res)
                if res.status_code in (200, 404, 400):
                    return res.status_code, res.json()
                return (
                    res.status_code,
                    "Something went wrong, please try again in sometime!",
                )
            return 403, "Something went wrong, please try again in sometime!"

        except Exception as exe:
            logger.exception(exe)
            return 500, "Something went wrong, please try again in sometime!"
