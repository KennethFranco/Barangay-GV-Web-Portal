from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello),
    path("barangay_id_form/", views.barangay_id_form, name = "barangay_id_form"),
    path("", views.base, name = "base")
]