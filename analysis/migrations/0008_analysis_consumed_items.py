# Generated by Django 4.0.3 on 2022-03-30 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_analysis_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='consumed_items',
            field=models.JSONField(null=True),
        ),
    ]