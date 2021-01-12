# Generated by Django 3.1.5 on 2021-01-12 17:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210112_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquiry',
            name='message',
            field=models.TextField(max_length=5000, validators=[django.core.validators.MaxLengthValidator(5000)]),
        ),
    ]
