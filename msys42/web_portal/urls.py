from django.urls import path
from . import views

urlpatterns = [
    path("", views.base, name = "base"),
    path("hello/", views.say_hello),
    path("barangay_id_form/", views.barangay_id_form, name = "barangay_id_form"),
    
]