# Generated by Django 3.2.6 on 2022-05-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0062_auto_20220520_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_account',
            name='blood_type',
            field=models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], default='null', max_length=100),
        ),
    ]