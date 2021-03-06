from django.contrib import admin
from .models import admin_account, certificate_of_indigency, user_account, announcement, barangay_id, barangay_certificate, barangay_clearance, inquiry

# Register your models here.
admin.site.register(barangay_id)
admin.site.register(announcement)
admin.site.register(barangay_certificate)
admin.site.register(barangay_clearance)
admin.site.register(certificate_of_indigency)
admin.site.register(admin_account)
admin.site.register(user_account)
admin.site.register(inquiry)