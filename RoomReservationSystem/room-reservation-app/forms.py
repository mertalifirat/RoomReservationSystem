from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'password1' ,'password2' )