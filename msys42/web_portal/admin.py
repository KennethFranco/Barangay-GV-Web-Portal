from django.contrib import admin
from .models import announcement, barangay_id

# Register your models here.
admin.site.register(barangay_id)
admin.site.register(announcement)
