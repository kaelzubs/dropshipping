# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        })
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
            }),
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            "class": "form-control",
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
        }
    ))
    
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Your Name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "Your Email"
    }))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Subject"
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Your Message", "rows": 5
    }))

