from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from hinded.apps.hinded.forms import UserLoginForm
from hinded.apps.hinded.views import CreateHinneView, DeleteHinneView, DeleteIsikView, HomeView, CreateIsikView, UpdateHinneView, UpdateIsikView

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
    path('hinded/<pk>/kustuta/', DeleteHinneView.as_view(), name='delete_hinne'),
    path('hinded/loo/', CreateHinneView.as_view(), name='create_hinne'),
    path('hinded/<pk>/uuenda/', UpdateHinneView.as_view(), name='update_hinne'),
    path('isik/<pk>/kustuta/', DeleteIsikView.as_view(), name='delete_isik'),
    path('isik/loo/', CreateIsikView.as_view(), name='create_isik'),
    path('isik/<pk>/uuenda/', UpdateIsikView.as_view(), name='update_isik'),
    path('', HomeView.as_view(), name="home"),
]
