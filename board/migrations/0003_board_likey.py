# Generated by Django 3.1 on 2022-01-03 03:01

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='likey',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
