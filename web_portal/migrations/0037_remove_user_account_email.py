# Generated by Django 3.2.6 on 2022-04-23 13:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0036_certificate_of_indigency'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_account',
            name='email',
        ),
    ]
