from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DeleteView, TemplateView, CreateView, UpdateView

from .forms import HindedForm, IsikForm
from .models import Hinded, Isik, IsikuHinne

COLORS = {
    "X": "#EE4B2B",
    "2": "#EE4B2B",
    "1": "#EE4B2B",
    "3": "#DFFF00",
    "4": "#50C878",
    "5": "#228B22",
}


class HomeView(TemplateView):
    """Avalehe vaade."""

    template_name = "hinded/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Lisa vajalikud andmed vaatele."""
        if self.request.user.is_authenticated:
            isikud = {}
            hinded = Hinded.objects.all()
            ids = {}

            for isik in Isik.objects.all():
                ids[(f"{isik.eesnimi} {isik.perenimi}", isik.id)] = isik.id
                isikud[(f"{isik.eesnimi} {isik.perenimi}", isik.id)] = []

                for hinne in hinded:
                    data = {
                        "varv": None,
                        "vaartus": None,
                        "hinde_id": None,
                        "isiku_id": None,
                        "markmed": None
                    }
                    try:
                        isiku_hinne = IsikuHinne.objects.get(hinne=hinne, isik=isik)
                        data["varv"] = COLORS[isiku_hinne.vaartus]
                        data["vaartus"] = isiku_hinne.vaartus
                        data["hinde_id"] = isiku_hinne.hinne_id
                        data["isiku_id"] = isiku_hinne.isik_id
                        data["markmed"] = isiku_hinne.markmed
                    except IsikuHinne.DoesNotExist:
                        pass

                    isikud[(f"{isik.eesnimi} {isik.perenimi}", isik.id)].append(data)
            return {"isikud": isikud, "hinded": hinded, "ids": ids}

        return {}


class DeleteHinneView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """Vaade hinnete kustutamiseks."""

    model = Hinded
    success_url = "/"
    success_message = "Hinde kustutamine õnnestus."


class DeleteIsikView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    """Vaade isiku kustutamiseks."""

    model = Isik
    success_url = "/"
    success_message = "Õpilase kustutamine õnnestus."


class CreateIsikView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Vaade isiku loomiseks."""

    model = Isik
    success_url = "/"
    success_message = "Õpilase loomine õnnestus"
    form_class = IsikForm
    template_name = "hinded/create_isik.html"


class UpdateIsikView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Vaade isiku uuendamiseks."""

    model = Isik
    success_url = "/"
    success_message = "Õpilase uuendamine õnnestus"
    form_class = IsikForm
    template_name = "hinded/edit_isik.html"



class CreateHinneView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Vaade hinde loomiseks."""

    model = Hinded
    success_url = "/"
    success_message = "Hinde loomine õnnestus"
    form_class = HindedForm
    template_name = "hinded/create_hinne.html"


class UpdateHinneView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Vaade hinde uuendamiseks."""

    model = Hinded
    success_url = "/"
    success_message = "Hinde uuendamine õnnestus"
    form_class = HindedForm
    template_name = "hinded/edit_hinne.html"

