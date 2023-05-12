from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Avalehe vaade."""

    template_name = "hinded/home.html"

    def get_context_data(self, **kwargs) -> dict:
        """Lisa vajalikud andmed vaatele."""
        if self.request.user.is_authenticated:
            return {"isikud": [], "hinded": [], "isiku_hinded": []}

        return {}
