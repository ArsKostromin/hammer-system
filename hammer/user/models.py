import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

def generate_invite_code() -> str:
    """Генерация случайного 6-значного инвайт-кода (буквы и цифры)."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    activated_invite_code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.username
