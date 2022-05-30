from distutils.command.upload import upload
from email.policy import default
from django.contrib.auth.models import User
from django.db import models
import os
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()
# Create your models here.

def path_and_rename_barangay_clearance(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[GOVT_ID_OR_LOA]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_clearance/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_personal_photo_barangay_clearance(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PERSONAL_PHOTO]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_clearance/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_pop_barangay_clearance(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PROOF_OF_PAYMENT]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_clearance/{}/proof_of_payment/{}'.format(instance.document_id, filename)

class barangay_clearance(models.Model):
    document_id = models.CharField(max_length = 100, default="null")
    # Personal Details
    document_type = models.CharField(max_length = 100, default="null")
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    middle_name = models.CharField(max_length = 100, default="null")
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")
    contact_num = models.CharField(max_length = 100, default="null")

    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")

    # Files
    government_id_or_letter = models.FileField(default="null", storage=gd_storage)
    personal_photo = models.FileField(default="null", storage=gd_storage)

    type = models.CharField(
        max_length = 100,
        choices =  [('Bonafide', 'Bonafide'), ('Transient', 'Transient')], 
        default="null"
    )

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')], 
        default = "null"
    )
    latest_contributor = models.CharField(max_length=100, default="PLACEHOLDER")
    submitted_by = models.CharField(max_length=100, default="AnonymousUser")

    additional_details = models.CharField(max_length=1000, default="null")

    proof_of_payment = models.FileField(default= "null", null =True, storage=gd_storage)
    objects = models.Manager()

        
    def __str__(self):
        return self.document_id + " " +  "(" + self.type + ")" + " " + self.last_name

def path_and_rename_barangay_certificate(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[GOVT_ID_OR_LOA]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_certificate/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_personal_photo_barangay_certificate(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PERSONAL_PHOTO]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_certificate/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_pop_barangay_certificate(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PROOF_OF_PAYMENT]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_certificate/{}/proof_of_payment/{}'.format(instance.document_id, filename)

class barangay_certificate(models.Model):
    document_id = models.CharField(max_length = 100, default="null")
    # Personal Details
    document_type = models.CharField(max_length = 100, default="null")
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    middle_name = models.CharField(max_length = 100, default="null")
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")
    contact_num = models.CharField(max_length = 100, default="null")

    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")

    # Files
    government_id_or_letter = models.FileField(default="null", storage=gd_storage)
    personal_photo = models.FileField(default="null", storage=gd_storage)

    type = models.CharField(
        max_length = 100,
        choices =  [('Bonafide', 'Bonafide'), ('Transient', 'Transient')], 
        default="null"
    )

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')],  
        default = "null"
    )
    latest_contributor = models.CharField(max_length=100, default="PLACEHOLDER")
    submitted_by = models.CharField(max_length=100, default="AnonymousUser")
    

    additional_details = models.CharField(max_length=1000, default="null")
    proof_of_payment = models.FileField(default= "null", null =True, storage=gd_storage)
    objects = models.Manager()

    def __str__(self):
        return self.document_id + " " +  "(" + self.type + ")" + " " + self.last_name


def path_and_rename_certificate_of_indigency(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[GOVT_ID_OR_LOA]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'certificate_of_indigency/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_personal_photo_certificate_of_indigency(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PERSONAL_PHOTO]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'certificate_of_indigency/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_pop_certificate_of_indigency(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PROOF_OF_PAYMENT]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'certificate_of_indigency/{}/proof_of_payment/{}'.format(instance.document_id, filename)


class certificate_of_indigency(models.Model):
    document_id = models.CharField(max_length = 100, default="null")
    # Personal Details
    document_type = models.CharField(max_length = 100, default="null")
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    middle_name = models.CharField(max_length = 100, default="null")
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")
    contact_num = models.CharField(max_length = 100, default="null")

    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")

    # Files
    government_id_or_letter = models.FileField(default="null", storage=gd_storage)
    personal_photo = models.FileField(default="null", storage=gd_storage)

    type = models.CharField(max_length = 100, default="", null =True)

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')],  
        default = "null"
    )
    latest_contributor = models.CharField(max_length=100, default="PLACEHOLDER")
    submitted_by = models.CharField(max_length=100, default="AnonymousUser")
    

    additional_details = models.CharField(max_length=1000, default="null")
    proof_of_payment = models.FileField(default= "null", null =True, storage=gd_storage)
    objects = models.Manager()

    def __str__(self):
        return self.document_id + " " +  "(" + self.type + ")" + " " + self.last_name

