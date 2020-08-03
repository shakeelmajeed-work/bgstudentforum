from django import forms
from .models import ad

class AdForm(forms.ModelForm):
    class Meta:
        model = ad
        fields = ['ad_link', 'image']
