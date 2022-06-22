from dataclasses import field
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# code here


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'username', 'email', 'password', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name....', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name..'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username..'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email...'}),
        }
