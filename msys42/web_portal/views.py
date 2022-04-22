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

import io
from django.http import FileResponse
import reportlab
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.utils import ImageReader

def some_view(request):
    if (request.method == 'POST'):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        pdf.drawString(100, 100, "Hello world.")
        pdf.drawString(100,810, 'x100')
        pdf.drawString(200,810, 'x200')
        pdf.drawString(300,810, 'x300')
        pdf.drawString(400,810, 'x400')
        pdf.drawString(500,810, 'x500')

        pdf.drawString(10,100, 'y100')
        pdf.drawString(10,200, 'y200')
        pdf.drawString(10,300, 'y300')
        pdf.drawString(10,400, 'y400')
        pdf.drawString(10,500, 'y500')
        pdf.drawString(10,600, 'y600')
        pdf.drawString(10,700, 'y700')
        pdf.drawString(10,800, 'y800')  

        for font in pdf.getAvailableFonts():
            print(font)

        pdf.setFont('Times-Roman', 14)
        pdf.drawString(270, 770, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(270, 670, "CERTIFICATION")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(270, 500, "TO WHOM IT MAY CONCERN:")

        logo = ImageReader('data:image/jpeg;base64,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')
        pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

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

def user_register(request): 
    return render(request, 'user_register.html')

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

def document_tracker(request):
    if (request.method == 'POST'):
        searched = request.POST.get("searched")

        ids = barangay_id.objects.filter(document_id = searched)
        clearances = barangay_clearance.objects.filter(document_id = searched)
        cois = certificate_of_indigency.objects.filter(document_id = searched)
        certificates = barangay_certificate.objects.filter(document_id = searched)

        print(clearances)
        context = {
            "ids": ids,
            "clearances": clearances,
            "cois": cois,
            "certificates": certificates,
            "searched": searched,
        }
        return render(request, 'document_tracker.html', context)
    else:
        return render(request, 'document_tracker.html')

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