from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class create_cook_form(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class account_update_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
