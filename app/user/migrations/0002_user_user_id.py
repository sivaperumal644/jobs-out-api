# Generated by Django 3.2 on 2021-06-13 05:56

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.uuid4, null=True),
        ),
    ]