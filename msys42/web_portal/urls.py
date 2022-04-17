from django.urls import path
from . import views

urlpatterns = [
    # user
    path("", views.base, name = "base"),
    path("hello/", views.say_hello),
    path("user_login/", views.user_login, name = 'user_login'),
    path("user_logout/", views.user_logout, name = "user_logout"),
    path("create_barangay_id/", views.create_barangay_id, name = "create_barangay_id"),
    path("create_barangay_certificate/", views.create_barangay_certificate, name = "create_barangay_certificate"),
    path("create_barangay_clearance/", views.create_barangay_clearance, name = "create_barangay_clearance"),
    path("create_certificate_of_indigency/", views.create_certificate_of_indigency, name = "create_certificate_of_indigency"),

    # document success page logged out
    path("document_success", views.document_success_page, name="document_success_page"),

    # admin
    path("admin_login/", views.admin_login, name = 'admin_login'),
    path("admin_logout", views.admin_logout, name = "admin_logout"),
    path("account_information/", views.admin_account_information, name='admin_account_information'),
    path("admin_base/", views.admin_documents_list, name = "admin_documents_list"),
    path("documents_list/", views.admin_documents_list, name = "admin_documents_list"),
    path("printed_documents/", views.admin_printed_documents, name="admin_printed_documents"),
    path("manage_announcements/", views.admin_manage_announcements, name="admin_manage_announcements"),
    path("create_announcements/", views.admin_create_announcements, name="admin_create_announcements"),
    path("individual_document/<int:pk>/", views.admin_indiviudal_document, name = "admin_indiviudal_document"),
    path("admin_individual_barangay_id/<int:pk>/", views.admin_individual_barangay_id, name = "admin_individual_barangay_id"),
    path("admin_individual_barangay_clearance/<int:pk>/", views.admin_individual_barangay_clearance, name = "admin_individual_barangay_clearance"),
    path("admin_individual_certificate_of_indigency/<int:pk>/", views.admin_individual_certificate_of_indigency, name = "admin_individual_certificate_of_indigency"),
    path("admin_individual_barangay_certificate/<int:pk>/", views.admin_individual_barangay_certificate, name = "admin_individual_barangay_certificate"),

    # admin prnting
    path("print_barangay_id_constituent/<int:pk>/", views.print_barangay_id_constituent, name = "print_barangay_id_constituent"),

    # updating barangay id
    path("admin_update_status_barangay_id_to_review_completed/<int:pk>/",  views.admin_update_status_barangay_id_to_review_completed, name="admin_update_status_barangay_id_to_review_completed"),
    path("admin_update_status_barangay_id_to_pre_filled_template_verified/<int:pk>/", views.admin_update_status_barangay_id_to_pre_filled_template_verified, name = "admin_update_status_barangay_id_to_pre_filled_template_verified"),
    path("admin_update_status_barangay_id_to_printed/<int:pk>/", views.admin_update_status_barangay_id_to_printed, name= "admin_update_status_barangay_id_to_printed"),
    
]