def path_and_rename_barangay_id(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[GOVT_ID_OR_LOA]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_id/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_voters_barangay_id(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[VOTERS_ID]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_id/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_personal_photo_barangay_id(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PERSONAL_PHOTO]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_id/{}/requirements/{}'.format(instance.document_id, filename)

def path_and_rename_pop_barangay_id(instance, filename):
    ext = filename.split('.')[-1]
    filename = '[PROOF_OF_PAYMENT]-{}-{}.{}'.format(instance.last_name, instance.document_id, ext)
    return 'barangay_id/{}/proof_of_payment/{}'.format(instance.document_id, filename)

class barangay_id(models.Model):
    document_id = models.CharField(max_length = 100, default="null")
    # Personal Details
    document_type = models.CharField(max_length = 100, default="null")
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    middle_name = models.CharField(max_length = 100, default="null")
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    blood_type = models.CharField(
        max_length = 100,
        choices =  [('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], 
        default="null"
    )
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")
    contact_num = models.CharField(max_length = 100, default="null")
    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")
    # Emergency Contact 
    emergency_name = models.CharField(max_length = 100, default="null")
    emergency_contact_num = models.IntegerField(default = 0)
    emergency_address = models.CharField(max_length = 100, default="null")

    # Files
    personal_photo = models.FileField(default="null", storage=gd_storage)
    government_id_or_letter = models.FileField(null = True, storage=gd_storage)
    voters_id = models.FileField(default="null", storage=gd_storage)

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')], 
        default = "null"
    )
    latest_contributor = models.CharField(max_length=100, default="PLACEHOLDER")
    submitted_by = models.CharField(max_length=100, default="AnonymousUser")

    # Type
    type = models.CharField(
        max_length = 100,
        choices =  [('Constituent', 'Constituent'), ('Transient', 'Transient')], 
        default="null"
    )

    # Landlord info (for transient)
    landlord_name = models.CharField(max_length = 100, null=True, default="null")
    landlord_contact_number = models.CharField(max_length = 100, null=True, default="null")
    landlord_address = models.CharField(max_length = 100, null=True, default="null")

    additional_details = models.CharField(max_length=1000, default="null")

    # Payment Stuff
    proof_of_payment = models.FileField(default= "null", storage=gd_storage)

    objects = models.Manager()

    def __str__(self):
        return self.document_id + " " +  "(" + self.type + ")" + " " + self.last_name

class announcement(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 1000)
    objects = models.Manager()

class inquiry(models.Model):
    # Last Name, First Name, Email
    last_name = models.CharField(max_length = 100, default="null")
    first_name = models.CharField(max_length = 100, default="null")
    email = models.CharField(max_length = 100, default="null")

    # Message
    message = models.TextField(max_length=500)
    objects = models.Manager

    def __str___(self):
        return "Inquiry #" + self.id + ": " + self.last_name + ", " +  self.first_name

class admin_account(models.Model): 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    age = models.IntegerField(default = 0)
    birthday = models.DateField(default="2022-01-01")
    contact_number = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class user_account(models.Model): 
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    # Personal Details
    middle_name = models.CharField(max_length=100, default='')
    age = models.IntegerField(default = 0)
    birthday = models.DateTimeField(default="2022-01-01")
    nationality = models.CharField(max_length = 100, default="null")
    civil_status = models.CharField(max_length = 100, default="null")
    sex = models.CharField(
        max_length = 100,
        choices =  [('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say')], 
        default="null"
    )
    blood_type = models.CharField(
        max_length = 100,
        choices =  [('A+', 'A+'), ('A-', 'A-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-')], 
        default="null"
    )
    personal_photo = models.FileField(default="null")

    # Account Info
    contact_number = models.IntegerField(max_length = 10, default=0)

    # Address 
    street = models.CharField(max_length = 100, default="null")
    city = models.CharField(max_length = 100, default="null")
    barangay = models.CharField(max_length = 100, default="null")
    province = models.CharField(max_length = 100, default="null")
    zip_code = models.CharField(max_length = 100, default="null")

    currently_active = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.user)

