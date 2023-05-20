from django.apps import AppConfig


class HindedConfig(AppConfig):
    """Hinnete app'i põhiline konfiguratsioon."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "hinded.apps.hinded"
