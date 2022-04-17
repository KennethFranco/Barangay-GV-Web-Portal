from multiprocessing import context
from winreg import REG_QWORD
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import barangay_certificate, barangay_id, announcement, certificate_of_indigency, barangay_clearance, admin_account
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string
from twilio.rest import Client
from sms import send_sms

# Create your views here.

# ADMIN

def admin_logout(request): 
    print("ENTERING LOGOUT FUNCTION")
    logout(request)
    return redirect('/web_portal/admin_login/')

def admin_login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            return redirect('/web_portal/documents_list/')
        else: 
            messages.warning(request, "Username or Password is incorrect ")

    return render(request, 'admin_login.html')

@staff_member_required
def admin_base (request):
    return render(request, 'admin_base.html')

@staff_member_required
def admin_account_information (request): 
    context = {
        'user': request.user,
    }
    user = request.user
    if (request.method == "POST"):
        age = request.POST.get("age")
        contact_number = request.POST.get("contact_number")
        birthday = request.POST.get("birthday")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if (User.objects.get(id=user.id) == None):
            print("USER ID IS NULL")    
            admin_account.objects.create(
            user = User.objects.get(id=user.id),
            age = age,
            contact_number = contact_number,
            birthday = birthday,
            ) 
        else:
            print("USER EXISTS")
            admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(age=age)
            admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(contact_number=contact_number)
            admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)
        
        User.objects.all().filter(id=user.id).update(first_name=first_name)
        User.objects.all().filter(id=user.id).update(last_name=last_name)

        return redirect("/web_portal/account_information")

    return render(request, 'admin_account_information.html', context)

@staff_member_required
def admin_documents_list (request): 

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids = ids1 | ids2 | ids3

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    clearances = cl1 | cl2 | cl3

    # ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    # ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    # ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    # cois = ci1 | ci2 | ci3

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    certificates = ce1 | ce2 | ce3
    
    context = {    
        # order by date submitted
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        # "cois": cois.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
        
    }

    return render(request, 'admin_documents_list.html', context)

@staff_member_required
def admin_indiviudal_document (request, pk):

    return render(request, "admin_individual_document.html")

@staff_member_required
def admin_individual_barangay_id(request,pk):
    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_id.objects.all().filter(pk=pk).update(status="Review Completed")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_documents_list")

    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_pre_filled_template_verified(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_id.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_documents_list")

    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_printed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        
        barangay_id.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        print(latest_contributor)

        # email notification
        currentObject =  barangay_id.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay ID#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Due Notice"
        emailBody = 'Good day, this is to notify you that your document request #' +  doc_id + " is now due for payment. Please settle this as soon as possible to proceed with your application."

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("admin_documents_list")

    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)


@staff_member_required
def print_barangay_id_constituent(request, pk):
    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "print_barangay_id_constituent.html", context)

@staff_member_required
def admin_individual_barangay_clearance(request,pk):
    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

@staff_member_required
def admin_individual_certificate_of_indigency(request,pk):
    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

@staff_member_required
def admin_individual_barangay_certificate(request, pk):
    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificate.html", context)

@staff_member_required
def admin_individual_id(request):
    return render(request, "admin_individual_id.html")

@staff_member_required
def admin_individual_id(request):
    return render(request, "admin_individual_id.html")

@staff_member_required
def admin_printed_documents (request): 
    ids1 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids2 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids3 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3

    cl1 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl2 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl3 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3

    ci1 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    cois = ci1 | ci2 | ci3

    ce1 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce2 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce3 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3
    context = {    
        # order by date submitted
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
        "cois": cois.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_printed_documents.html', context)

def admin_manage_announcements (request): 
    return render(request, 'admin_manage_announcements.html')

def admin_create_announcements (request): 
    return render(request, 'admin_create_announcements.html')




# USER

def base(request):
    context = {
        "barangay_id_form": barangay_id.objects.all(),
        "announcements": announcement.objects.all(),
        "user": request.user
    }
    return render(request, "base.html", context)

def say_hello(request):
    return render(request, "base.html")

def user_logout(request): 
    print("ENTERING LOGOUT FUNCTION")
    logout(request)
    return redirect('/web_portal')

def user_login(request):
    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            print(username)
            print(password)
            return redirect('/web_portal/')
        else: 
            messages.warning(request, "Username or Password is incorrect")

    return render(request, 'user_login.html')

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
        if (landlord_name == ""):
            landlord_name = "null"
        
        landlord_contact_number = request.POST.get("landlord_contact_number")
        if (landlord_contact_number == ""):
            landlord_contact_number = "null"
        
        landlord_address = request.POST.get("landlord_address")
        if (landlord_address == ""):
            landlord_address = "null"

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
            status = "Submitted for Review",
            latest_contributor = "System",
            date_submitted = date.today(),
            )
        global current_document_id
        current_document_id = document_id

        emailSubject = 'Barangay ID#' + current_document_id + " Request from " + last_name + ", " + first_name
        emailBody = 'Good day, this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at URL for updates."

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        account_sid = 'ACab503ab8dea552d21d83e1137db95ea8'
        auth_token = 'abd486fb93e4cc627bb11dede5438320'
        client = Client(account_sid, auth_token)


        messageBody = "Hello, this is to confirm that your document request #" + current_document_id + " has been submitted. Please regularly check on it."
        number = '+63' + contact_num

        message = client.messages.create(
        body= messageBody,
        from_='+19124913021',
        to= '+639088178530'
        )

        # send_sms(
        #     messageBody,
        #     '+639088178530',
        #     [number],
        #     fail_silently=False
        # )

        print(message.sid)
        return redirect("document_success_page")
    else:
        return render(request, "barangay_id_form.html", context)

def document_success_page(request):
    document_id = current_document_id
    print(document_id)
    context = {
        "document_id": document_id
    }
    return render(request, "document_success_page.html", context)

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