from django.db import models

# Create your models here.
class barangay_id(models.Model):
    # Personal Details
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    middle_name = models.CharField(max_length = 100, default="null")
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")
    contact_num = models.IntegerField(default = 0)
    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")
    # Emergency Contact 
    emergency_name = models.CharField(max_length = 100, default="null")
    emergency_contact_num = models.IntegerField(default = 0)
    emergency_address = models.CharField(max_length = 100, default="null")
    objects = models.Manager()

class announcement(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 1000)
    objects = models.Manager()