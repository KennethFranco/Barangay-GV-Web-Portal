# Generated by Django 4.0.2 on 2022-02-24 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0007_alter_barangay_id_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barangay_id',
            name='contact_num',
            field=models.CharField(default='null', max_length=100),
        ),
    ]