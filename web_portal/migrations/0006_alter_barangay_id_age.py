# Generated by Django 3.2.6 on 2022-02-23 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0005_barangay_id_government_id_or_letter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay_id',
            name='age',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
