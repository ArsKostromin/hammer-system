# Generated by Django 5.1.4 on 2024-12-25 22:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_customuser_activated_invite_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='invitees',
            field=models.ManyToManyField(blank=True, related_name='invited_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
