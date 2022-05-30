from multiprocessing import context
from datetime import date
import re
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import barangay_certificate, barangay_id, announcement, barangay_clearance, admin_account, certificate_of_indigency, user_account, inquiry
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.

def faqs(request):
    return render(request, 'faqs.html')
    
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

    print(user)
    print(admin_account.objects.all().filter(user=user.id).exists())
    if (request.method == "POST"):
        age = request.POST.get("age")
        contact_number = request.POST.get("contact_number")
        birthday = request.POST.get("birthday")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if (admin_account.objects.all().filter(user=user.id).exists()):
            print("USER ID IS NULL")    
            admin_account.objects.create(
            user = User.objects.get(id=user.id),
            age = age,
            contact_number = contact_number,
            birthday = birthday,
            ) 

            User.objects.all().filter(id=user.id).update(first_name=first_name)
            User.objects.all().filter(id=user.id).update(last_name=last_name)
            User.objects.all().filter(id=user.id).update(email=email)
        else:
            emailQuery = User.objects.all().filter(email=email)
            contactNumQuery = admin_account.objects.all().filter(contact_number=contact_number)

            if emailQuery.exists():
                print("EMAIL EXISTS")
                messages.warning(request, 'The email you submitted already has an account. Please use a different email.')
            elif contactNumQuery.exists():
                print("PHONE NUMBER EXISTS")
                messages.warning(request, 'The phone number you submitted already exists. Please use a different phone number.')
            else:
                print("USER EXISTS")
                admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(age=age)
                admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(contact_number=contact_number)
                admin_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)

                User.objects.all().filter(id=user.id).update(first_name=first_name)
                User.objects.all().filter(id=user.id).update(last_name=last_name)
                User.objects.all().filter(id=user.id).update(email=email)

        return redirect("/web_portal/admin_account_information")

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

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    certificates = ce1 | ce2 | ce3

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    indigencies = ci1 | ci2 | ci3

    context = {    
        # order by date submitted
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
        # "LODS": certificate_of_indigency.objects.all(),
        "indigencies": indigencies.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_documents_list.html', context)

@staff_member_required
def admin_inactive_documents_list(request):
    ids1 = barangay_id.objects.all().filter(status = "Rejected")
    ids2 = barangay_id.objects.all().filter(status = "Delivered/Picked-up")
    ids = ids1 | ids2

    cl1 = barangay_clearance.objects.all().filter(status = "Rejected")
    cl2 = barangay_clearance.objects.all().filter(status = "Delivered/Picked-up")
    clearances = cl1 | cl2
    ce1 = barangay_certificate.objects.all().filter(status = "Rejected")
    ce2 = barangay_certificate.objects.all().filter(status = "Delivered/Picked-up")
    certificates = ce1 | ce2

    ci1 = certificate_of_indigency.objects.all().filter(status = "Rejected")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Delivered/Picked-up")
    indigencies = ci1 | ci2

    lods = "HELO"
    print("LODS")
    print(indigencies)
    
    context = {    
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
        "indigencies": indigencies.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_inactive_documents_list.html', context)

@staff_member_required
def admin_all_documents_list(request):
    ids1 = barangay_id.objects.all()
    cl1 = barangay_clearance.objects.all()
    ce1 = barangay_certificate.objects.all()
    ci1 = certificate_of_indigency.objects.all()


    context = {    
        "ids": ids1.order_by("date_submitted").reverse(),
        "clearances": cl1.order_by("date_submitted").reverse(),
        "certificates": ce1.order_by("date_submitted").reverse(),
        "indigencies": ci1.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_all_documents_list.html', context)


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
def admin_update_status_barangay_id_to_rejected(request, pk):
    if (request.method == "POST"):
        reason_for_rejection = request.POST.get("reason_for_rejection")
        currentObject =  barangay_id.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay ID#' + doc_id + " Request from " + last_name + ", " + first_name + ": Rejection Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " has unfortunately been rejected for the following reasons:\n\n " +  reason_for_rejection + "\n\nFeel free to apply again at our website anytime.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        barangay_id.objects.all().filter(pk=pk).update(status="Rejected")
        detailsString = "Your document has been has unfortunately been rejected due to not meeting certain requirements set by the barangay. Please check your email for the specific reasons(s) and feel free to submit a request again anytime."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)
        return redirect("admin_documents_list")

@staff_member_required
def admin_update_status_barangay_id_back_to_submitted_for_review(request, pk):
    barangay_id.objects.all().filter(pk=pk).update(status="Submitted for Review")
    return redirect("admin_individual_barangay_id", pk=pk)

@staff_member_required
def admin_update_status_barangay_id_back_to_review_completed(request, pk):
    barangay_id.objects.all().filter(pk=pk).update(status="Review Completed")
    return redirect("admin_individual_barangay_id", pk=pk)

@staff_member_required
def admin_update_status_barangay_id_back_to_pre_filled_template_verified(request, pk):
    barangay_id.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
    return redirect("admin_individual_barangay_id", pk=pk)

@staff_member_required
def admin_update_status_barangay_id_back_to_printed(request, pk):
    barangay_id.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
    return redirect("admin_individual_barangay_id", pk=pk)

@staff_member_required
def admin_update_status_barangay_id_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get('middle_name')
        age = request.POST.get("age")
        blood_type = request.POST.get("blood_type")
        birthday = request.POST.get("birthday")
        sex = request.POST.get("sex")
        print(sex)
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

        barangay_id.objects.all().filter(pk=pk).update(status="Review Completed")
        barangay_id.objects.all().filter(pk=pk).update(last_name=last_name)
        barangay_id.objects.all().filter(pk=pk).update(first_name=first_name)
        barangay_id.objects.all().filter(pk=pk).update(middle_name=middle_name)
        barangay_id.objects.all().filter(pk=pk).update(age=age)
        barangay_id.objects.all().filter(pk=pk).update(blood_type=blood_type)
        barangay_id.objects.all().filter(pk=pk).update(birthday=birthday)
        barangay_id.objects.all().filter(pk=pk).update(sex=sex)
        barangay_id.objects.all().filter(pk=pk).update(nationality=nationality)
        barangay_id.objects.all().filter(pk=pk).update(civil_status=civil_status)
        barangay_id.objects.all().filter(pk=pk).update(email=email)
        barangay_id.objects.all().filter(pk=pk).update(contact_num=contact_num)
        barangay_id.objects.all().filter(pk=pk).update(street=street)
        barangay_id.objects.all().filter(pk=pk).update(city=city)
        barangay_id.objects.all().filter(pk=pk).update(barangay=barangay)
        barangay_id.objects.all().filter(pk=pk).update(zip_code=zip_code)
        barangay_id.objects.all().filter(pk=pk).update(province=province)
        barangay_id.objects.all().filter(pk=pk).update(emergency_name=emergency_name)
        barangay_id.objects.all().filter(pk=pk).update(emergency_contact_num=emergency_contact_num)
        barangay_id.objects.all().filter(pk=pk).update(emergency_address=emergency_address)

        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        print(latest_contributor)
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_id", pk=pk)

    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_transient_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get('middle_name')
        age = request.POST.get("age")
        birthday = request.POST.get("birthday")
        sex = request.POST.get("sex")
        print(sex)
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

        landlord_name = request.POST.get("landlord_name")
        landlord_contact_number = request.POST.get("landlord_contact_number")
        landlord_address = request.POST.get("landlord_address")

        barangay_id.objects.all().filter(pk=pk).update(status="Review Completed")
        barangay_id.objects.all().filter(pk=pk).update(last_name=last_name)
        barangay_id.objects.all().filter(pk=pk).update(first_name=first_name)
        barangay_id.objects.all().filter(pk=pk).update(middle_name=middle_name)
        barangay_id.objects.all().filter(pk=pk).update(age=age)
        barangay_id.objects.all().filter(pk=pk).update(birthday=birthday)
        barangay_id.objects.all().filter(pk=pk).update(sex=sex)
        barangay_id.objects.all().filter(pk=pk).update(nationality=nationality)
        barangay_id.objects.all().filter(pk=pk).update(civil_status=civil_status)
        barangay_id.objects.all().filter(pk=pk).update(email=email)
        barangay_id.objects.all().filter(pk=pk).update(contact_num=contact_num)
        barangay_id.objects.all().filter(pk=pk).update(street=street)
        barangay_id.objects.all().filter(pk=pk).update(city=city)
        barangay_id.objects.all().filter(pk=pk).update(barangay=barangay)
        barangay_id.objects.all().filter(pk=pk).update(zip_code=zip_code)
        barangay_id.objects.all().filter(pk=pk).update(province=province)
        barangay_id.objects.all().filter(pk=pk).update(emergency_name=emergency_name)
        barangay_id.objects.all().filter(pk=pk).update(emergency_contact_num=emergency_contact_num)
        barangay_id.objects.all().filter(pk=pk).update(emergency_address=emergency_address)
        barangay_id.objects.all().filter(pk=pk).update(landlord_name=landlord_name)
        barangay_id.objects.all().filter(pk=pk).update(landlord_contact_number=landlord_contact_number)
        barangay_id.objects.all().filter(pk=pk).update(landlord_address=landlord_address)
        
        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_id", pk=pk)

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
        
        detailsString = "The pre-filled template for your document has been verified and will now undergo printing. Please standby for any emails from us regarding payment for your document."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_id", pk=pk)

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
        detailsString = "Your document has been printed and is now due for payment. Please settle this and upload the proof of payment on your document's page at the document tracker"
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

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
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " is now due for payment. Please settle this as soon as possible to proceed with your application.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("admin_individual_barangay_id", pk=pk)

    lia = get_object_or_404(barangay_id, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_paid(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_id.objects.all().filter(pk=pk).update(status="Printed, Paid")

        detailsString = "Payment for your document has been received. Please standby for any emails from us regarding when you can pick this up or have it delivered."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        currentObject =  barangay_id.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay ID#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Received Notice"
        emailBody = 'Good day, \n\nThis is to confirm that your payment for document request #' +  doc_id + " has been received. We will notify you again once your document is ready for delivery/pickup.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_id", pk=pk)
    else:
        return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_out_for_delivery(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_id.objects.all().filter(pk=pk).update(status="Printed, Out for Delivery/Ready for Pickup")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        detailsString = "Your document is now available for pickup/delivery. Please see the email sent to you for more details."
        barangay_id.objects.all().filter(pk=pk).update(additional_details=detailsString)

        currentObject =  barangay_id.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay ID#' + doc_id + " Request from " + last_name + ", " + first_name + ": Out for Delivery/Pickup Notice"
        emailBody = 'Good day, \n\nCongratulations!\n\nThis is to notify you that your document request #' +  doc_id + " is now out for delivery/ready for pickup. You can call us at 9XXXXXXXXX to schedule for a pickup through your preferred courier or pick up the document yourself at the Barangay Hall during work hours. Thank you very much!\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_id", pk=pk)
    else:
        return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_id_to_delivered(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        receipt_date = request.POST.get("receipt_date")
        barangay_id.objects.all().filter(pk=pk).update(status="Delivered/Picked-up")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_id.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        detailString = "Document request completed. Picked up on " + receipt_date
        barangay_id.objects.all().filter(pk=pk).update(additional_details = detailString)
        return redirect("admin_individual_barangay_id", pk=pk)
    else:
        return render(request, "admin_individual_barangay_id.html", context)

@staff_member_required
def admin_update_status_barangay_clearance_to_rejected(request, pk):
    if (request.method == "POST"):
        reason_for_rejection = request.POST.get("reason_for_rejection")
        currentObject =  barangay_clearance.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Clearance#' + doc_id + " Request from " + last_name + ", " + first_name + ": Rejection Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " has unfortunately been rejected for the following reasons:\n " +  reason_for_rejection + "\nFeel free to apply again at our website anytime.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        barangay_clearance.objects.all().filter(pk=pk).update(status="Rejected")
        detailsString = "Your document has been has unfortunately been rejected due to not meeting certain requirements set by the barangay. Please check your email for the specific reasons(s) and feel free to submit a request again anytime."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)
        return redirect("admin_documents_list")

@staff_member_required
def admin_update_status_barangay_clearance_back_to_submitted_for_review(request, pk):
    barangay_clearance.objects.all().filter(pk=pk).update(status="Submitted for Review")
    return redirect("admin_individual_barangay_clearance", pk=pk)

@staff_member_required
def admin_update_status_barangay_clearance_back_to_review_completed(request, pk):
    barangay_clearance.objects.all().filter(pk=pk).update(status="Review Completed")
    return redirect("admin_individual_barangay_clearance", pk=pk)

@staff_member_required
def admin_update_status_barangay_clearance_back_to_pre_filled_template_verified(request, pk):
    barangay_clearance.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
    return redirect("admin_individual_barangay_clearance", pk=pk)

@staff_member_required
def admin_update_status_barangay_clearance_back_to_printed(request, pk):
    barangay_clearance.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
    return redirect("admin_individual_barangay_clearance", pk=pk)

@staff_member_required
def admin_update_status_barangay_clearance_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
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

        barangay_clearance.objects.all().filter(pk=pk).update(status="Review Completed")
        barangay_clearance.objects.all().filter(pk=pk).update(last_name=last_name)
        barangay_clearance.objects.all().filter(pk=pk).update(first_name=first_name)
        barangay_clearance.objects.all().filter(pk=pk).update(middle_name=middle_name)
        barangay_clearance.objects.all().filter(pk=pk).update(age=age)
        barangay_clearance.objects.all().filter(pk=pk).update(birthday=birthday)
        barangay_clearance.objects.all().filter(pk=pk).update(sex=sex)
        barangay_clearance.objects.all().filter(pk=pk).update(nationality=nationality)
        barangay_clearance.objects.all().filter(pk=pk).update(civil_status=civil_status)
        barangay_clearance.objects.all().filter(pk=pk).update(email=email)
        barangay_clearance.objects.all().filter(pk=pk).update(contact_num=contact_num)
        barangay_clearance.objects.all().filter(pk=pk).update(street=street)
        barangay_clearance.objects.all().filter(pk=pk).update(city=city)
        barangay_clearance.objects.all().filter(pk=pk).update(barangay=barangay)
        barangay_clearance.objects.all().filter(pk=pk).update(zip_code=zip_code)
        barangay_clearance.objects.all().filter(pk=pk).update(province=province)
        
        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_clearance", pk=pk)

    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

@staff_member_required
def admin_update_status_barangay_clearance_to_pre_filled_template_verified(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_clearance.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
        
        detailsString = "The pre-filled template for your document has been verified and will now undergo printing. Please standby for any emails from us regarding payment for your document."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_clearance", pk=pk)

    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

@staff_member_required
def admin_print_barangay_clearance_bonafide(request, pk):
    if (request.method == 'POST'):
        currentObject =  barangay_clearance.objects.all().get(pk=pk)

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        # pdf.drawString(100,810, 'x100')
        # pdf.drawString(200,810, 'x200')
        # pdf.drawString(300,810, 'x300')
        # pdf.drawString(400,810, 'x400')
        # pdf.drawString(500,810, 'x500')

        # pdf.drawString(10,100, 'y100')
        # pdf.drawString(10,200, 'y200')
        # pdf.drawString(10,300, 'y300')
        # pdf.drawString(10,400, 'y400')
        # pdf.drawString(10,500, 'y500')
        # pdf.drawString(10,600, 'y600')
        # pdf.drawString(10,700, 'y700')
        # pdf.drawString(10,800, 'y800')  

        for font in pdf.getAvailableFonts():
            print(font)

        pdf.setFont('Times-Roman', 14)
        pdf.drawString(174, 700, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(180, 650, "BARANGAY CLEARANCE")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(100, 600, "TO WHOM IT MAY CONCERN:")
        pdf.drawString(150, 550, "THIS IS TO CERTIFY")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(273, 550, "that _________________________________")
        pdf.drawString(340, 553, currentObject.first_name)
        pdf.drawString(100, 530, "_____________________________ is a bonafide resident with postal or business")
        pdf.drawString(110, 533, currentObject.middle_name + " " + currentObject.last_name)
        pdf.drawString(100, 510, "address at _________________________________________________________ ")
        pdf.drawString(160, 513, currentObject.street + " " + currentObject.province +  " " + currentObject.city + " " + currentObject.barangay)
        pdf.drawString(100, 490, "has been issued this Barangay Permit/ Clearance for the purpose of securing his/her")
        pdf.drawString(100, 470, "_____________________________________________________.")

        pdf.drawString(135, 430, "Given this _______ day of ____________________, 2022 at Barangay Hall,")
        pdf.drawString(100, 410, "Barangay Guadalupe Viejo, Makati City.")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(280, 330, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 12)
        pdf.drawString(340, 316, "Barangay Captain")

        pdf.drawString(100, 270, "New/ Renewal")
        pdf.drawString(250, 270, ":")
        pdf.drawString(100, 250, "O.R. No.")
        pdf.drawString(250, 250, ":")
        pdf.drawString(100, 230, "Brgy. Clearance No.")
        pdf.drawString(250, 230, ":")
        pdf.drawString(100, 210, "Line/ Type of Business")
        pdf.drawString(250, 210, ":")
        pdf.drawString(100, 190, "No. of Years Operating")
        pdf.drawString(250, 190, ":")

        # logo = ImageReader('data:image/jpeg;base64,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')
        # pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@staff_member_required
def admin_print_barangay_clearance_transient(request, pk):
    if (request.method == 'POST'):
        currentObject =  barangay_clearance.objects.all().get(pk=pk)
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
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
        pdf.drawString(174, 700, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(180, 650, "BARANGAY CLEARANCE")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(100, 600, "TO WHOM IT MAY CONCERN:")
        pdf.drawString(150, 550, "THIS IS TO CERTIFY")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(273, 550, "that _________________________________")
        pdf.drawString(340, 553, currentObject.first_name)
        pdf.drawString(100, 530, "____________________________________ is a transient with postal or business")
        pdf.drawString(110, 533, currentObject.middle_name + " " + currentObject.last_name)
        pdf.drawString(100, 510, "address at _________________________________________________________ ")
        pdf.drawString(160, 513, currentObject.street + " " + currentObject.province +  " " + currentObject.city + " " + currentObject.barangay)
        pdf.drawString(100, 490, "has been issued this Barangay Permit/ Clearance for the purpose of securing his/her")
        pdf.drawString(100, 470, "_____________________________________________________.")

        pdf.drawString(135, 430, "Given this _______ day of ____________________, 2022 at Barangay Hall,")
        pdf.drawString(100, 410, "Barangay Guadalupe Viejo, Makati City.")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(280, 330, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 12)
        pdf.drawString(340, 316, "Barangay Captain")

        pdf.drawString(100, 270, "New/ Renewal")
        pdf.drawString(250, 270, ":")
        pdf.drawString(100, 250, "O.R. No.")
        pdf.drawString(250, 250, ":")
        pdf.drawString(100, 230, "Brgy. Clearance No.")
        pdf.drawString(250, 230, ":")
        pdf.drawString(100, 210, "Line/ Type of Business")
        pdf.drawString(250, 210, ":")
        pdf.drawString(100, 190, "No. of Years Operating")
        pdf.drawString(250, 190, ":")

        

        # logo = ImageReader('data:image/jpeg;base64,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')
        # pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@staff_member_required
def admin_update_status_barangay_clearance_to_printed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        
        barangay_clearance.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
        detailsString = "Your document has been printed and is now due for payment. Please settle this and upload the proof of payment on your document's page at the document tracker"
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        print(latest_contributor)

        # email notification
        currentObject =  barangay_clearance.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Clearance#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Due Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " is now due for payment. Please settle this as soon as possible to proceed with your application.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("admin_individual_barangay_clearance", pk=pk)

    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

def upload_proof_of_payment_barangay_clearance(request, pk):
    if (request.method == "POST"):
        proof_of_payment = request.FILES.get("proof_of_payment")
        clearance = barangay_clearance.objects.get(pk=pk)
        clearance.proof_of_payment = proof_of_payment
        clearance.save()

        currentObject = barangay_clearance.objects.all().get(pk=pk)
        global current_document_id
        current_document_id = currentObject.document_id
        return redirect("payment_success")

@staff_member_required
def admin_update_status_barangay_clearance_to_paid(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_clearance.objects.all().filter(pk=pk).update(status="Printed, Paid")

        detailsString = "Payment for your document has been received. Please standby for any emails from us regarding when you can pick this up or have it delivered."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        currentObject =  barangay_clearance.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Clearance#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Received Notice"
        emailBody = 'Good day, \n\nThis is to confirm that your payment for document request #' +  doc_id + " has been received. We will notify you again once your document is ready for delivery/pickup.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_clearance", pk=pk)
    else:
        return render(request, "admin_individual_barangay_clearance.html", context)

@staff_member_required
def admin_update_status_barangay_clearance_to_out_for_delivery(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_clearance.objects.all().filter(pk=pk).update(status="Printed, Out for Delivery/Ready for Pickup")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        detailsString = "Your document is now available for pickup/delivery. Please see the email sent to you for more details."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        currentObject =  barangay_clearance.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Clearance#' + doc_id + " Request from " + last_name + ", " + first_name + ": Out for Delivery/Pickup Notice"
        emailBody = 'Good day, \n\nCongratulations!\nThis is to notify you that your document request #' +  doc_id + " is now out for delivery/ready for pickup. You can call us at 9XXXXXXXXX to schedule for a pickup through your preferred courier or pick up the document yourself at the Barangay Hall during work hours. Thank you very much!\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_clearance", pk=pk)
    else:
        return render(request, "admin_individual_barangay_.html", context)

@staff_member_required
def admin_update_status_barangay_clearance_to_delivered(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        receipt_date = request.POST.get("receipt_date")
        barangay_clearance.objects.all().filter(pk=pk).update(status="Delivered/Picked-up")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        detailString = "Document request completed. Picked up on " + receipt_date
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details = detailString)
        return redirect("admin_individual_barangay_clearance", pk=pk)
    else:
        return render(request, "admin_individual_barangay_clearance.html", context)

def admin_update_status_certificate_of_indigency_to_rejected(request, pk):
    if (request.method == "POST"):
        reason_for_rejection = request.POST.get("reason_for_rejection")
        currentObject =  certificate_of_indigency.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Certificate of Indigency#' + doc_id + " Request from " + last_name + ", " + first_name + ": Rejection Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " has unfortunately been rejected for the following reasons:\n " +  reason_for_rejection + "\nFeel free to apply again at our website anytime.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Rejected")
        detailsString = "Your document has been has unfortunately been rejected due to not meeting certain requirements set by the barangay. Please check your email for the specific reasons(s) and feel free to submit a request again anytime."
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)
        return redirect("admin_documents_list")

# Revert
@staff_member_required
def admin_update_status_certificate_of_indigency_back_to_submitted_for_review(request, pk):
    certificate_of_indigency.objects.all().filter(pk=pk).update(status="Submitted for Review")
    return redirect("admin_individual_certificate_of_indigency", pk=pk)

@staff_member_required
def admin_update_status_certificate_of_indigency_back_to_review_completed(request, pk):
    certificate_of_indigency.objects.all().filter(pk=pk).update(status="Review Completed")
    return redirect("admin_individual_certificate_of_indigency", pk=pk)

@staff_member_required
def admin_update_status_certificate_of_indigency_back_to_pre_filled_template_verified(request, pk):
    certificate_of_indigency.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
    return redirect("admin_individual_certificate_of_indigency", pk=pk)

@staff_member_required
def admin_update_status_certificate_of_indigency_back_to_printed(request, pk):
    certificate_of_indigency.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
    return redirect("admin_individual_certificate_of_indigency", pk=pk)

# u
@staff_member_required
def admin_update_status_certificate_of_indigency_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
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

        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Review Completed")
        certificate_of_indigency.objects.all().filter(pk=pk).update(last_name=last_name)
        certificate_of_indigency.objects.all().filter(pk=pk).update(first_name=first_name)
        certificate_of_indigency.objects.all().filter(pk=pk).update(middle_name=middle_name)
        certificate_of_indigency.objects.all().filter(pk=pk).update(age=age)
        certificate_of_indigency.objects.all().filter(pk=pk).update(birthday=birthday)
        certificate_of_indigency.objects.all().filter(pk=pk).update(sex=sex)
        certificate_of_indigency.objects.all().filter(pk=pk).update(nationality=nationality)
        certificate_of_indigency.objects.all().filter(pk=pk).update(civil_status=civil_status)
        certificate_of_indigency.objects.all().filter(pk=pk).update(email=email)
        certificate_of_indigency.objects.all().filter(pk=pk).update(contact_num=contact_num)
        certificate_of_indigency.objects.all().filter(pk=pk).update(street=street)
        certificate_of_indigency.objects.all().filter(pk=pk).update(city=city)
        certificate_of_indigency.objects.all().filter(pk=pk).update(barangay=barangay)
        certificate_of_indigency.objects.all().filter(pk=pk).update(zip_code=zip_code)
        certificate_of_indigency.objects.all().filter(pk=pk).update(province=province)
        
        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_certificate_of_indigency", pk=pk)

    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

@staff_member_required
def admin_update_status_certificate_of_indigency_to_pre_filled_template_verified(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
        
        detailsString = "The pre-filled template for your document has been verified and will now undergo printing. Please standby for any emails from us regarding payment for your document."
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_certificate_of_indigency", pk=pk)

    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

@staff_member_required
def admin_print_certificate_of_indigency(request, pk):
    if (request.method == 'POST'):
        currentObject =  certificate_of_indigency.objects.all().get(pk=pk)

        last_name =currentObject.last_name
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
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

        # CERTIFICATE OF INDIGENCY
        pdf.setFont('Times-Bold', 9)
        pdf.drawString(215, 760, "GUADALUPE VIEJO COMMUNITY COMPLEX")
        pdf.drawString(210, 750, "GUMAMELA STREET CORNER CAMIA STREET")
        pdf.drawString(195, 740, "GUADALUPE VIEJO, MAKATI CITY PHILIPPINES-1211")
        pdf.drawString(225, 730, "TEL. NO. 8672-00-32 / 8470-0081 / 8552-10-98")

        pdf.setFont('Times-Bold', 24)
        pdf.drawString(30, 702, "_____________________________________________")
        pdf.drawString(30, 700, "_____________________________________________")

        pdf.setFont('Times-Roman', 9)
        pdf.drawString(30, 650, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 640, "Barangay Chairman")
        pdf.drawString(30, 630, "Development Plan Chairman")
        pdf.drawString(30, 620, "Peace and Order")
        pdf.drawString(30, 610, "Committee Chairman")

        pdf.drawString(80, 580, "Kagawad")

        pdf.setFont('Times-Roman', 9)
        pdf.drawString(30, 560, "SIEGFRED JASON A. JACOME")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 550, "Infrastructure and Public Works")
        pdf.drawString(30, 540, "Committee Chairman")
        pdf.setFont('Times-Roman', 9)

        pdf.drawString(30, 510, "MIKHAIL SANDINO S. GATCHALIAN")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 500, "Fire and Rescue")
        pdf.drawString(30, 490, "Committee Chairman")

        pdf.drawString(30, 460, "ABELARDO U. BRILLANTES")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 450, "Cleanliness and Beautification")
        pdf.drawString(30, 440, "Committee Chairman")

        pdf.drawString(30, 410, "LUIS P. ALMARIO, JR.")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 400, "Social Services")
        pdf.drawString(30, 390, "Women and Family Welfare;")
        pdf.drawString(30, 380, "Committee Chairman")

        pdf.drawString(30, 350, "CRISOSTOMO B. CUNANAN")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 340, "Education and Culture")
        pdf.drawString(30, 330, "Committee Chairman")

        pdf.drawString(30, 300, "AGNES M. AGUSTIN")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 290, "Health and Sanitation;")
        pdf.drawString(30, 280, "Ways and Means/Bids and Awards")
        pdf.drawString(30, 270, "Committee Chairman")

        pdf.drawString(30, 240, "SHIRLEY G. BORJA")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 230, "Livelihood")
        pdf.drawString(30, 220, "Committee Chairwoman")

        pdf.drawString(30, 190, "KATE CHRISLINE M. CAÑEGA")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 180, "Sangguniang Kabataan Chairwoman")

        pdf.drawString(30, 150, "EDGARDO D. GATCHALIAN")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 140, "Barangay Treasurer")

        pdf.drawString(30, 110, "MYRNA F. CASABON")
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(30, 100, "Barangay Secretary")


        pdf.setFont('Times-Roman', 14)
        pdf.drawString(225, 600, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(210, 550, "CERTIFICATE OF INDIGENCY")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(170, 500, "TO WHOM IT MAY CONCERN:")
        pdf.drawString(235, 450, "THIS IS TO CERTIFY")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(358, 450, "that _________________________________")
        pdf.drawString(420, 453, currentObject.first_name + " " + currentObject.middle_name + " " + currentObject.last_name)
        pdf.drawString(170, 430, ", ______ years old, and residing at ______________________________, Guadalupe")
        pdf.drawString(187, 433,  str(currentObject.age))
        pdf.drawString(370, 433, currentObject.street)
        pdf.drawString(170, 410, "Viejo, Makati City is a member of the indigent families in our community.")

        pdf.drawString(235, 370, "This ceritification is being issued upon the request of the above-named")
        pdf.drawString(170, 350, "person for securing requirement for ________________________.")

        pdf.drawString(235, 310, "Given this _______ day of ____________________, 2022 at Barangay")
        pdf.drawString(170, 290, "Hall, Barangay Guadalupe Viejo, Makati City.")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(280, 130, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 12)
        pdf.drawString(340, 116, "Barangay Captain")

        # logo = ImageReader('data:image/jpeg;base64,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')
        # pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
        
@staff_member_required
def admin_update_status_certificate_of_indigency_to_printed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
        detailsString = "Your document has been printed and is now due for payment. Please settle this and upload the proof of payment on your document's page at the document tracker"
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        print(latest_contributor)

        # email notification
        currentObject =  certificate_of_indigency.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Certificate of Indigenc#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Due Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " is now due for payment. Please settle this as soon as possible to proceed with your application.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("admin_individual_certificate_of_indigency", pk=pk)

    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

def upload_proof_of_payment_certificate_of_indigency(request, pk):
    if (request.method == "POST"):
        proof_of_payment = request.FILES.get("proof_of_payment")
        coi = certificate_of_indigency.objects.get(pk=pk)
        coi.proof_of_payment = proof_of_payment
        coi.save()

        currentObject = certificate_of_indigency.objects.all().get(pk=pk)
        global current_document_id
        current_document_id = currentObject.document_id

        return redirect("payment_success")

@staff_member_required
def admin_update_status_certificate_of_indigency_to_paid(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Printed, Paid")

        detailsString = "Payment for your document has been received. Please standby for any emails from us regarding when you can pick this up or have it delivered."
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        currentObject =  certificate_of_indigency.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay ID#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Received Notice"
        emailBody = 'Good day, \n\nThis is to confirm that your payment for document request #' +  doc_id + " has been received. We will notify you again once your document is ready for delivery/pickup.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_certificate_of_indigency", pk=pk)
    else:
        return render(request, "admin_individual_certificate_of_indigency.html", context)

@staff_member_required
def admin_update_status_certificate_of_indigency_to_out_for_delivery(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Printed, Out for Delivery/Ready for Pickup")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        detailsString = "Your document is now available for pickup/delivery. Please see the email sent to you for more details."
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details=detailsString)

        currentObject =  certificate_of_indigency.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Certificate of Indigency#' + doc_id + " Request from " + last_name + ", " + first_name + ": Out for Delivery/Pickup Notice"
        emailBody = 'Good day, \n\nCongratulations!\nThis is to notify you that your document request #' +  doc_id + " is now out for delivery/ready for pickup. You can call us at 9XXXXXXXXX to schedule for a pickup through your preferred courier or pick up the document yourself at the Barangay Hall during work hours. Thank you very much!\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_certificate_of_indigency", pk=pk)
    else:
        return render(request, "admin_individual_certificate_of_indigency.html", context)

