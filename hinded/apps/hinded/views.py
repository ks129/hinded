from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import CreateView, DeleteView, TemplateView, UpdateView

from .forms import HindedForm, IsikForm
from .models import Hinded, Isik, IsikuHinne

ICONS = {
    "X": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#EE4B2B" class="bi bi-x-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm3.354 4.646L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 1 1 .708-.708z"/></svg>',  # noqa: E501
    "1": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#EE4B2B" class="bi bi-1-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Zm7.283 4.002V12H7.971V5.338h-.065L6.072 6.656V5.385l1.899-1.383h1.312Z"/></svg>',  # noqa: E501
    "2": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#EE4B2B" class="bi bi-2-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Zm4.646 6.24v.07H5.375v-.064c0-1.213.879-2.402 2.637-2.402 1.582 0 2.613.949 2.613 2.215 0 1.002-.6 1.667-1.287 2.43l-.096.107-1.974 2.22v.077h3.498V12H5.422v-.832l2.97-3.293c.434-.475.903-1.008.903-1.705 0-.744-.557-1.236-1.313-1.236-.843 0-1.336.615-1.336 1.306Z"/></svg>',  # noqa: E501
    "3": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#DFFF00" class="bi bi-3-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Zm5.918 8.414h-.879V7.342h.838c.78 0 1.348-.522 1.342-1.237 0-.709-.563-1.195-1.348-1.195-.79 0-1.312.498-1.348 1.055H5.275c.036-1.137.95-2.115 2.625-2.121 1.594-.012 2.608.885 2.637 2.062.023 1.137-.885 1.776-1.482 1.875v.07c.703.07 1.71.64 1.734 1.917.024 1.459-1.277 2.396-2.93 2.396-1.705 0-2.707-.967-2.754-2.144H6.33c.059.597.68 1.06 1.541 1.066.973.006 1.6-.563 1.588-1.354-.006-.779-.621-1.318-1.541-1.318Z"/></svg>',  # noqa: E501
    "4": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#50C878" class="bi bi-4-square-fill" viewBox="0 0 16 16"><path d="M6.225 9.281v.053H8.85V5.063h-.065c-.867 1.33-1.787 2.806-2.56 4.218Z"/><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Zm5.519 5.057c.22-.352.439-.703.657-1.055h1.933v5.332h1.008v1.107H10.11V12H8.85v-1.559H4.978V9.322c.77-1.427 1.656-2.847 2.542-4.265Z"/></svg>',  # noqa: E501
    "5": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#228B22" class="bi bi-5-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2Zm5.994 12.158c-1.57 0-2.654-.902-2.719-2.115h1.237c.14.72.832 1.031 1.529 1.031.791 0 1.57-.597 1.57-1.681 0-.967-.732-1.57-1.582-1.57-.767 0-1.242.45-1.435.808H5.445L5.791 4h4.705v1.103H6.875l-.193 2.343h.064c.17-.258.715-.68 1.611-.68 1.383 0 2.561.944 2.561 2.585 0 1.687-1.184 2.806-2.924 2.806Z"/></svg>',  # noqa: E501
    "add": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="gray" class="bi bi-plus-square-fill" viewBox="0 0 16 16"><path d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm6.5 4.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3a.5.5 0 0 1 1 0z"/></svg>',  # noqa: E501
}


class HomeView(TemplateView):
    """Avalehe vaade."""

    template_name = "hinded/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Lisa hinnete andmed vaatele."""
        if self.request.user.is_authenticated:
            isikud = {}
            hinded = list(Hinded.objects.all())
            initial_isikud = list(Isik.objects.all())
            isiku_hinded = IsikuHinne.objects.all()
            # Valib kõik õpilaste hinded korraga, vähendab SQL päringute arvu andmebaasile.
            list(isiku_hinded)
            ids = {}

            for isik in initial_isikud:
                ids[(f"{isik.eesnimi} {isik.perenimi}", isik.id)] = isik.id
                isikud[(f"{isik.eesnimi} {isik.perenimi}", isik.id)] = []

                for hinne in hinded:
                    data = {
                        "vaartus": None,
                        "hinde_id": hinne.id,
                        "hinde_nimi": hinne.nimi,
                        "isiku_id": None,
                        "markmed": None,
                        "ikoon": ICONS["add"],
                    }
                    try:
                        isiku_hinne = isiku_hinded.get(hinne=hinne, isik=isik)
                        data["vaartus"] = isiku_hinne.vaartus
                        data["isiku_id"] = isiku_hinne.isik_id
                        data["markmed"] = isiku_hinne.markmed
                        data["ikoon"] = ICONS[isiku_hinne.vaartus]
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
    """Vaade õpilase loomiseks."""

    model = Isik
    success_url = "/"
    success_message = "Õpilase loomine õnnestus"
    form_class = IsikForm
    template_name = "hinded/create_isik.html"


