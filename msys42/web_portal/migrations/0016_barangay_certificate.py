# Generated by Django 4.0.2 on 2022-02-28 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_portal', '0015_barangay_clearance_personal_photo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='barangay_certificate',
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
                ('voters_id', models.FileField(null=True, upload_to='')),
                ('personal_photo', models.FileField(default='null', upload_to='')),
                ('type', models.CharField(choices=[('Bonafide', 'Bonafide'), ('Transient', 'Transient')], default='null', max_length=100)),
                ('status', models.CharField(choices=[('Submitted', 'Submitted'), ('Under Review', 'Under Review')], default='null', max_length=100)),
            ],
        ),
    ]
