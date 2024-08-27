from django import forms
from .models import *

class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False,label='Sex')
 
    
class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(queryset=SizeShoe.objects.all(), required=True, label='Select Size')
    
    