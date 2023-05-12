from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import TextInput, CharField, PasswordInput


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
