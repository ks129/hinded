from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import CharField, PasswordInput, TextInput, ModelForm

from hinded.apps.hinded.models import Hinded, Isik


class UserLoginForm(AuthenticationForm):
    """Overwrite default AuthenticationForm to translate labels."""

    username = UsernameField(widget=TextInput(attrs={'autofocus': True}), label='Kasutajanimi')
    password = CharField(
        label="Parool",
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'current-password'})
    )

    error_messages = {
        'invalid_login': 'Vale kasutajanimi või parool.',
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)


class IsikForm(ModelForm):
    """Õpilase lisamise ja muutmise vorm."""

    def __init__(self, *args, **kwargs):
        """Lisa vormi väljadele korralikud nimed."""
        super(IsikForm, self).__init__(*args, **kwargs)
        self.fields["eesnimi"].label = "Õpilase eesnimi"
        self.fields["perenimi"].label = "Õpilase perekonnanimi"

    class Meta:
        """Üldine info õpilase vormi kohta."""

        model = Isik
        fields = ["eesnimi", "perenimi"]

class HindedForm(ModelForm):
    """Hinde lisamise ja muutmise vorm"""

    def __init__(self, *args, **kwargs):
        """midagi"""

        super(HindedForm, self).__init__(*args, **kwargs)
        self.fields["nimi"].label = "Töö nimi"
        self.fields["kirjeldus"].label = "Töö kirjeldus"
        self.fields["aine"].label = "Õppeaine"

    class Meta:
        """Üldine info hinde vormi kohta."""

        model = Hinded
        fields = ["nimi", "kirjeldus", "aine"]


