import requests
from .config import (
    LOGIN_CREDENTIAL,
    TEACHER_SERVICE_URL,
    AUTH_ENDPOINT,
    TEACHER_ENDPOINT,
)

import logging

logger = logging.getLogger("django")


def get_teacher_name(teacher_id):
    """
    Connect with teacher service to get the teacher name.
    teacher_id: id of the class teacher
    return: teacher name
    """

    try:
        auth_url = f"{TEACHER_SERVICE_URL}{AUTH_ENDPOINT}"
        res = requests.post(auth_url, LOGIN_CREDENTIAL)

        logger.info(f"Teacher service API auth response: {res.status_code}")

        if res.status_code == 200:
            token = res.json().get("token")
            headers = {"Authorization": f"Bearer {token}"}

            res = requests.get(
                f"{TEACHER_SERVICE_URL}{TEACHER_ENDPOINT}{teacher_id}/", headers=headers
            )

            logger.info(f"Teacher service API data response: {res.status_code}")

            if res.status_code == 200:
                return res.json().get("name")
        return
    except Exception as exe:
        logger.exception(exe)
        return
