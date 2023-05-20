from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views import View
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
                        "hinde_id": hinne.id,
                        "hinde_nimi": hinne.nimi,
                        "isiku_id": None,
                        "markmed": None
                    }
                    try:
                        isiku_hinne = IsikuHinne.objects.get(hinne=hinne, isik=isik)
                        data["varv"] = COLORS[isiku_hinne.vaartus]
                        data["vaartus"] = isiku_hinne.vaartus
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


class MassAddHinded(SuccessMessageMixin, LoginRequiredMixin, View):
    """Lisa õpilastele korraga hinded."""

    def get(self, request, *args, **kwargs):
        """Lisa vajalikud väärtused HTML-i."""
        hinne = get_object_or_404(Hinded, pk=kwargs["pk"])
        isikud = Isik.objects.all()
        isik_data = {}

        for isik in isikud:
            try:
                isik_data[isik] = IsikuHinne.objects.get(isik=isik, hinne=hinne)
            except IsikuHinne.DoesNotExist:
                isik_data[isik] = None

        return render(
            request,
            "hinded/mass_add_hinded.html",
            context={"hinne": hinne, "isik_data": isik_data}
        )

    def post(self, request, *args, **kwargs):
        """Lisa sisestatud hinded andmebaasi."""
        hinne = get_object_or_404(Hinded, pk=kwargs["pk"])
        isikud = Isik.objects.all()

        for isik in isikud:
            try:
                data = IsikuHinne.objects.get(isik=isik, hinne=hinne)
            except IsikuHinne.DoesNotExist:
                data = None

            if data:
                if request.POST.get(f"isik-{isik.id}-hinne", "none") == "none":
                    data.delete()
                else:
                    data.vaartus = request.POST.get(f"isik-{isik.id}-hinne")
                    data.markmed = request.POST.get(f"isik-{isik.id}-markmed", "")
                    data.save()
            else:
                if request.POST.get(f"isik-{isik.id}-hinne", "none") != "none":
                    data = IsikuHinne(
                        isik=isik,
                        hinne=hinne,
                        vaartus=request.POST.get(f"isik-{isik.id}-hinne"),
                        markmed=request.POST.get(f"isik-{isik.id}-markmed", "")
                    )
                    data.save()

        messages.success(request, "Hinnete muutmine õnnestus")
        return HttpResponseRedirect("/")


class AddSingleHinneView(LoginRequiredMixin, View):
    """Vaade ühele õpilasele ühe hinde lisamiseks."""

    def post(self, request, *args, **kwargs):
        """Lisa õpilasele hinne ja tagasta tabeli välja HTML."""
        if (
                request.POST.get("hinne-id", None) is None
                or request.POST.get("isik-id", None) is None
                or request.POST.get("hinne", None) is None
        ):
            return HttpResponseBadRequest()

        isiku_hinne = IsikuHinne(
            hinne_id=request.POST.get("hinne-id"),
            isik_id=request.POST.get("isik-id"),
            vaartus=request.POST.get("hinne"),
            markmed=request.POST.get("markmed", "")
        )
        isiku_hinne.save()

        cell = render_to_string("hinded/hinne_cell.html", {
            "varv": COLORS[isiku_hinne.vaartus],
            "icon": f"{isiku_hinne.vaartus.lower()}-square-fill",
            "markmed": isiku_hinne.markmed,
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
            "vaartus": isiku_hinne.vaartus,
        })

        return JsonResponse({"html": cell, "hinne": isiku_hinne.hinne_id, "isik": isiku_hinne.isik_id})


class RemoveSingleHinne(LoginRequiredMixin, View):
    """Eemalda õpilaselt üks hinne."""

    def post(self, request, *args, **kwargs):
        """Eemalda õpilaselt üks hinne."""
        if request.POST.get("hinne-id", None) is None or request.POST.get("isik-id", None) is None:
            return HttpResponseBadRequest()

        try:
            isiku_hinne = IsikuHinne.objects.get(
                hinne_id=int(request.POST.get("hinne-id")),
                isik_id=int(request.POST.get("isik-id"))
            )
        except IsikuHinne.DoesNotExist:
            return HttpResponseNotFound()

        cell = render_to_string("hinded/add_cell.html", {
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
        })
        isiku_hinne.delete()

        return JsonResponse({"html": cell, "isik": int(request.POST.get("isik-id")), "hinne": int(request.POST.get("hinne-id"))})


class EditSingleHinne(LoginRequiredMixin, View):
    """Vaade ühe õpilase ühe hinde muutmiseks."""

    def post(self, request, *args, **kwargs):
        """Muuda ühe õpilase ühte hinnet."""
        if (
                request.POST.get("hinne-id", None) is None
                or request.POST.get("isik-id", None) is None
                or request.POST.get("hinne", None) is None
        ):
            return HttpResponseBadRequest()

        try:
            isiku_hinne = IsikuHinne.objects.get(
                isik_id=request.POST.get("isik-id"),
                hinne_id=request.POST.get("hinne-id")
            )
        except IsikuHinne.DoesNotExist:
            return HttpResponseNotFound()

        isiku_hinne.vaartus = request.POST.get("hinne")
        isiku_hinne.markmed = request.POST.get("markmed", "")
        isiku_hinne.save()

        cell = render_to_string("hinded/hinne_cell.html", {
            "varv": COLORS[isiku_hinne.vaartus],
            "icon": f"{isiku_hinne.vaartus.lower()}-square-fill",
            "markmed": isiku_hinne.markmed,
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
            "vaartus": isiku_hinne.vaartus,
        })

        return JsonResponse({"html": cell, "isik": isiku_hinne.isik.id, "hinne": isiku_hinne.hinne.id})
