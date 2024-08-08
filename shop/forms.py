import django.forms as forms
from django.core.exceptions import ValidationError

from .models import Product

from .validators import validate_login


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(forms.Form):
    username = forms.CharField(label='Username', validators=[validate_login])
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')

    def clean(self) -> dict[str, any]:
        data = super().clean()
        if data['password1'] != data['password2']:
            raise ValidationError('passwords do not match')
        return data


class SearchForm(forms.Form):
    searched = forms.CharField(label='Search')