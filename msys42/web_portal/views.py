from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import barangay_id, announcement

# Create your views here.
def base(request):
    context = {
        "barangay_ids": barangay_id.objects.all(),
        "announcements": announcement.objects.all()
    }
    return render(request, "base.html", context)

def say_hello(request):
    return render(request, "hello.html")

def create_barangay_id(request):
    if (request.method == "POST"):
        ln = request.POST.get('last_name')
        fn = request.POST.get('first_name')
        barangay_id.objects.create(last_name = ln, first_name= fn) 
        return redirect("hello/")
    else:
        return render(request, "hello.html")

def barangay_ids(request):
    barangay_id_objects = barangay_id.objects.all()
    return render(request, "base.html", {'barangay_ids': barangay_id_objects})