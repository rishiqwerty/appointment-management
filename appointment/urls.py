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
    path("", views.display_appointments, name="get-appoint")
]