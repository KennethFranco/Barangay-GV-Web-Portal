# Generated by Django 3.2.6 on 2022-05-13 09:41

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0059_auto_20220513_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay_certificate',
            name='government_id_or_letter',
            field=models.FileField(default='null', storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='barangay_certificate',
            name='personal_photo',
            field=models.FileField(default='null', storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='barangay_certificate',
            name='proof_of_payment',
            field=models.FileField(default='null', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
    ]
