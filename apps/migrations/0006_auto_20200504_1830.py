# Generated by Django 2.2.12 on 2020-05-04 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_subscription_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='cancel_subs',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='feedback',
        ),
    ]
