# Generated by Django 3.2.6 on 2022-04-17 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_portal', '0027_auto_20220416_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin_account',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='admin_account',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='admin_account',
            name='password',
        ),
        migrations.RemoveField(
            model_name='admin_account',
            name='username',
        ),
        migrations.AddField(
            model_name='admin_account',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='admin_account',
            name='birthday',
            field=models.DateField(default='2022-01-01'),
        ),
        migrations.AddField(
            model_name='admin_account',
            name='contact_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='admin_account',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]