class UpdateIsikView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Vaade õpilase uuendamiseks."""

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
    """Lisa kõigi õpilaste hinded korraga."""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Lisa vaatele vajalikud andmed olemasolevate hinnete kohta."""
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

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
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
    """Vaade ühele õpilasele ühe hinde lisamiseks AJAX-i kaudu."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Lisa õpilasele hinne ja tagasta tabeli välja HTML ning ID-d JSON formaadis."""
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
            "ikoon": ICONS[isiku_hinne.vaartus],
            "markmed": isiku_hinne.markmed,
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
            "vaartus": isiku_hinne.vaartus,
        })

        return JsonResponse({
            "html": cell,
            "hinne": isiku_hinne.hinne_id,
            "isik": isiku_hinne.isik_id
        })


class RemoveSingleHinne(LoginRequiredMixin, View):
    """Eemalda õpilaselt üks hinne AJAX-i kaudu."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Eemalda õpilaselt üks hinne ning tagasti JSON formaadis nupu HTML ning ID-d."""
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
            "ikoon": ICONS["add"],
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
        })
        isiku_hinne.delete()

        return JsonResponse({
            "html": cell,
            "isik": int(request.POST.get("isik-id")),
            "hinne": int(request.POST.get("hinne-id")),
        })


class EditSingleHinne(LoginRequiredMixin, View):
    """Vaade ühe õpilase ühe hinde muutmiseks AJAX-i kaudu."""

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Muuda ühe õpilase ühte hinnet ning tagasta uus HTML JSON formaadis."""
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
            "ikoon": ICONS[isiku_hinne.vaartus],
            "markmed": isiku_hinne.markmed,
            "isik_id": isiku_hinne.isik.id,
            "isik_name": f"{isiku_hinne.isik.eesnimi} {isiku_hinne.isik.perenimi}",
            "hinde_id": isiku_hinne.hinne.id,
            "hinde_nimi": isiku_hinne.hinne.nimi,
            "vaartus": isiku_hinne.vaartus,
        })

        return JsonResponse({
            "html": cell,
            "isik": isiku_hinne.isik.id,
            "hinne": isiku_hinne.hinne.id,
        })


class ViewIsikHinded(View):
    """Vaade õpilastele oma hinnete vaatamiseks."""

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Küsi õpilaselt koodi oma hinnete vaatamiseks."""
        return render(request, "hinded/request_hinded.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Kontrolli õpilase koodi ning näida hindeid."""
        if request.POST.get("kood") is None:
            messages.error(request, "Kood on vajalik hinnete nägemiseks.")
            return render(request, "hinded/request_hinded.html")

        try:
            isik = Isik.objects.get(kood=request.POST.get("kood"))
        except Isik.DoesNotExist:
            messages.error(
                request,
                """Sellise koodiga õpilast ei ole.
                Pange tähele, et suurtel ja väikestel tähtedel tehakse vahet."""
            )
            return render(request, "hinded/request_hinded.html")

        hinded = []
        for hinne in IsikuHinne.objects.filter(isik=isik):
            hinded.append({
                "ikoon": ICONS[hinne.vaartus],
                "markmed": hinne.markmed,
                "hinne": hinne.hinne.nimi,
                "hinde_kirjeldus": hinne.hinne.kirjeldus,
                "hinde_oppeaine": hinne.hinne.aine,
            })

        hinded.reverse()
        return render(request, "hinded/isiku_hinded.html", {
            "hinded": hinded,
            "isik": isik,
        })
