# Generated by Django 3.2.6 on 2022-02-21 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='barangay_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(default='null', max_length=100)),
                ('first_name', models.CharField(default='null', max_length=100)),
                ('middle_name', models.CharField(default='null', max_length=100)),
                ('age', models.IntegerField(default=0)),
                ('birthday', models.DateField(default='0000-01-01')),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], default='null', max_length=100)),
                ('nationality', models.CharField(default='null', max_length=100)),
                ('civil_status', models.CharField(default='null', max_length=100)),
                ('email', models.CharField(default='null', max_length=100)),
                ('contact_num', models.IntegerField(default=0)),
                ('street', models.CharField(default='null', max_length=100)),
                ('city', models.CharField(default='null', max_length=100)),
                ('barangay', models.CharField(default='null', max_length=100)),
                ('province', models.CharField(default='null', max_length=100)),
                ('zip_code', models.CharField(default='null', max_length=100)),
                ('emergency_name', models.CharField(default='null', max_length=100)),
                ('emergency_contact_num', models.IntegerField(default=0)),
                ('emergency_address', models.CharField(default='null', max_length=100)),
            ],
        ),
    ]
