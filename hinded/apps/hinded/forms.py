from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import CharField, ModelForm, PasswordInput, TextInput, Textarea

from .models import Hinded, Isik


class UserLoginForm(AuthenticationForm):
    """Tavalise AuthenticationFormi ülekirjutamine, et lisada eestikeelsed väljade nimed."""

    username = UsernameField(widget=TextInput(attrs={"autofocus": True}), label="Kasutajanimi")
    password = CharField(
        label="Parool",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"})
    )

    error_messages = {
        "invalid_login": "Vale kasutajanimi või parool.",
    }


class IsikForm(ModelForm):
    """Vorm õpilaste lisamiseks ning muutmiseks."""

    def __init__(self, *args, **kwargs):
        """Lisa vormi väljadele eestikeelsed korralikud nimed."""
        super(IsikForm, self).__init__(*args, **kwargs)
        self.fields["eesnimi"].label = "Õpilase eesnimi"
        self.fields["perenimi"].label = "Õpilase perekonnanimi"
        self.fields["kood"].label = "Ligipääsukood"
        self.fields["kood"].error_messages = {
            "unique": "Õpilaste koodid peavad olema unikaalsed.",
        }

    class Meta:
        """Üldine info õpilase vormi kohta."""

        model = Isik
        fields = ["eesnimi", "perenimi", "kood"]


class HindedForm(ModelForm):
    """Vorm hinnete lisamiseks ja muutmiseks."""

    def __init__(self, *args, **kwargs):
        """Määra igale väljale eestikeelne korralik nimetus."""
        super(HindedForm, self).__init__(*args, **kwargs)
        self.fields["nimi"].label = "Nimi"
        self.fields["kirjeldus"].label = "Kirjeldus"
        self.fields["kirjeldus"].widget = Textarea(attrs={"rows": 3})
        self.fields["aine"].label = "Õppeaine"

    class Meta:
        """Üldine info hinde vormi kohta."""

        model = Hinded
        fields = ["nimi", "kirjeldus", "aine"]
