from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User


class RegisterUserForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ModifyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'title', 'bio']
