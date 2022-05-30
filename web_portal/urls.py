from django.urls import path
from . import views

urlpatterns = [
    # try
    path("some_view/", views.some_view, name = "some_view"),

    # USER
    path("", views.base, name = "base"),
    path("hello/", views.say_hello),
    path("user_login/", views.user_login, name = 'user_login'),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("user_logout/", views.user_logout, name = "user_logout"),
    path("user_register", views.user_register, name="user_register"),
    path("account_information/", views.user_account_information, name="user_account_information"),
    path("change_password", views.change_password, name="change_password"),

    path("individual_announcement/<int:pk>/", views.individual_announcement, name="individual_announcement"),
    path('faqs', views.faqs, name = "faqs"),

    # USER create barangay id
    path("create_barangay_id/", views.create_barangay_id, name = "create_barangay_id"),
    path("create_barangay_id_transient/", views.create_barangay_id_transient, name="create_barangay_id_transient"),

    # USER create barangay clearance
    path("create_barangay_clearance/", views.create_barangay_clearance, name = "create_barangay_clearance"),
    path("create_barangay_clearance_transient/", views.create_barangay_clearance_transient, name = "create_barangay_clearance_transient"),

    # USER create barangay certificate
    path("create_barangay_certificate/", views.create_barangay_certificate, name = "create_barangay_certificate"),
    path("create_barangay_certificate_transient/", views.create_barangay_certificate_transient, name = "create_barangay_certificate_transient"),

    # USER create certificate of indigency
    path("create_certificate_of_indigency/", views.create_certificate_of_indigency, name = "create_certificate_of_indigency"),

    # USER document tracker
    path("document_tracker/", views.document_tracker, name = "document_tracker"),

    # USER document success page logged out
    path("document_success", views.document_success_page, name="document_success_page"),

    # USER payment successs
    path("payment_success/", views.payment_success_page, name = "payment_success"),

    # USER Documents List
    path("all_active_requests/", views.all_active_requests, name = "all_active_requests"),

    # USER Contact Us page
    path("contact_us_page/", views.contact_us_page, name = "contact_us_page"),

    # USER About Us page
    path("user_about_us_page/", views.user_about_us_page, name = "user_about_us_page"),


    # ADMIN Stuff
    path("admin_login/", views.admin_login, name = 'admin_login'),
    path("admin_logout", views.admin_logout, name = "admin_logout"),
    path("admin_account_information/", views.admin_account_information, name='admin_account_information'),
    path("admin_base/", views.admin_documents_list, name = "admin_documents_list"),

    # ADMIN document lists
    path("documents_list/", views.admin_documents_list, name = "admin_documents_list"),
    path("printed_documents/", views.admin_printed_documents, name="admin_printed_documents"),
    path("inactive_documents_list", views.admin_inactive_documents_list, name ="admin_inactive_documents_list"),
    path("all_documents_list", views.admin_all_documents_list, name="admin_all_documents_list"),

    # ADMIN announcements
    path("manage_announcements/", views.admin_manage_announcements, name="admin_manage_announcements"),
    path("create_announcements/", views.admin_create_announcements, name="admin_create_announcements"),
    path("individual_document/<int:pk>/", views.admin_indiviudal_document, name = "admin_indiviudal_document"),
    path("delete_announcement/<int:pk>/", views.delete_announcement, name="delete_announcement" ),
    path("admin_individual_announcement/<int:pk>/", views.admin_individual_announcement, name ="admin_individual_announcement"),
    
    # ADMIN Individual Document Pages
    path("admin_individual_barangay_id/<int:pk>/", views.admin_individual_barangay_id, name = "admin_individual_barangay_id"),
    path("admin_individual_barangay_clearance/<int:pk>/", views.admin_individual_barangay_clearance, name = "admin_individual_barangay_clearance"),
    path("admin_individual_certificate_of_indigency/<int:pk>/", views.admin_individual_certificate_of_indigency, name= "admin_individual_certificate_of_indigency"),
    path("admin_individual_barangay_certificate/<int:pk>/", views.admin_individual_barangay_certificate, name = "admin_individual_barangay_certificate"),

    # NO IDEA
    path("print_barangay_id_constituent/<int:pk>/", views.print_barangay_id_constituent, name = "print_barangay_id_constituent"),


    # ---
    # ADMIN Barangay ID

    # Reject
    path("admin_update_status_barangay_id_to_rejected/<int:pk>/", views.admin_update_status_barangay_id_to_rejected, name = "admin_update_status_barangay_id_to_rejected"),
    
    # Revert
    path("admin_update_status_barangay_id_back_to_submitted_for_review/<int:pk>/", views.admin_update_status_barangay_id_back_to_submitted_for_review, name = "admin_update_status_barangay_id_back_to_submitted_for_review"),
    path("admin_update_status_barangay_id_back_to_review_completed/<int:pk>/", views.admin_update_status_barangay_id_back_to_review_completed, name = "admin_update_status_barangay_id_back_to_review_completed"),
    path("admin_update_status_barangay_id_back_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_id_back_to_pre_filled_template_verified, name = "admin_update_status_barangay_id_back_to_pre_filled_template_verified"),
    path("admin_update_status_barangay_id_back_to_printed/<int:pk>/", views.admin_update_status_barangay_id_back_to_printed, name ="admin_update_status_barangay_id_back_to_printed"),

    # Update
    path("upload_proof_of_payment_barangay_id/<int:pk>", views.upload_proof_of_payment_barangay_id, name = "upload_proof_of_payment_barangay_id"),
    path("admin_update_status_barangay_id_to_review_completed/<int:pk>/",  views.admin_update_status_barangay_id_to_review_completed, name="admin_update_status_barangay_id_to_review_completed"),
    path("admin_update_status_barangay_id_transient_to_review_completed/<int:pk>", views.admin_update_status_barangay_id_transient_to_review_completed, name="admin_update_status_barangay_id_transient_to_review_completed"),
    path("admin_update_status_barangay_id_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_id_to_pre_filled_template_verified, name = "admin_update_status_barangay_id_to_pre_filled_template_verified"),
    path("admin_update_status_barangay_id_to_printed/<int:pk>/", views.admin_update_status_barangay_id_to_printed, name= "admin_update_status_barangay_id_to_printed"),
    path("admin_update_status_barangay_id_to_paid/<int:pk>/", views.admin_update_status_barangay_id_to_paid, name = "admin_update_status_barangay_id_to_paid"),
    path("admin_update_status_barangay_id_to_out_for_delivery/<int:pk>/", views.admin_update_status_barangay_id_to_out_for_delivery, name= "admin_update_status_barangay_id_to_out_for_delivery"),
    path("admin_update_status_barangay_id_to_delivered/<int:pk>/", views.admin_update_status_barangay_id_to_delivered, name = "admin_update_status_barangay_id_to_delivered"),

    # ---
    # ADMIN Barangay Clearance

    # Reject
    path("admin_update_status_barangay_clearance_to_rejected/<int:pk>/", views.admin_update_status_barangay_clearance_to_rejected, name = "admin_update_status_barangay_clearance_to_rejected"),

    # Revert
    path("admin_update_status_barangay_clearance_back_to_submitted_for_review/<int:pk>", views.admin_update_status_barangay_clearance_back_to_submitted_for_review, name = "admin_update_status_barangay_clearance_back_to_submitted_for_review"),
    path("admin_update_status_barangay_clearance_back_to_review_completed/<int:pk>/", views.admin_update_status_barangay_clearance_back_to_review_completed, name= "admin_update_status_barangay_clearance_back_to_review_completed"),
    path("admin_update_status_barangay_clearance_back_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_clearance_back_to_pre_filled_template_verified, name = "admin_update_status_barangay_clearance_back_to_pre_filled_template_verified"),
    path("admin_update_status_barangay_clearance_back_to_printed/<int:pk>/", views.admin_update_status_barangay_clearance_back_to_printed, name ="admin_update_status_barangay_clearance_back_to_printed"),
    
    # Update
    path("admin_update_status_barangay_clearance_to_review_completed/<int:pk>/", views.admin_update_status_barangay_clearance_to_review_completed, name= "admin_update_status_barangay_clearance_to_review_completed"),
    path("admin_update_status_barangay_clearance_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_clearance_to_pre_filled_template_verified, name="admin_update_status_barangay_clearance_to_pre_filled_template_verified"),
    path("admin_print_barangay_clearance_bonafide/<int:pk>/", views.admin_print_barangay_clearance_bonafide, name ="admin_print_barangay_clearance_bonafide"),
    path("admin_print_barangay_clearance_transient/<int:pk>", views.admin_print_barangay_clearance_transient, name ="admin_print_barangay_clearance_transient"),
    path("admin_update_status_barangay_clearance_to_printed/<int:pk>/", views.admin_update_status_barangay_clearance_to_printed, name = "admin_update_status_barangay_clearance_to_printed"),
    path("upload_proof_of_payment_barangay_clearance/<int:pk>/", views.upload_proof_of_payment_barangay_clearance, name= "upload_proof_of_payment_barangay_clearance"),
    path("admin_update_status_barangay_clearance_to_paid/<int:pk>", views.admin_update_status_barangay_clearance_to_paid, name ="admin_update_status_barangay_clearance_to_paid"),
    path("admin_update_status_barangay_clearance_to_out_for_delivery/<int:pk>", views.admin_update_status_barangay_clearance_to_out_for_delivery, name ="admin_update_status_barangay_clearance_to_out_for_delivery"),
    path("admin_update_status_barangay_clearance_to_delivered/<int:pk>", views.admin_update_status_barangay_clearance_to_delivered, name ="admin_update_status_barangay_clearance_to_delivered"),

    # ADMIN Certificate of Indigency

    # Reject
    path("admin_update_status_certificate_of_indigency_to_rejected/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_rejected, name = "admin_update_status_certificate_of_indigency_to_rejected"),

    # Revert
    path("admin_update_status_certificate_of_indigency_back_to_submitted_for_review/<int:pk>/", views.admin_update_status_certificate_of_indigency_back_to_submitted_for_review, name ="admin_update_status_certificate_of_indigency_back_to_submitted_for_review"),
    path("admin_update_status_certificate_of_indigency_back_to_review_completed/<int:pk>/", views.admin_update_status_certificate_of_indigency_back_to_review_completed, name="admin_update_status_certificate_of_indigency_back_to_review_completed"),
    path("admin_update_status_certificate_of_indigency_back_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_certificate_of_indigency_back_to_pre_filled_template_verified, name="admin_update_status_certificate_of_indigency_back_to_pre_filled_template_verified"),
    path("admin_update_status_certificate_of_indigency_back_to_printed/<int:pk>/", views.admin_update_status_certificate_of_indigency_back_to_printed, name="admin_update_status_certificate_of_indigency_back_to_printed"),

    # Update
    path("admin_update_status_certificate_of_indigency_to_review_completed/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_review_completed, name ="admin_update_status_certificate_of_indigency_to_review_completed"),
    path("admin_update_status_certificate_of_indigency_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_pre_filled_template_verified, name = "admin_update_status_certificate_of_indigency_to_pre_filled_template_verified"),
    path("admin_print_certificate_of_indigency/<int:pk>/", views.admin_print_certificate_of_indigency, name="admin_print_certificate_of_indigency"),
    path("admin_update_status_certificate_of_indigency_to_printed/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_printed, name="admin_update_status_certificate_of_indigency_to_printed"),
    path("upload_proof_of_payment_certificate_of_indigency/<int:pk>/", views.upload_proof_of_payment_certificate_of_indigency, name = "upload_proof_of_payment_certificate_of_indigency"),
    path("admin_update_status_certificate_of_indigency_to_paid/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_paid, name= "admin_update_status_certificate_of_indigency_to_paid"),
    path("admin_update_status_certificate_of_indigency_to_out_for_delivery/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_out_for_delivery, name="admin_update_status_certificate_of_indigency_to_out_for_delivery"),
    path("admin_update_status_certificate_of_indigency_to_delivered/<int:pk>/", views.admin_update_status_certificate_of_indigency_to_delivered, name="admin_update_status_certificate_of_indigency_to_delivered"),

    # ADMIN Barangay Certificate

    # Reject
    path("admin_update_status_barangay_certificate_to_rejected/<int:pk>/", views.admin_update_status_barangay_certificate_to_rejected, name="admin_update_status_barangay_certificate_to_rejected"),

    # Revert
    path("admin_update_status_barangay_certificate_back_to_submitted_for_review/<int:pk>/", views.admin_update_status_barangay_certificate_back_to_submitted_for_review, name ="admin_update_status_barangay_certificate_back_to_submitted_for_review"),
    path("admin_update_status_barangay_certificate_back_to_review_completed/<int:pk>/", views.admin_update_status_barangay_certificate_back_to_review_completed, name="admin_update_status_barangay_certificate_back_to_review_completed"),
    path("admin_update_status_barangay_certificate_back_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_certificate_back_to_pre_filled_template_verified, name="admin_update_status_barangay_certificate_back_to_pre_filled_template_verified"),
    path("admin_update_status_barangay_certificate_back_to_printed/<int:pk>/", views.admin_update_status_barangay_certificate_back_to_printed, name= "admin_update_status_barangay_certificate_back_to_printed"),

    # Update
    path("admin_update_status_barangay_certificate_to_review_completed/<int:pk>/", views.admin_update_status_barangay_certificate_to_review_completed, name ="admin_update_status_barangay_certificate_to_review_completed"),
    path("admin_update_status_barangay_certificate_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_certificate_to_pre_filled_template_verified, name= "admin_update_status_barangay_certificate_to_pre_filled_template_verified"),
    path("admin_print_barangay_certificate_bonafide/<int:pk>/", views.admin_print_barangay_certificate_bonafide, name ="admin_print_barangay_certificate_bonafide"),
    path("admin_print_barangay_certificate_transient/<int:pk>/", views.admin_print_barangay_certificate_transient, name = "admin_print_barangay_certificate_transient"),
    path("admin_update_status_barangay_certificate_to_printed/<int:pk>/", views.admin_update_status_barangay_certificate_to_printed, name = "admin_update_status_barangay_certificate_to_printed"),
    path("upload_proof_of_payment_barangay_certificate/<int:pk>/", views.upload_proof_of_payment_barangay_certificate, name = "upload_proof_of_payment_barangay_certificate"),
    path("admin_update_status_barangay_certificate_to_paid/<int:pk>/", views.admin_update_status_barangay_certificate_to_paid, name = "admin_update_status_barangay_certificate_to_paid"),
    path("admin_update_status_barangay_certificate_to_out_for_delivery/<int:pk>/", views.admin_update_status_barangay_certificate_to_out_for_delivery, name= "admin_update_status_barangay_certificate_to_out_for_delivery"),
    path("admin_update_status_barangay_certificate_to_delivered/<int:pk>/", views.admin_update_status_barangay_certificate_to_delivered, name="admin_update_status_barangay_certificate_to_delivered"),

    # Inquiries
    path("admin_view_inquiries", views.admin_view_inquiries, name = "admin_view_inquiries"),
    path("admin_view_specific_inquiry/<int:pk>/", views.admin_view_specific_inquiry, name = "admin_view_specific_inquiry"),
]