@staff_member_required
def admin_update_status_certificate_of_indigency_to_delivered(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        receipt_date = request.POST.get("receipt_date")
        certificate_of_indigency.objects.all().filter(pk=pk).update(status="Delivered/Picked-up")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        certificate_of_indigency.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        detailString = "Document request completed. Picked up on " + receipt_date
        certificate_of_indigency.objects.all().filter(pk=pk).update(additional_details = detailString)
        return redirect("admin_individual_certificate_of_indigency", pk=pk)
    else:
        return render(request, "admin_individual_certificate_of_indigency.html", context)

# BARANGAY CERTIFICATE
def admin_update_status_barangay_certificate_to_rejected(request, pk):
    if (request.method == "POST"):
        reason_for_rejection = request.POST.get("reason_for_rejection")
        currentObject =  barangay_certificate.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Certificate of Indigency#' + doc_id + " Request from " + last_name + ", " + first_name + ": Rejection Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " has unfortunately been rejected for the following reasons:\n " +  reason_for_rejection + "\nFeel free to apply again at our website anytime.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        barangay_certificate.objects.all().filter(pk=pk).update(status="Rejected")
        detailsString = "Your document has been has unfortunately been rejected due to not meeting certain requirements set by the barangay. Please check your email for the specific reasons(s) and feel free to submit a request again anytime."
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)
        return redirect("admin_documents_list")
