from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget




class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = [
            'profile_picture', 'phone', 'date_of_birth', 'country',
            'address', 'city', 'state', 'pincode'
        ]
        widgets = {
            'country': CountrySelectWidget(attrs={'class': 'form-select'}),
            'state': forms.Select(attrs={'class': 'form-select'})
        }
