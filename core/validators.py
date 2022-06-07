from django.core.exceptions import ValidationError

from django.core.validators import RegexValidator


class ContainsLetterValidator:

    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError('Le mot de passe doit contenir une lettre', code='password_no_letters')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins une lettre majuscule ou minuscule.'


class ContainsNumberValidator:

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError('Le mot de passe doit contenir un chiffre', code='password_no_numbers')

    def get_help_text(self):
        return 'Votre mot de passe doit contenir au moins un chiffre.'


def validate_username():
    regex_symboles = RegexValidator(r"\W", "Le nom d'utilisateur doit comporter un caractère spécial")

    return regex_symboles
