from django import forms
from django.forms import ModelForm
from twitteruser.models import MyUser


class AddUserForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ["username", "password", "display_name"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
