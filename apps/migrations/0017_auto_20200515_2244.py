# Generated by Django 2.2.12 on 2020-05-15 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0016_subscription_leaverequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='leaveRequest',
            field=models.BooleanField(default=False, verbose_name='Leave Request'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='leaveRequest',
            field=models.BooleanField(default=False, verbose_name='Leave Request'),
        ),
    ]
