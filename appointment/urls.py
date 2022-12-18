from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.signup, name="register"),
    path("login/", views.user_login, name="login"),
    path("appoint/", views.appointment_creation, name="appoint"),
    path("get-appoint/", views.display_appointments, name="get-appoint"),
    path("logout/", views.user_logout, name="logout"),
    path("update/<int:id>/", views.update_appointment, name="update"),
    path("delete/<int:id>/", views.appointment_delete, name='delete'),
    path("med/<int:id>", views.create_medical_report, name="med"),
    path("med-data/", views.med_data, name="med-data"),
    path("profile/", views.profile_edit, name="profile"),
    path("profile-info/", views.profile_info, name="profile-info"),
    path("med-info/<int:id>", views.med_per_info, name="med-info"),
    path("", views.display_appointments, name="get-appoint")
]