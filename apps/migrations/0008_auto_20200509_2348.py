# Generated by Django 2.2.12 on 2020-05-09 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20200504_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='status',
            field=models.CharField(choices=[('Inactive', 'Joined'), ('Pending', 'Pending Admin Approval'), ('Active', 'Approve'), ('Ship', 'Shipment'), ('Approved', 'Activate')], default='Inactive', max_length=15, verbose_name='Plan Status'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('Inactive', 'Joined'), ('Pending', 'Pending Admin Approval'), ('Active', 'Approve'), ('Ship', 'Shipment'), ('Approved', 'Activate')], default='Inactive', max_length=15, verbose_name='Subscription Status'),
        ),
    ]
