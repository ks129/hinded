from django.views.generic import TemplateView
from .models import Hinded, Isik, IsikuHinne


class HomeView(TemplateView):
    """Avalehe vaade."""

    template_name = "hinded/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Lisa vajalikud andmed vaatele."""
        if self.request.user.is_authenticated:
            return {"isikud": Isik.objects.all(), "hinded": Hinded.objects.all(), "isiku_hinded": IsikuHinne.objects.all()}

        return {}
