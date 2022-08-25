import re

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


import logging

logger = logging.getLogger("django")


def username_validation(username):
    if not re.match(r"^[A-Za-z0-9]+$", username):
        logger.error(f"Invalid username: {username}")
        raise ValidationError(
            _("Enter a valid username. This value may contain only letters and numbers")
        )
