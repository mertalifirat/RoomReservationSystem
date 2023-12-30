from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import Event, Organization, Room

class UserForm(UserCreationForm):
    username = forms.CharField()
    email = forms.EmailField()
    first_name = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'password1' ,'password2' )

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['orgName', 'orgOwner']

class RoomForm(forms.ModelForm):

    roomName = forms.CharField(max_length=100)
    roomCapacity = forms.IntegerField()
    roomWorkingHours = forms.CharField(max_length=100)
    roomPermissions = forms.MultipleChoiceField(
        choices=[
            ("LIST", "LIST"),
            ("DELETE", "DELETE"),
            ("ADD", "ADD"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Room
        fields = (
            "roomName",
            "roomCapacity",
            "roomWorkingHours",
            "roomPermissions",
        )
class EventForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.CharField()
    category = forms.CharField()
    capacity = forms.IntegerField()
    duration = forms.IntegerField()
    weekly = forms.IntegerField()
    permissions = forms.MultipleChoiceField(
        choices=[
            ("LIST", "LIST"),
            ("DELETE", "DELETE"),
            ("ADD", "ADD"),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Event
        fields = (
            "title",
            "description",
            "category",
            "capacity",
            "duration",
            "weekly",
            "permissions",
         )        