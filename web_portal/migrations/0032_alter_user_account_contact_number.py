# Generated by Django 3.2.6 on 2022-04-17 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0031_alter_user_account_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='contact_number',
            field=models.IntegerField(default=0, max_length=10),
        ),
    ]
