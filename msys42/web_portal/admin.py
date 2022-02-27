from django.contrib import admin
from .models import announcement, barangay_id, certificate_of_indigency

# Register your models here.
admin.site.register(barangay_id)
admin.site.register(announcement)
admin.site.register(certificate_of_indigency)
