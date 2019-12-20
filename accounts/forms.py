from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'autocomplete': 'off', 'class': 'form-control'}
        self.fields['password'].widget.attrs = {'autocomplete': 'off', 'class': 'form-control'}