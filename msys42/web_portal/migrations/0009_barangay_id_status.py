# Generated by Django 4.0.2 on 2022-02-24 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0008_alter_barangay_id_contact_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay_id',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Under Review', 'Under Review')], default='null', max_length=100),
        ),
    ]
