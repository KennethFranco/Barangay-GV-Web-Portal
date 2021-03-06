# Generated by Django 3.2.6 on 2022-02-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0002_auto_20220221_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay_id',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='barangay',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='city',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='civil_status',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='contact_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='email',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='emergency_address',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='emergency_contact_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='emergency_name',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='middle_name',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='nationality',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='province',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='street',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='barangay_id',
            name='zip_code',
            field=models.CharField(default='null', max_length=100),
        ),
    ]
