from django.db import models

# Create your models here.
class barangay_clearance(models.Model):
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
    government_id_or_letter = models.FileField(default="null")
    personal_photo = models.FileField(default="null")

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

    objects = models.Manager()

class barangay_certificate(models.Model):
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
    government_id_or_letter = models.FileField(default="null")
    personal_photo = models.FileField(default="null")

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

    objects = models.Manager()

class barangay_id(models.Model):
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
    # Emergency Contact 
    emergency_name = models.CharField(max_length = 100, default="null")
    emergency_contact_num = models.IntegerField(default = 0)
    emergency_address = models.CharField(max_length = 100, default="null")

    # Files
    personal_photo = models.FileField(default="null")
    government_id_or_letter = models.FileField(null = True)
    voters_id = models.FileField(default="null")

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')], 
        default = "null"
    )

    # Type
    type = models.CharField(
        max_length = 100,
        choices =  [('Constituent', 'Constituent'), ('Transient', 'Transient')], 
        default="null"
    )

    # Landlord info (for transient)
    landlord_name = models.CharField(max_length = 100, null=True)
    landlord_contact_number = models.CharField(max_length = 100, null=True)
    landlord_address = models.CharField(max_length = 100, null=True)

    objects = models.Manager()

class certificate_of_indigency(models.Model):
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
    government_id_or_letter = models.FileField(default="null")
    personal_photo = models.FileField(default="null")

    # Status
    date_submitted = models.DateField(default="2022-01-01")
    status = models.CharField(
        max_length = 100,
        choices =  [('Submitted for Review', 'Submitted for Review'), ('Review Completed', 'Review Completed'), ('Pre-filled Template Verified', 'Pre-filled Template Verified'), ('Printed, Not Paid', 'Printed, Not Paid'), ('Printed, Paid', 'Printed, Paid'), ('Printed, Out for Delivery/Ready for Pickup', 'Printed, Out for Delivery/Ready for Pickup'), ('Delivered/Picked-up', 'Delivered/Picked-up'), ('Rejected', 'Rejected')], 
        default = "null"
    )



    objects = models.Manager()

class announcement(models.Model):
    title = models.CharField(max_length = 100)
    content = models.CharField(max_length = 1000)
    objects = models.Manager()