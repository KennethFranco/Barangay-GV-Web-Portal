# Generated by Django 3.2.6 on 2022-04-09 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0023_auto_20220407_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='admin_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
            ],
        ),
    ]