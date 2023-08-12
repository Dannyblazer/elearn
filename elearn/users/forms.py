from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account
from django.forms import forms
from django.contrib.auth import authenticate

class CustomUserCreation(UserCreationForm):
    class Meta:
        model = Account
        fields = ("email",)

class CustomUserChangeForm(UserCreationForm):
    class CustomUserChangeForm(UserChangeForm):
        class meta:
            model = Account
            fields = ("email",)

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")


class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('email', ) #'username', 'first_name', 'last_name', 'profile_image', 'hide_email'
    
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email {} is already in use.".format(email))
    
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username {} is already in use.".format(username))
    
    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        # account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        # account.first_name = self.cleaned_data['first_name']
        # account.last_name = self.cleaned_data['last_name']
        # account.profile_image = self.cleaned_data['profile_image']
        # account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account