from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_login(value):
    if User.objects.filter(username=value):
        raise ValidationError('Loggin in use')
