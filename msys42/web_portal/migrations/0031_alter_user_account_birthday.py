# Generated by Django 3.2.6 on 2022-04-17 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0030_user_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='birthday',
            field=models.DateTimeField(default='2022-01-01'),
        ),
    ]
