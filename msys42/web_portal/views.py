from winreg import REG_QWORD
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import barangay_id, announcement

# Create your views here.
def base(request):
    context = {
        "barangay_id_form": barangay_id.objects.all(),
        "announcements": announcement.objects.all()
    }
    return render(request, "base.html", context)

def say_hello(request):
    return render(request, "base.html")

def barangay_id_form(request):
    if (request.method == "POST"):
        ln = request.POST.get('last_name')
        fn = request.POST.get('first_name')
        barangay_id.objects.create(last_name = ln, first_name= fn) 
        return redirect("base")
    else:
        return render(request, "barangay_id_form.html")

def create_barangay_id(request):
    if (request.method == "POST"):
        # Personal Details
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get('middle_name')
        age = request.POST.get("age")
        birthday = request.POST.get("birthday")
        sex = request.POST.get("sex")
        nationality = request.POST.get("nationality")
        civil_status = request.POST.get("civil_status")
        email = request.POST.get("email")
        contact_num = request.POST.get("contact_number")

        street = request.POST.get("address_first_line")
        city = request.POST.get("address_city")
        barangay = request.POST.get("address_barangay")
        zip_code = request.POST.get("address_zip_code")
        province = request.POST.get("address_province")

        emergency_name = request.POST.get("emergency_name")
        emergency_contact_num = request.POST.get("emergency_contact_number")
        emergency_address = request.POST.get("emergency_address")

        
        government_id_or_letter = request.POST.get("first_file")
        voters_id = request.POST.get("second_file")
        personal_photo = request.POST.get("third_file")

        barangay_id.objects.create(
            # Personal Info
            last_name = last_name,
            first_name = first_name,
            middle_name = middle_name,
            age = age,
            birthday = birthday,
            sex = sex,
            nationality = nationality,
            civil_status = civil_status,
            email = email,
            contact_num = contact_num,
            street = street,
            city = city,
            barangay = barangay,
            province= province,
            zip_code = zip_code,
            emergency_name = emergency_name,
            emergency_contact_num = emergency_contact_num,
            emergency_address = emergency_address,
            personal_photo = personal_photo,
            government_id_or_letter = government_id_or_letter,
            voters_id = voters_id,
            ) 
        return redirect("base")
    else:
        return render(request, "barangay_id_form.html")

# def barangay_ids(request):
#     barangay_id_objects = barangay_id.objects.all()
#     return render(request, "base.html", {'barangay_ids': barangay_id_objects})