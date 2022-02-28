from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name = "base"),
    path("hello/", views.say_hello),
    path("create_barangay_id/", views.create_barangay_id, name = "create_barangay_id"),
    path("create_barangay_certificate/", views.create_barangay_certificate, name = "create_barangay_certificate"),
    path("create_barangay_clearance/", views.create_barangay_clearance, name = "create_barangay_clearance"),
    path("create_certificate_of_indigency/", views.create_certificate_of_indigency, name = "create_certificate_of_indigency"),
]