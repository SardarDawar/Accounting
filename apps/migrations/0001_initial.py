# Generated by Django 2.2.12 on 2020-05-02 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=150)),
                ('slug', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=150)),
                ('plan_name', models.CharField(max_length=150)),
                ('number_of_open_slots', models.IntegerField(default=0)),
                ('monthly_payment_date', models.CharField(max_length=150)),
                ('currently_monthly_payment_per_line', models.CharField(max_length=150)),
                ('total_slots', models.IntegerField(default=0, verbose_name='Total Fixed Slots')),
                ('linkWeb', models.URLField(blank=True, default='', null=True)),
                ('notes', models.TextField(blank=True, default='', max_length=500, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('approve', models.BooleanField(blank=True, default=False, null=True, verbose_name='Approve Plan')),
                ('request_Status', models.BooleanField(blank=True, default=False, null=True, verbose_name='Request to Cancel')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_slots', models.IntegerField(default=0, verbose_name='Number of Slots')),
                ('TotalAmount', models.IntegerField(default=0, verbose_name='Total Amount')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('approved', models.BooleanField(blank=True, default=False, null=True, verbose_name='Approve Subscription')),
                ('cancel_subs', models.BooleanField(blank=True, default=False, null=True, verbose_name='Request To Cancel')),
                ('feedback', models.TextField(blank=True, default='', max_length=500, null=True, verbose_name='Feedback')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='profileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contactNumber', models.CharField(blank=True, default='', max_length=14, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
            },
        ),
        migrations.CreateModel(
            name='commentPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(default='', max_length=300, null=True, verbose_name='Commment Body')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]