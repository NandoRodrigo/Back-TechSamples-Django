# Generated by Django 4.0.3 on 2022-03-31 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0008_analysis_consumed_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
