# Generated by Django 4.1.5 on 2023-01-26 22:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Corporate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('core_id', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MessageType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(max_length=15, unique=True)),
                ('en', models.TextField(max_length=1500)),
                ('sw', models.TextField(blank=True, max_length=1500, null=True)),
                ('fr', models.TextField(blank=True, max_length=1500, null=True)),
                ('editable', models.BooleanField(default=False)),
                ('message_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.messagetype')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('send_url', models.CharField(blank=True, max_length=200, null=True)),
                ('balance_url', models.CharField(blank=True, max_length=200, null=True)),
                ('sms_token_url', models.CharField(blank=True, max_length=255, null=True)),
                ('send_callback', models.CharField(blank=True, help_text='send sms endpoint', max_length=50, null=True)),
                ('balance_callback', models.CharField(max_length=255)),
                ('key', models.CharField(default=uuid.uuid4, editable=False, max_length=100)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OAuth',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('access_token', models.DateTimeField(default=datetime.datetime(2023, 1, 26, 23, 19, 29, 166308, tzinfo=datetime.timezone.utc))),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.app')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='messagetype',
            name='message_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state'),
        ),
        migrations.CreateModel(
            name='MessageLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('destination', models.CharField(blank=True, max_length=100, null=True)),
                ('message', models.TextField(blank=True, max_length=1500, null=True)),
                ('confirmation_code', models.CharField(blank=True, max_length=60, null=True)),
                ('source_ip', models.CharField(blank=True, max_length=20, null=True)),
                ('request', models.CharField(blank=True, max_length=500, null=True)),
                ('response', models.CharField(blank=True, max_length=250, null=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.app')),
                ('corporate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.corporate')),
                ('message_types', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.messagetype')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='corporate',
            name='provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.provider'),
        ),
        migrations.AddField(
            model_name='corporate',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state'),
        ),
        migrations.CreateModel(
            name='AppCredential',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('sender_id', models.CharField(blank=True, help_text='SMS sender id', max_length=100, null=True)),
                ('sender_code', models.CharField(blank=True, max_length=100, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('org_id', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.CharField(blank=True, help_text='either user id or sender code', max_length=50, null=True)),
                ('balance', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=20, null=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.app')),
                ('corporate', models.ForeignKey(blank=True, help_text="corporate's credentials", max_length=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.corporate')),
                ('message_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.messagetype')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='app',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.state'),
        ),
    ]
