from django.forms import ModelForm
from .models import * 
from django import forms

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields ='__all__'
        exclude = ['user']
        labels = {
            'realname':'Name',
            'phonenumber':'Phone number'
        }
    