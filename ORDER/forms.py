from django.forms import ModelForm
from .models import * 
from django import forms
from USER.models import *

class ConfirmForm(ModelForm):
    class Meta:
        model = Profile
        fields ='__all__'
        exclude = ['user','realname','email']
        labels = {
            'phonenumber':'Phone number'
        }
    