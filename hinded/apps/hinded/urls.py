from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import TemplateView
from hinded.apps.hinded.forms import UserLoginForm

urlpatterns = [
    path(
        'login/',
        LoginView.as_view(
            template_name='registration/login.html',
            authentication_form=UserLoginForm,
            redirect_authenticated_user=True
        ),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', TemplateView.as_view(template_name="hinded/home.html"), name="home"),
]
