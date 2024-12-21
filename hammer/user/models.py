import random
import string
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


def generate_invite_code() -> str:
    """Генерация случайного 6-значного инвайт-кода (буквы и цифры)."""
    while True:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not CustomUser.objects.filter(invite_code=code).exists():
            return code


class CustomUser(AbstractUser):
    name = models.CharField(max_length=32, verbose_name="Имя", blank=True, null=True)
    phone_number = PhoneNumberField(help_text="Enter phone number", verbose_name='номер телефона', blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code, verbose_name='инвайт код')
    activated_invite_code = models.CharField(max_length=6, null=True, blank=True, default=None, verbose_name='активированный инвайт код')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.name:
            super().save(*args, **kwargs)
            self.name = f'user{self.id}'
            super().save()
        else:
            super().save(*args, **kwargs)
