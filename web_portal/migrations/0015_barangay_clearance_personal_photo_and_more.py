# Generated by Django 4.0.2 on 2022-02-28 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0014_auto_20220228_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay_clearance',
            name='personal_photo',
            field=models.FileField(default='null', upload_to=''),
        ),
        migrations.AddField(
            model_name='certificate_of_indigency',
            name='personal_photo',
            field=models.FileField(default='null', upload_to=''),
        ),
    ]
