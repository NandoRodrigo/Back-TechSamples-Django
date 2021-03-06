# Generated by Django 4.0.3 on 2022-03-21 13:50

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
            name='Analysis',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('batch', models.IntegerField(unique=True)),
                ('made', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(max_length=255)),
                ('is_concluded', models.BooleanField(default=False)),
                ('analyst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
