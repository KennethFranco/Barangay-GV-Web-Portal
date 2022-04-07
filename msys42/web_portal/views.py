from winreg import REG_QWORD
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import barangay_certificate, barangay_id, announcement, certificate_of_indigency, barangay_clearance
from django.core import serializers

# Create your views here.

# ADMIN
def admin_base (request):
    return render(request, 'admin_base.html')

def admin_documents_list (request): 
    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids = ids1 | ids2 | ids3

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    clearances = cl1 | cl2 | cl3

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    cois = ci1 | ci2 | ci3

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    certificates = ce1 | ce2 | ce3
    context = {
        # order by date submitted
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
        "cois": cois.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_documents_list.html', context)

def admin_indiviudal_document (request, pk):

    return render(request, "admin_individual_document.html")

def admin_individual_barangay_id(request,pk):
    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

def admin_update_status_barangay_id_to_printed(request, pk):
    barangay_id.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

def print_barangay_id_constituent(request, pk):
    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "print_barangay_id_constituent.html", context)

def admin_individual_barangay_clearance(request,pk):
    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

def admin_individual_certificate_of_indigency(request,pk):
    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

def admin_individual_barangay_certificate(request, pk):
    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificate.html", context)

def admin_individual_id(request):
    return render(request, "admin_individual_id.html")

def admin_individual_id(request):
    return render(request, "admin_individual_id.html")

def admin_printed_documents (request): 
    return render(request, 'admin_printed_documents.html')

def admin_manage_announcements (request): 
    return render(request, 'admin_manage_announcements.html')

def admin_create_announcements (request): 
    return render(request, 'admin_create_announcements.html')




# USER

def base(request):
    context = {
        "barangay_id_form": barangay_id.objects.all(),
        "announcements": announcement.objects.all(),
    }
    return render(request, "base.html", context)

def say_hello(request):
    return render(request, "base.html")

def create_barangay_certificate(request):
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificateIndigency": certificate_of_indigency.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }
    if (request.method == "POST"):
        barangay_certificate_type = "Barangay Certificate"
        document_id = "02-" + str(date.today().year) + "-" + request.POST.get("document_id")
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

        government_id_or_letter = request.POST.get("first_file")
        personal_photo = request.POST.get("third_file")

        type = request.POST.get("barangay_certificate_type")

        barangay_certificate.objects.create(
            barangay_certificate_type = barangay_certificate_type,
            document_id = document_id,
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
            personal_photo = personal_photo,
            government_id_or_letter = government_id_or_letter,
            type = type,
            status = "Submitted",
            ) 
        return redirect("base")
    else:
        return render(request, "barangay_certificate_form.html", context)

def create_barangay_clearance(request):
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificateIndigency": certificate_of_indigency.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }
    if (request.method == "POST"):
        barangay_clearance_type = "Barangay Clearance"
        document_id = "01-" + str(date.today().year) + "-" + request.POST.get("document_id")
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

        government_id_or_letter = request.POST.get("first_file")
        personal_photo = request.POST.get("third_file")

        type = request.POST.get("barangay_clearance_type")

        barangay_clearance.objects.create(
            barangay_clearance_type = barangay_clearance_type,
            document_id = document_id,
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
            personal_photo = personal_photo,
            government_id_or_letter = government_id_or_letter,
            type = type,
            status = "Submitted",
            ) 
        return redirect("base")
    else:
        return render(request, "barangay_clearance_form.html", context)

def create_certificate_of_indigency(request):
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificateIndigency": certificate_of_indigency.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }
    if (request.method == "POST"):
        document_id = "03-" + str(date.today().year) + "-" + request.POST.get("document_id")
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

        government_id_or_letter = request.POST.get("first_file")
        personal_photo = request.POST.get("third_file")

        certificate_of_indigency.objects.create(
            document_id = document_id,
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
            government_id_or_letter = government_id_or_letter,
            personal_photo = personal_photo,
            status = "Submitted",) 
        return redirect("base")
    else:
        return render(request, "certificate_of_indigency_form.html", context)


def create_barangay_id(request):
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificateIndigency": certificate_of_indigency.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }
    if (request.method == "POST"):
        document_type = "Barangay ID"
        document_id = str(date.today().year) + "-" + str(date.today().month) + "-" + request.POST.get("document_id")
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

        type = request.POST.get("barangay_id_type")

        landlord_name = request.POST.get("landlord_name")
        landlord_contact_number = request.POST.get("landlord_contact_number")
        landlord_address = request.POST.get("landlord_address")

        barangay_id.objects.create(
            document_type = document_type,
            document_id = document_id,
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
            type = type,
            landlord_name = landlord_name,
            landlord_address = landlord_address,
            landlord_contact_number = landlord_contact_number,
            status = "Submitted",
            ) 
        return redirect("base")
    else:
        return render(request, "barangay_id_form.html", context)

# def barangay_ids(request):
#     barangay_id_objects = barangay_id.objects.all()
#     return render(request, "base.html", {'barangay_ids': barangay_id_objects})

def admin_create_announcements(request):
    context = {
        "announcements": announcement.objects.all(),
    }
    if (request.method =="POST"):
        title = request.POST.get("title")
        content = request.POST.get("content")

        announcement.objects.create(
            title = title,
            content = content,
        )
        return redirect("admin_manage_announcements")

    else:
        return render(request, "admin_create_announcements.html", context)