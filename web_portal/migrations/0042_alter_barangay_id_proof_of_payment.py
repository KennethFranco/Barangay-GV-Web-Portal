# Generated by Django 3.2.6 on 2022-04-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0041_alter_certificate_of_indigency_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay_id',
            name='proof_of_payment',
            field=models.FileField(default='null', null=True, upload_to=''),
        ),
    ]