# Revert
@staff_member_required
def admin_update_status_barangay_certificate_back_to_submitted_for_review(request, pk):
    barangay_certificate.objects.all().filter(pk=pk).update(status="Submitted for Review")
    return redirect("admin_individual_barangay_certificate", pk=pk)

@staff_member_required
def admin_update_status_barangay_certificate_back_to_review_completed(request, pk):
    barangay_certificate.objects.all().filter(pk=pk).update(status="Review Completed")
    return redirect("admin_individual_barangay_certificate", pk=pk)

@staff_member_required
def admin_update_status_barangay_certificate_back_to_pre_filled_template_verified(request, pk):
    barangay_certificate.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
    return redirect("admin_individual_barangay_certificate", pk=pk)

@staff_member_required
def admin_update_status_barangay_certificate_back_to_printed(request, pk):
    barangay_certificate.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
    return redirect("admin_individual_barangay_certificate", pk=pk)

# Update
@staff_member_required
def admin_update_status_barangay_certificate_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
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

        barangay_certificate.objects.all().filter(pk=pk).update(status="Review Completed")
        barangay_certificate.objects.all().filter(pk=pk).update(last_name=last_name)
        barangay_certificate.objects.all().filter(pk=pk).update(first_name=first_name)
        barangay_certificate.objects.all().filter(pk=pk).update(middle_name=middle_name)
        barangay_certificate.objects.all().filter(pk=pk).update(age=age)
        barangay_certificate.objects.all().filter(pk=pk).update(birthday=birthday)
        barangay_certificate.objects.all().filter(pk=pk).update(sex=sex)
        barangay_certificate.objects.all().filter(pk=pk).update(nationality=nationality)
        barangay_certificate.objects.all().filter(pk=pk).update(civil_status=civil_status)
        barangay_certificate.objects.all().filter(pk=pk).update(email=email)
        barangay_certificate.objects.all().filter(pk=pk).update(contact_num=contact_num)
        barangay_certificate.objects.all().filter(pk=pk).update(street=street)
        barangay_certificate.objects.all().filter(pk=pk).update(city=city)
        barangay_certificate.objects.all().filter(pk=pk).update(barangay=barangay)
        barangay_certificate.objects.all().filter(pk=pk).update(zip_code=zip_code)
        barangay_certificate.objects.all().filter(pk=pk).update(province=province)
        
        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_certificate", pk=pk)

    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificate.html", context)

