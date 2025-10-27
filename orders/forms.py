from django import forms
from .models import Address
from django.utils.safestring import mark_safe
import pycountry
import re

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'line1', 'line2', 'city', 'state', 'postcode', 'country', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State/Province'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add suggestion text below each field
        suggestions = {
            'full_name': 'Enter your full legal name as it appears on official documents',
            'line1': 'Street address, P.O. box, company name',
            'line2': 'Apartment, suite, unit, building, floor, etc.',
            'city': 'Enter your city name',
            'state': 'Enter your state, province, or region',
            'postcode': 'Enter your postal or ZIP code',
            'country': 'Enter your country name',
            'phone': 'Include country and area code (e.g. +1-555-555-5555)'
        }
        
        for field_name, suggestion in suggestions.items():
            self.fields[field_name].help_text = mark_safe(f'<small class="text-muted">{suggestion}</small>')
            # Use pycountry for country choices
            country_choices = [(country.alpha_2, country.name) for country in pycountry.countries]
            self.fields['country'] = forms.ChoiceField(
                choices=[('', 'Select Country')] + country_choices,
                widget=forms.Select(attrs={'class': 'form-control'}),
                help_text=self.fields['country'].help_text
            )

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name', '').strip()
        if not full_name:
            raise forms.ValidationError("Full name is required.")
        return full_name

    def clean_postcode(self):
        postcode = self.cleaned_data.get('postcode', '').strip()
        if not postcode:
            raise forms.ValidationError("Postal code is required.")
        return postcode

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise forms.ValidationError("Phone number is required.")
        return phone

    def clean_country(self):
        country = self.cleaned_data.get('country', '').strip()
        if not country:
            raise forms.ValidationError("Country is required.")
        return country

    # Validate phone number format (basic example)
    def validate_phone_number(self, phone):
        pattern = re.compile(r'^\+?1?\d{9,15}$')
        return pattern.match(phone) is not None

    # Validate postal code format (basic example)
    def validate_postal_code(self, postcode):
        pattern = re.compile(r'^[A-Za-z0-9\s-]{3,10}$')
        return pattern.match(postcode) is not None