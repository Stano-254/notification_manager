# Generated by Django 4.1.5 on 2023-01-26 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauth',
            name='access_token',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 30, 33, 185161, tzinfo=datetime.timezone.utc)),
        ),
    ]
