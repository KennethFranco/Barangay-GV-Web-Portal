from django.contrib import admin
from .models import admin_account, announcement, barangay_id, certificate_of_indigency, barangay_certificate, barangay_clearance

# Register your models here.
admin.site.register(barangay_id)
admin.site.register(announcement)
admin.site.register(certificate_of_indigency)
admin.site.register(barangay_certificate)
admin.site.register(barangay_clearance)
admin.site.register(admin_account)
