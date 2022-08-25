from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from .tokens import account_activation_token

import logging

logger = logging.getLogger("django")


def trigger_email(hostname, user, email_id):
    try:
        email_body = render_to_string(
            "school/account_activation.html",
            {
                "hostname": hostname,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "username": user,
            },
        )
        response = send_mail(
            "Activate your School management account!",
            email_body,
            settings.EMAIL_HOST_USER,
            [email_id],
            fail_silently=False,
            html_message=email_body,
        )
        logger.info(f"activation email response: {response}")
        return response
    except Exception as exe:
        logger.exception(exe)
        return 0
