from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from core.models import User


class SignupForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input', "placeholder": " ", "autocomplete": "off"})
        self.fields['first_name'].widget.attrs.update({'class': 'input', "placeholder": " ", "autocomplete": "off"})
        self.fields['last_name'].widget.attrs.update({'class': 'input', "placeholder": " ", "autocomplete": "off"})
        self.fields['password1'].widget.attrs.update({'class': 'input', "placeholder": " "})
        self.fields['password2'].widget.attrs.update({'class': 'input', "placeholder": " "})
        self.fields['email'].widget.attrs.update({'class': 'input', "placeholder": " ", "autocomplete": "off"})
        self.fields['email'].label = 'Email'

        # Allow to override the error message if the password doesn't match with the confirmation password'
        self.error_messages['password_mismatch'] = 'Le mot de passe doit être identique'

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        """Check if the form is validated."""

        # call the default "clean" method to perform
        super().clean()

        # extract user input data
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        # Check if the email used doesn't already exist
        if User.objects.filter(email=email).exists():
            self._errors['email'] = self.error_class([
                "Cette adresse mail est déjà utilisée"
            ])

        if User.objects.filter(username=username).exists():
            self._errors['username'] = self.error_class([
                "Ce nom d'utilisateur est déjà utilisé"
            ])

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utilisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")
