from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import UserLoginForm
from .views import AddSingleHinneView, CreateHinneView, CreateIsikView, DeleteHinneView, \
    DeleteIsikView, EditSingleHinne, HomeView, MassAddHinded, RemoveSingleHinne, \
    UpdateHinneView, UpdateIsikView, ViewIsikHinded

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm,
            redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("hinded/<pk>/kustuta/", DeleteHinneView.as_view(), name="delete_hinne"),
    path("hinded/loo/", CreateHinneView.as_view(), name="create_hinne"),
    path("hinded/<pk>/uuenda/", UpdateHinneView.as_view(), name="update_hinne"),
    path("hinded/lisa/", AddSingleHinneView.as_view(), name="add_single_hinne"),
    path("hinded/eemalda/", RemoveSingleHinne.as_view(), name="remove_single_hinne"),
    path("hinded/muuda/", EditSingleHinne.as_view(), name="edit_single_hinne"),
    path("hinded/<pk>/hulgi", MassAddHinded.as_view(), name="mass_add_hinded"),
    path("isik/<pk>/kustuta/", DeleteIsikView.as_view(), name="delete_isik"),
    path("isik/loo/", CreateIsikView.as_view(), name="create_isik"),
    path("isik/<pk>/uuenda/", UpdateIsikView.as_view(), name="update_isik"),
    path("opilane/", ViewIsikHinded.as_view(), name="view_isik_hinded"),
    path("", HomeView.as_view(), name="home"),
]
