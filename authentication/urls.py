from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name='generic_form.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", views.SignUp.as_view(), name="signup" ),
    path('password/',   views.PasswordUpdateView.as_view()   , name = 'update_password'),
]
