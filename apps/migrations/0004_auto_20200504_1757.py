# Generated by Django 2.2.12 on 2020-05-04 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_auto_20200504_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='approve',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='request_Status',
        ),
    ]
