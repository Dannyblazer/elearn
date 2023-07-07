from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreation(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserCreationForm):
    class CustomUserChangeForm(UserChangeForm):
        class meta:
            model = CustomUser
            fields = ("email",)
            