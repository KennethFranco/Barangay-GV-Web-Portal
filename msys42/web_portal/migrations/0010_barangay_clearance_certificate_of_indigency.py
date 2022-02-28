# Generated by Django 4.0.2 on 2022-02-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0009_barangay_id_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='barangay_clearance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default='null', max_length=100)),
                ('first_name', models.CharField(default='null', max_length=100)),
                ('middle_name', models.CharField(default='null', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('birthday', models.DateField(default='2022-01-01')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], default='null', max_length=100)),
                ('nationality', models.CharField(default='null', max_length=100)),
                ('civil_status', models.CharField(default='null', max_length=100)),
                ('email', models.CharField(default='null', max_length=100)),
                ('contact_num', models.CharField(default='null', max_length=100)),
                ('street', models.CharField(default='null', max_length=100)),
                ('city', models.CharField(default='null', max_length=100)),
                ('barangay', models.CharField(default='null', max_length=100)),
                ('province', models.CharField(default='null', max_length=100)),
                ('zip_code', models.CharField(default='null', max_length=100)),
                ('emergency_name', models.CharField(default='null', max_length=100)),
                ('emergency_contact_num', models.IntegerField(default=0)),
                ('emergency_address', models.CharField(default='null', max_length=100)),
                ('government_id_or_letter', models.FileField(default='null', upload_to='')),
                ('voters_id', models.FileField(default='null', upload_to='')),
                ('status', models.CharField(choices=[('Submitted', 'Submitted'), ('Under Review', 'Under Review')], default='null', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='certificate_of_indigency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default='null', max_length=100)),
                ('first_name', models.CharField(default='null', max_length=100)),
                ('middle_name', models.CharField(default='null', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('birthday', models.DateField(default='2022-01-01')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], default='null', max_length=100)),
                ('nationality', models.CharField(default='null', max_length=100)),
                ('civil_status', models.CharField(default='null', max_length=100)),
                ('email', models.CharField(default='null', max_length=100)),
                ('contact_num', models.CharField(default='null', max_length=100)),
                ('street', models.CharField(default='null', max_length=100)),
                ('city', models.CharField(default='null', max_length=100)),
                ('barangay', models.CharField(default='null', max_length=100)),
                ('province', models.CharField(default='null', max_length=100)),
                ('zip_code', models.CharField(default='null', max_length=100)),
                ('government_id_or_letter', models.FileField(default='null', upload_to='')),
                ('voters_id', models.FileField(default='null', upload_to='')),
                ('status', models.CharField(choices=[('Submitted', 'Submitted'), ('Under Review', 'Under Review')], default='null', max_length=100)),
            ],
        ),
    ]
