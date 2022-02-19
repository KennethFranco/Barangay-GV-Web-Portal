from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.say_hello),
    path("create_barangay_id/", views.create_barangay_id, name = "create_barangay_id"),
    path("", views.base, name = "base")
]