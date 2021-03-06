# Generated by Django 2.2.12 on 2020-05-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20200512_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='currentFamilySize',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Current Family Size'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='total_slots',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0, verbose_name='Total Available Slots'),
        ),
    ]