@staff_member_required
def admin_update_status_barangay_clearance_to_review_completed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
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

        barangay_clearance.objects.all().filter(pk=pk).update(status="Review Completed")
        barangay_clearance.objects.all().filter(pk=pk).update(last_name=last_name)
        barangay_clearance.objects.all().filter(pk=pk).update(first_name=first_name)
        barangay_clearance.objects.all().filter(pk=pk).update(middle_name=middle_name)
        barangay_clearance.objects.all().filter(pk=pk).update(age=age)
        barangay_clearance.objects.all().filter(pk=pk).update(birthday=birthday)
        barangay_clearance.objects.all().filter(pk=pk).update(sex=sex)
        barangay_clearance.objects.all().filter(pk=pk).update(nationality=nationality)
        barangay_clearance.objects.all().filter(pk=pk).update(civil_status=civil_status)
        barangay_clearance.objects.all().filter(pk=pk).update(email=email)
        barangay_clearance.objects.all().filter(pk=pk).update(contact_num=contact_num)
        barangay_clearance.objects.all().filter(pk=pk).update(street=street)
        barangay_clearance.objects.all().filter(pk=pk).update(city=city)
        barangay_clearance.objects.all().filter(pk=pk).update(barangay=barangay)
        barangay_clearance.objects.all().filter(pk=pk).update(zip_code=zip_code)
        barangay_clearance.objects.all().filter(pk=pk).update(province=province)
        
        detailsString = "Your document has been reviewed by the barangay and will now be proceed to the next steps. Please standby for any emails from us regarding your application moving forward."
        barangay_clearance.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_clearance.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_clearance", pk=pk)

    lia = get_object_or_404(barangay_clearance, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_clearance.html", context)

@staff_member_required
def admin_update_status_barangay_certificate_to_pre_filled_template_verified(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_certificate.objects.all().filter(pk=pk).update(status="Pre-filled Template Verified")
        
        detailsString = "The pre-filled template for your document has been verified and will now undergo printing. Please standby for any emails from us regarding payment for your document."
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        return redirect("admin_individual_barangay_certificate", pk=pk)

    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificatence.html", context)

@staff_member_required
def admin_print_barangay_certificate_bonafide(request, pk):
    if (request.method == 'POST'):
        currentObject =  barangay_certificate.objects.all().get(pk=pk)

        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.

        # pdf.drawString(100,810, 'x100')
        # pdf.drawString(200,810, 'x200')
        # pdf.drawString(300,810, 'x300')
        # pdf.drawString(400,810, 'x400')
        # pdf.drawString(500,810, 'x500')

        # pdf.drawString(10,100, 'y100')
        # pdf.drawString(10,200, 'y200')
        # pdf.drawString(10,300, 'y300')
        # pdf.drawString(10,400, 'y400')
        # pdf.drawString(10,500, 'y500')
        # pdf.drawString(10,600, 'y600')
        # pdf.drawString(10,700, 'y700')
        # pdf.drawString(10,800, 'y800')  

        for font in pdf.getAvailableFonts():
            print(font)

        pdf.setFont('Times-Roman', 14)
        pdf.drawString(174, 700, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(180, 650, "CERTIFICATION")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(100, 600, "TO WHOM IT MAY CONCERN:")
        pdf.drawString(150, 550, "THIS IS TO CERTIFY")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(273, 550, "that _________________________________")
        pdf.drawString(340, 553, currentObject.first_name)
        pdf.drawString(100, 530, "_____________________________ is a bonafide resident with postal or business")
        pdf.drawString(110, 533, currentObject.middle_name + " " + currentObject.last_name)
        pdf.drawString(100, 510, "address at _________________________________________________________ ")
        pdf.drawString(160, 513, currentObject.street + " " + currentObject.province +  " " + currentObject.city + " " + currentObject.barangay)
        pdf.drawString(100, 490, "has been issued this Barangay Permit/ Clearance for the purpose of securing his/her")
        pdf.drawString(100, 470, "_____________________________________________________.")

        pdf.drawString(135, 430, "Given this _______ day of ____________________, 2022 at Barangay Hall,")
        pdf.drawString(100, 410, "Barangay Guadalupe Viejo, Makati City.")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(280, 330, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 12)
        pdf.drawString(340, 316, "Barangay Captain")

        pdf.drawString(100, 270, "New/ Renewal")
        pdf.drawString(250, 270, ":")
        pdf.drawString(100, 250, "O.R. No.")
        pdf.drawString(250, 250, ":")
        pdf.drawString(100, 230, "Brgy. Clearance No.")
        pdf.drawString(250, 230, ":")
        pdf.drawString(100, 210, "Line/ Type of Business")
        pdf.drawString(250, 210, ":")
        pdf.drawString(100, 190, "No. of Years Operating")
        pdf.drawString(250, 190, ":")

        # logo = ImageReader('data:image/jpeg;base64,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')
        # pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@staff_member_required
def admin_print_barangay_certificate_transient(request, pk):
    if (request.method == 'POST'):
        currentObject =  barangay_certificate.objects.all().get(pk=pk)
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        pdf = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
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
        pdf.drawString(174, 700, "OFFICE OF THE BARANGAY CHAIRMAN")

        pdf.setFont('Times-Bold', 20)
        pdf.drawString(180, 650, "BARANGAY CLEARANCE")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(100, 600, "TO WHOM IT MAY CONCERN:")
        pdf.drawString(150, 550, "THIS IS TO CERTIFY")

        pdf.setFont('Times-Roman', 12)
        pdf.drawString(273, 550, "that _________________________________")
        pdf.drawString(340, 553, currentObject.first_name)
        pdf.drawString(100, 530, "____________________________________ is a transient with postal or business")
        pdf.drawString(110, 533, currentObject.middle_name + " " + currentObject.last_name)
        pdf.drawString(100, 510, "address at _________________________________________________________ ")
        pdf.drawString(160, 513, currentObject.street + " " + currentObject.province +  " " + currentObject.city + " " + currentObject.barangay)
        pdf.drawString(100, 490, "has been issued this Barangay Permit/ Clearance for the purpose of securing his/her")
        pdf.drawString(100, 470, "_____________________________________________________.")

        pdf.drawString(135, 430, "Given this _______ day of ____________________, 2022 at Barangay Hall,")
        pdf.drawString(100, 410, "Barangay Guadalupe Viejo, Makati City.")

        pdf.setFont('Times-Bold', 12)
        pdf.drawString(280, 330, "HEINRICH THADDEUS M. ANGELES")
        pdf.setFont('Times-Roman', 12)
        pdf.drawString(340, 316, "Barangay Captain")

        pdf.drawString(100, 270, "New/ Renewal")
        pdf.drawString(250, 270, ":")
        pdf.drawString(100, 250, "O.R. No.")
        pdf.drawString(250, 250, ":")
        pdf.drawString(100, 230, "Brgy. Clearance No.")
        pdf.drawString(250, 230, ":")
        pdf.drawString(100, 210, "Line/ Type of Business")
        pdf.drawString(250, 210, ":")
        pdf.drawString(100, 190, "No. of Years Operating")
        pdf.drawString(250, 190, ":")

        # logo = ImageReader('data:image/jpeg;base64,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')
        # pdf.drawImage(logo, 10, 10, mask='auto')

        # Close the PDF object cleanly, and we're done.
        pdf.showPage()
        pdf.save()
        

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

@staff_member_required
def admin_update_status_barangay_certificate_to_printed(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        
        barangay_certificate.objects.all().filter(pk=pk).update(status="Printed, Not Paid")
        detailsString = "Your document has been printed and is now due for payment. Please settle this and upload the proof of payment on your document's page at the document tracker"
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        print(latest_contributor)

        # email notification
        currentObject =  barangay_certificate.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Certificate#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Due Notice"
        emailBody = 'Good day,\n\n this is to notify you that your document request #' +  doc_id + " is now due for payment. Please settle this as soon as possible to proceed with your application.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect("admin_individual_barangay_certificate", pk=pk)

    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificate.html", context)

def upload_proof_of_payment_barangay_certificate(request, pk):
    if (request.method == "POST"):
        proof_of_payment = request.FILES.get("proof_of_payment")
        certificate = barangay_certificate.objects.get(pk=pk)
        certificate.proof_of_payment = proof_of_payment
        certificate.save()

        currentObject = barangay_certificate.objects.all().get(pk=pk)
        global current_document_id
        current_document_id = currentObject.document_id

        return redirect("payment_success")


@staff_member_required
def admin_update_status_barangay_certificate_to_paid(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_certificate.objects.all().filter(pk=pk).update(status="Printed, Paid")

        detailsString = "Payment for your document has been received. Please standby for any emails from us regarding when you can pick this up or have it delivered."
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)

        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        currentObject =  barangay_certificate.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Clearance#' + doc_id + " Request from " + last_name + ", " + first_name + ": Payment Received Notice"
        emailBody = 'Good day, \n\nThis is to confirm that your payment for document request #' +  doc_id + " has been received. We will notify you again once your document is ready for delivery/pickup.\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_certificate", pk=pk)
    else:
        return render(request, "admin_individual_barangay_certificate.html", context)


@staff_member_required
def admin_update_status_barangay_certificate_to_out_for_delivery(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        barangay_certificate.objects.all().filter(pk=pk).update(status="Printed, Out for Delivery/Ready for Pickup")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)

        detailsString = "Your document is now available for pickup/delivery. Please see the email sent to you for more details."
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details=detailsString)

        currentObject =  barangay_certificate.objects.all().get(pk=pk)
        email = currentObject.email
        last_name = currentObject.last_name
        first_name = currentObject.first_name
        doc_id = currentObject.document_id

        emailSubject = 'Barangay Certifiate#' + doc_id + " Request from " + last_name + ", " + first_name + ": Out for Delivery/Pickup Notice"
        emailBody = 'Good day, \n\nCongratulations!\nThis is to notify you that your document request #' +  doc_id + " is now out for delivery/ready for pickup. You can call us at 9XXXXXXXXX to schedule for a pickup through your preferred courier or pick up the document yourself at the Barangay Hall during work hours. Thank you very much!\n\nBest regards,\nBarangay Guadalupe Viejo"

        send_mail(
            emailSubject,
            emailBody,
            'barangayguadalupeviejotest@gmail.com',
            [email],
            fail_silently=False,
        )
        return redirect("admin_individual_barangay_certificate", pk=pk)
    else:
        return render(request, "admin_individual_barangay_certificate_.html", context)

@staff_member_required
def admin_update_status_barangay_certificate_to_delivered(request, pk):
    current_user = request.user
    if (request.method == "POST"):
        receipt_date = request.POST.get("receipt_date")
        barangay_certificate.objects.all().filter(pk=pk).update(status="Delivered/Picked-up")
        latest_contributor = current_user.first_name + " " + current_user.last_name
        barangay_certificate.objects.all().filter(pk=pk).update(latest_contributor = latest_contributor)
        detailString = "Document request completed. Picked up on " + receipt_date
        barangay_certificate.objects.all().filter(pk=pk).update(additional_details = detailString)
        return redirect("admin_individual_barangay_certificate", pk=pk)
    else:
        return render(request, "admin_individual_barangay_certificate.html", context)

# ANCHOR


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
def admin_individual_barangay_certificate(request, pk):
    lia = get_object_or_404(barangay_certificate, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_barangay_certificate.html", context)

@staff_member_required
def admin_individual_certificate_of_indigency(request,pk):
    lia = get_object_or_404(certificate_of_indigency, pk=pk)
    context = {
        "lia": lia,
    }
    return render(request, "admin_individual_certificate_of_indigency.html", context)

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

    ce1 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce2 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce3 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3
    context = {    
        # order by date submitted
        "ids": ids.order_by("date_submitted").reverse(),
        "clearances": clearances.order_by("date_submitted").reverse(),
        "certificates": certificates.order_by("date_submitted").reverse(),
    }

    return render(request, 'admin_printed_documents.html', context)

def admin_manage_announcements (request):
    context = {
        "announcements": announcement.objects.all()
    } 
    return render(request, 'admin_manage_announcements.html', context)

def admin_individual_announcement(request, pk):
    if (request.method == "POST"):
        title = request.POST.get("title")
        content = request.POST.get("content")
        announcement.objects.all().filter(pk=pk).update(title=title)
        announcement.objects.all().filter(pk=pk).update(content=content)
        return redirect('admin_manage_announcements')
    else:
        lia = get_object_or_404(announcement, pk=pk)
        context = {
            "lia": lia,
        }
        return render(request, 'admin_individual_announcement.html', context)

def delete_announcement(request, pk):
    announcement.objects.filter(pk=pk).delete()
    return redirect('admin_manage_announcements')

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

def individual_announcement(request, pk):
    lia = get_object_or_404(announcement, pk=pk)
    context  = {
        "lia": lia,
    }
    return render(request, 'individual_announcement.html', context)

def user_register(request): 

    if (request.method == "POST"):
        last_name = request.POST.get('last_name')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        personal_photo = request.FILES["personal_photo"]
        nationality = request.POST.get('nationality')
        sex = request.POST.get('sex')
        blood_type = request.POST.get('blood_type')
        civil_status = request.POST.get('civil_status')
        age = request.POST.get('age')
        birthday = request.POST.get('birthday')
        username = request.POST.get('username')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        street = request.POST.get('street')
        province = request.POST.get('province')
        city = request.POST.get('city')
        barangay = request.POST.get('barangay')
        zip_code = request.POST.get('zip_code')

        emailQuery = User.objects.all().filter(email=email)
        contactNumQuery = user_account.objects.all().filter(contact_number=contact_number)
        usernameQuery = User.objects.all().filter(username=username)
        if emailQuery.exists():
            messages.warning(request, 'The email you submitted already has an account. Please use a different email.')
        elif usernameQuery.exists():
            messages.warning(request, 'The username you submitted already exists. Please use a different username.')
        elif contactNumQuery.exists():
            messages.warning(request, 'The phone number you submitted already exists. Please use a different phone number.')
        else:
            User.objects.create(
                last_name = last_name,
                first_name = first_name,
                email = email,
                username = username,
            )

            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()

            user = authenticate(request, username=username, password=password)
            login(request, user)

            user_account.objects.create(
                user = User.objects.get(username = username),
                personal_photo = personal_photo,
                middle_name = middle_name,
                nationality = nationality,
                sex = sex,
                blood_type = blood_type,
                civil_status = civil_status,
                age = age,
                birthday = birthday,
                contact_number = contact_number,
                street = street,
                province = province,
                city = city,
                barangay = barangay,
                zip_code = zip_code
            )
            return redirect('/web_portal/')

    return render(request, 'user_register.html')

    

def user_login(request):
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            login(request, user)
            print(username)
            print(password)
            return redirect('/web_portal/')
        else: 
            messages.warning(request, "Username or Password is incorrect")

    return render(request, 'user_login.html')

def change_password(request):
    current_user = request.user
    if (request.method == 'POST'):
        username = current_user.username
        print(username)
        password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = authenticate(request, username=username, password=password)
        if user is not None: 
            if new_password == confirm_password:
                current_user.set_password(new_password)
                current_user.save()
                user = authenticate(request, username=username, password=new_password)
                login(request, user)
                return redirect("base")
            else:
                messages.warning(request, "Please confirm your new password.")
        else: 
            messages.warning(request, "The password you entered is incorrect. Please enter your current password.")

    return render(request, 'user_change_password.html')

def reset_password(request):
    if (request.method == "POST"):
        # email notification
        email = request.POST.get("email")
        confirm_email = request.POST.get("confirm_email")
        username = request.POST.get("username")
        birthday = request.POST.get("birthday")
        
        if User.objects.all().filter(email=email).exists():
            checker = str(user_account.objects.all().get(user=User.objects.all().get(email=email)).birthday).split(" ")
            if email == confirm_email:
                if User.objects.all().get(email=email).username == username:
                    if checker[0] == birthday:
                        user = User.objects.get(email=email)
                        newpass = uuid.uuid4()
                        user.set_password(str(newpass))
                        user.save()
                        emailSubject = "Password Reset Request"
                        emailBody = "Good day,\n\n This is to notify you that you received a password reset request from the Guadalupe Viejo Web Portal.\n\nYour new password is as follows:\n" + str(newpass) + "\n\nBest regards,\nBarangay Guadalupe Viejo"

                        send_mail(
                            emailSubject,
                            emailBody,
                            'barangayguadalupeviejotest@gmail.com',
                            [email],
                            fail_silently=False,
                        )
                        messages.warning(request, "A password has been sent to your email!")
                        return redirect("user_login")
                    else: 
                        messages.warning(request, "The birthday and email credentials do not match.")
                        print(checker[0])
                        print(birthday)
                else:
                    messages.warning(request, "The username and email credentials do not match.")
            else:
                messages.warning(request, "Please confirm your email.")
        else: 
            messages.warning(request, "That email does not have an account. Please input a valid email.")

    return render(request, "user_reset_password.html")

def user_account_information (request): 
    context = {
        'user': request.user,
    }
    user = request.user
    if (request.method == "POST"):
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")

        middle_name = request.POST.get("middle_name")
        age = request.POST.get("age")
        blood_type = request.POST.get("blood_type")
        contact_number = request.POST.get("contact_number")
        birthday = request.POST.get("birthday")
        civil_status = request.POST.get("civil_status")
        nationality = request.POST.get("nationality")
        sex = request.POST.get("sex")
        street = request.POST.get("street")
        province = request.POST.get("province")
        city = request.POST.get("city")
        barangay = request.POST.get("barangay")
        zip_code = request.POST.get("zip_code")

        contactNumQuery = user_account.objects.all().filter(contact_number=contact_number)
        
        if (User.objects.get(id=user.id) == None):
            print("User does not exist")
        else:
            if contactNumQuery.exists():
                if user_account.objects.all().get(contact_number=contact_number).id == user.user_account.id:
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(age=age)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(contact_number=contact_number)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(middle_name=middle_name)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(civil_status=civil_status)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(nationality=nationality)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(sex=sex)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(blood_type=blood_type)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(street=street)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(province=province)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(city=city)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(barangay=barangay)
                    user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(zip_code=zip_code)
                    User.objects.all().filter(id=user.id).update(first_name=first_name)
                    User.objects.all().filter(id=user.id).update(last_name=last_name)
                else:
                    messages.warning(request, 'The phone number you submitted already exists. Please use a different phone number.')
            else:
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(age=age)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(contact_number=contact_number)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(middle_name=middle_name)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(civil_status=civil_status)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(birthday=birthday)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(nationality=nationality)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(sex=sex)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(street=street)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(province=province)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(city=city)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(barangay=barangay)
                user_account.objects.all().filter(user=User.objects.get(id=user.id)).update(zip_code=zip_code)
                User.objects.all().filter(id=user.id).update(first_name=first_name)
                User.objects.all().filter(id=user.id).update(last_name=last_name)
    
        return redirect("user_account_information")

    return render(request, 'user_account_information.html', context)

def all_active_requests (request): 
    user = request.user

    if request.user == "AnonymousUser":
        ids = ""
        clearances = ""
        certificates = ""
        cois = ""
    else:
        ids1 = barangay_id.objects.all().filter(status = "Submitted for Review", submitted_by = user.username)
        ids2 = barangay_id.objects.all().filter(status = "Review Completed", submitted_by = user.username)
        ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified", submitted_by = user.username)
        ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid", submitted_by = user.username)
        ids5 = barangay_id.objects.all().filter(status = "Printed, Paid", submitted_by = user.username)
        ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup", submitted_by = user.username)
        ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

        cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review", submitted_by = user.username)
        cl2 = barangay_clearance.objects.all().filter(status = "Review Completed", submitted_by = user.username)
        cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified", submitted_by = user.username)
        cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid", submitted_by = user.username)
        cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid", submitted_by = user.username)
        cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup", submitted_by = user.username)
        clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6


        c1 = barangay_certificate.objects.all().filter(status = "Submitted for Review", submitted_by = user.username)
        c2 = barangay_certificate.objects.all().filter(status = "Review Completed", submitted_by = user.username)
        c3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified", submitted_by = user.username)
        c4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid", submitted_by = user.username)
        c5 = barangay_certificate.objects.all().filter(status = "Printed, Paid", submitted_by = user.username)
        c6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup", submitted_by = user.username)
        certificates = c1 | c2 | c3 | c4 | c5 | c6


        coi1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review", submitted_by = user.username)
        coi2 = certificate_of_indigency.objects.all().filter(status = "Review Completed", submitted_by = user.username)
        coi3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified", submitted_by = user.username)
        coi4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid", submitted_by = user.username)
        coi5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid", submitted_by = user.username)
        coi6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup", submitted_by = user.username)
        cois = coi1 | coi2 | coi3 | coi4 | coi5 | coi6
    

    context = {
        "ids": ids,
        "clearances": clearances,
        "cois": cois,
        "certificates": certificates,
        'user': request.user
    }

    return render(request, 'all_active_requests.html', context)

def document_tracker(request):
    if (request.method == 'POST'):
        searched = request.POST.get("searched")

        ids = barangay_id.objects.filter(document_id = searched)
        clearances = barangay_clearance.objects.filter(document_id = searched)
        certificates = barangay_certificate.objects.filter(document_id = searched)
        cois = certificate_of_indigency.objects.filter(document_id = searched)

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
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_id = "02-" + str(date.today().year) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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

            government_id_or_letter = request.FILES["government_id_or_letter"]
            personal_photo = request.FILES["personal_photo"]

            type = "Bonafide"
            document_type = "Barangay Certificate"

            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_certificate.objects.create(
                document_id = document_id,
                document_type = document_type,
                submitted_by = submitted_by,

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
                status = "Submitted for Review",
                date_submitted = date.today(),
                additional_details = detailsString,
                ) 
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay Certificate#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "barangay_certificate_form.html", context)

def create_barangay_certificate_transient(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_id = "02-" + str(date.today().year) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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

            government_id_or_letter = request.FILES["government_id_or_letter"]
            personal_photo = request.FILES["personal_photo"]

            type = "Transient"
            document_type = "Barangay Certificate"

            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_certificate.objects.create(
                document_id = document_id,
                document_type = document_type,
                submitted_by = submitted_by,

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
                status = "Submitted for Review",
                date_submitted = date.today(),
                additional_details = detailsString,
                ) 
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay Certificate#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
        return redirect("document_success_page")
    else:
        return render(request, "barangay_certificate_transient_form.html", context)

def create_barangay_clearance(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_id = "01-" + str(date.today().year) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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

            government_id_or_letter = request.FILES["government_id_or_letter"]
            personal_photo = request.FILES["personal_photo"]

            type = "Bonafide"
            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_clearance.objects.create(
                document_id = document_id,
                document_type = "Barangay Clearance",
                submitted_by = submitted_by,

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
                status = "Submitted for Review",
                latest_contributor = "System",
                date_submitted = date.today(),
                additional_details = detailsString,
                ) 
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay Clearance#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "barangay_clearance_form.html", context)
        

def create_barangay_clearance_transient(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_id = "01-" + str(date.today().year) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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

            government_id_or_letter = request.FILES['government_id_or_letter']
            personal_photo = request.FILES["personal_photo"]

            type = "Transient"

            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_clearance.objects.create(
                document_id = document_id,
                submitted_by = submitted_by,

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
                document_type = "Barangay Clearance",
                status = "Submitted for Review",
                date_submitted = date.today(),
                additional_details = detailsString
                ) 
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay Clearance#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "barangay_clearance_transient_form.html", context)

def create_barangay_id(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_type = "Barangay ID"
            document_id = str(date.today().year) + "-" + str(date.today().month) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

            # Personal Details
            last_name = request.POST.get("last_name")
            first_name = request.POST.get("first_name")
            middle_name = request.POST.get('middle_name')
            age = request.POST.get("age")
            birthday = request.POST.get("birthday")
            sex = request.POST.get("sex")
            blood_type = request.POST.get("blood_type")
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

            
            government_id_or_letter = request.FILES['government_id_or_letter']
            voters_id = request.FILES["voters_id"]
            personal_photo = request.FILES["personal_photo"]

            type = "Constituent"

            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_id.objects.create(
                document_type = document_type,
                submitted_by = submitted_by,
                document_id = document_id,

                # Personal Info
                last_name = last_name,
                first_name = first_name,
                middle_name = middle_name,
                age = age,
                birthday = birthday,
                sex = sex,
                blood_type = blood_type,
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
                
                status = "Submitted for Review",
                latest_contributor = "System",
                date_submitted = date.today(),
                additional_details = detailsString,
                )
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay ID#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "barangay_id_form.html", context)

def create_barangay_id_transient(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_type = "Barangay ID"
            document_id = str(date.today().year) + "-" + str(date.today().month) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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

            
            government_id_or_letter = request.FILES['government_id_or_letter']
            voters_id = request.FILES["voters_id"]
            personal_photo = request.FILES["personal_photo"]

            landlord_name = request.POST.get("landlord_name")
            landlord_contact_number = request.POST.get("landlord_contact_number")
            landlord_address = request.POST.get("landlord_address")

            type = "Transient"

            detailsString = "Your document has been submitted into our system and will now undergo review."

            barangay_id.objects.create(
                document_type = document_type,
                document_id = document_id,
                submitted_by = submitted_by,

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
                landlord_name = landlord_name,
                landlord_contact_number = landlord_contact_number,
                landlord_address = landlord_address,
                type = type,
                
                status = "Submitted for Review",
                latest_contributor = "System",
                date_submitted = date.today(),
                additional_details = detailsString,
                )
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Barangay ID#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "barangay_id_form_transient.html", context)        

def upload_proof_of_payment_barangay_id(request, pk):
    if (request.method == "POST"):
        proof_of_payment = request.FILES.get("proof_of_payment")
        id = barangay_id.objects.get(pk=pk)
        id.proof_of_payment = proof_of_payment
        id.save()

        currentObject = barangay_id.objects.all().get(pk=pk)
        global current_document_id
        current_document_id = currentObject.document_id

        return redirect("payment_success")
    

def create_certificate_of_indigency(request):
    current_user = request.user
    context = {
        "ids": barangay_id.objects.all(),
        "clearances": barangay_clearance.objects.all(),
        "certificate": barangay_certificate.objects.all(),
    }

    ids1 = barangay_id.objects.all().filter(status = "Submitted for Review")
    ids2 = barangay_id.objects.all().filter(status = "Review Completed")
    ids3 = barangay_id.objects.all().filter(status = "Pre-filled Template Verified")
    ids4 = barangay_id.objects.all().filter(status = "Printed, Not Paid")
    ids5 = barangay_id.objects.all().filter(status = "Printed, Paid")
    ids6 = barangay_id.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    ids = ids1 | ids2 | ids3 | ids4 | ids5 | ids6

    cl1 = barangay_clearance.objects.all().filter(status = "Submitted for Review")
    cl2 = barangay_clearance.objects.all().filter(status = "Review Completed")
    cl3 = barangay_clearance.objects.all().filter(status = "Pre-filled Template Verified")
    cl4 = barangay_clearance.objects.all().filter(status = "Printed, Not Paid")
    cl5 = barangay_clearance.objects.all().filter(status = "Printed, Paid")
    cl6 = barangay_clearance.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    clearances = cl1 | cl2 | cl3 | cl4 | cl5 | cl6

    ce1 = barangay_certificate.objects.all().filter(status = "Submitted for Review")
    ce2 = barangay_certificate.objects.all().filter(status = "Review Completed")
    ce3 = barangay_certificate.objects.all().filter(status = "Pre-filled Template Verified")
    ce4 = barangay_certificate.objects.all().filter(status = "Printed, Not Paid")
    ce5 = barangay_certificate.objects.all().filter(status = "Printed, Paid")
    ce6 = barangay_certificate.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    certificates = ce1 | ce2 | ce3 | ce4 | ce5 | ce6

    ci1 = certificate_of_indigency.objects.all().filter(status = "Submitted for Review")
    ci2 = certificate_of_indigency.objects.all().filter(status = "Review Completed")
    ci3 = certificate_of_indigency.objects.all().filter(status = "Pre-filled Template Verified")
    ci4 = certificate_of_indigency.objects.all().filter(status = "Printed, Not Paid")
    ci5 = certificate_of_indigency.objects.all().filter(status = "Printed, Paid")
    ci6 = certificate_of_indigency.objects.all().filter(status = "Printed, Out for Delivery/Ready for Pickup")
    indigencies = ci1 | ci2 | ci3 | ci4 | ci5 | ci6

    print(str(current_user))

    isValid = False

    if str(current_user) != "AnonymousUser":
        doc_count = certificates.filter(submitted_by=current_user).count() + ids.filter(submitted_by=current_user).count() + clearances.filter(submitted_by=current_user).count() + indigencies.filter(submitted_by=current_user).count()
        user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=doc_count)


    if (request.method == "POST"):
        if str(current_user) == "AnonymousUser":
            if ids.filter(contact_num=request.POST.get("contact_number")).exists() or clearances.filter(contact_num=request.POST.get("contact_number")).exists() or certificates.filter(contact_num=request.POST.get("contact_number")).exists() or indigencies.filter(contact_num=request.POST.get("contact_number")).exists():
                messages.warning(request, "You have reached your limit for requesting documents! Unregistered users can only have 1 active document at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)
            else:
                isValid = True
                pass
        else:
            if doc_count < 5:
                print("Current Active: " + str(doc_count))
                user_account.objects.all().filter(user=User.objects.get(id=current_user.id)).update(currently_active=(doc_count + 1))
                isValid = True
                pass
            else:
                messages.warning(request, "You have reached your limit for requesting documents! Registered users can only have 5 active documents at a time, please wait for your documents to be resolved before requesting again.")
                isValid = False
                return render(request, "barangay_certificate_form.html", context)

        if isValid == True:
            document_type = "Certificate of Indigency"
            document_id = str(date.today().year) + "-" + str(date.today().month) + "-" + request.POST.get("document_id")
            submitted_by = current_user.username

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
            
            government_id_or_letter = request.FILES["government_id_or_letter"]
            personal_photo = request.FILES["personal_photo"]

            type = ""
            detailsString = "Your document has been submitted into our system and will now undergo review."

            certificate_of_indigency.objects.create(
                document_type = document_type,
                document_id = document_id,
                submitted_by = submitted_by,

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
                
                status = "Submitted for Review",
                latest_contributor = "System",
                date_submitted = date.today(),
                additional_details = detailsString,
                )
            global current_document_id
            current_document_id = document_id

            emailSubject = 'Certificate of Indigency#' + current_document_id + " Request from " + last_name + ", " + first_name
            emailBody = 'Good day,\n\n this is to confirm that your document request #' +  current_document_id + "has been submitted, and will now undergo review. Please regularly check its status at https://www.guadalupeviejo.com/web_portal/document_tracker/ for updates.\n\nBest regards,\nBarangay Guadalupe Viejo"

            send_mail(
                emailSubject,
                emailBody,
                'barangayguadalupeviejotest@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect("document_success_page")
    else:
        return render(request, "certificate_of_indigency_form.html", context) 

def document_success_page(request):
    document_id = current_document_id
    print(document_id)
    context = {
        "document_id": document_id
    }
    return render(request, "document_success_page.html", context)

def payment_success_page(request):
    document_id = current_document_id
    print(document_id)
    context = {
        "document_id": document_id
    }
    return render(request, "payment_success.html", context)

    
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

def contact_us_page(request):
    context = {
        'user': request.user
    }
    if(request.method == "POST"):
        last_name = request.POST.get("last_name")
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        inquiry.objects.create(
            last_name = last_name,
            first_name = first_name,
            email = email,
            message = message,
        )
        #how to show users na meron submitted na inquiry nila?
        return redirect('contact_us_page')
    else:
        return render(request, "contact_us_page.html", context)

def user_about_us_page(request):
    return render(request, 'user_about_us_page.html')


def admin_view_inquiries(request):
    all_inquiries = inquiry.objects.all()
    return render(request, 'admin_view_inquiries.html', {'inquiries':all_inquiries})

def admin_view_specific_inquiry(request, pk):
    i = get_object_or_404(inquiry, pk=pk)
    return render(request, 'admin_view_specific_inquiry.html', {'i':i})
