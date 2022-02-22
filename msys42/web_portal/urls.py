from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name = "base"),
    path("hello/", views.say_hello),
    path("barangay_id_form/", views.barangay_id_form, name = "barangay_id_form"),
    path("create_barangay_id/", views.create_barangay_id, name = "create_barangay_id"),
    
]