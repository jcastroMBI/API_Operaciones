from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.conf import settings


class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    def salt(self):
        return settings.PASSWORD_STATIC_SALT
