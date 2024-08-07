from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


# def validate_year(value):
#     if value < 2000 or value > 2004:
#         raise ValidationError('Niepoprawny rok urodzenia')
#

def validate_login(value):
    if User.objects.filter(username=value):
        raise ValidationError('Loggin in use')
