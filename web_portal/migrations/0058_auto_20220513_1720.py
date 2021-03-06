# Generated by Django 3.2.6 on 2022-05-13 09:20

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0057_alter_barangay_id_proof_of_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default='null', max_length=100)),
                ('first_name', models.CharField(default='null', max_length=100)),
                ('email', models.CharField(default='null', max_length=100)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='barangay_clearance',
            name='government_id_or_letter',
            field=models.FileField(default='null', storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='barangay_clearance',
            name='personal_photo',
            field=models.FileField(default='null', storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
        migrations.AlterField(
            model_name='barangay_clearance',
            name='proof_of_payment',
            field=models.FileField(default='null', null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to=''),
        ),
    ]
