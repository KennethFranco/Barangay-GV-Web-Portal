# Generated by Django 4.0.2 on 2022-02-28 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0016_barangay_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barangay_clearance',
            name='emergency_address',
        ),
        migrations.RemoveField(
            model_name='barangay_clearance',
            name='emergency_contact_num',
        ),
        migrations.RemoveField(
            model_name='barangay_clearance',
            name='emergency_name',
        ),
    ]
