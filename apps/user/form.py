from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()

class RegisterUserForm(UserCreationForm):
    # email = forms.EmailField(required=True, label='Email')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ModifyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'title', 'bio']
