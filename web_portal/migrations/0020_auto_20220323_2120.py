# Generated by Django 3.2.6 on 2022-03-23 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0019_auto_20220323_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay_certificate',
            name='date_submitted',
            field=models.DateField(default='2022-01-01'),
        ),
        migrations.AddField(
            model_name='barangay_clearance',
            name='date_submitted',
            field=models.DateField(default='2022-01-01'),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='date_submitted',
            field=models.DateField(default='2022-01-01'),
        ),
        migrations.AddField(
            model_name='certificate_of_indigency',
            name='date_submitted',
            field=models.DateField(default='2022-01-01'),
        ),
    ]