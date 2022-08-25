from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.utils.http import urlsafe_base64_decode


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


def token_validator(user, token):
    """
    Validate the incoming token 
    """
    try:
        if user is not None and account_activation_token.check_token(user, token):
            return True
        else:
            return False
    except:
        return False


def token_decoder(uidb64):
    """
    Decode incoming token with the inbuilt module
    """
    try:
        return urlsafe_base64_decode(uidb64)
    except Exception as exe:
        print(exe)
        return 0


account_activation_token = TokenGenerator()
