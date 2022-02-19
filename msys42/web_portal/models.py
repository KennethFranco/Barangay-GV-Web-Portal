from django.db import models

# Create your models here.
class barangay_id(models.Model):
    last_name = models.CharField(max_length = 100)
    first_name = models.CharField(max_length = 100)
