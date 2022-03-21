# Generated by Django 4.0.2 on 2022-02-28 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0017_remove_barangay_clearance_emergency_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barangay_certificate',
            name='voters_id',
        ),
        migrations.RemoveField(
            model_name='barangay_clearance',
            name='voters_id',
        ),
        migrations.RemoveField(
            model_name='certificate_of_indigency',
            name='voters_id',
        ),
        migrations.AlterField(
            model_name='barangay_id',
            name='government_id_or_letter',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]