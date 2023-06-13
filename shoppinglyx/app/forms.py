from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from .models import *


class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    # first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        label = {'email': 'Email'}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control'})}

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError('Email already exists')
        return email


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'autofocus': True}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(
        attrs={'class': 'form-control', "autocomplete": "current-password"}))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', strip=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autofocus': True, 'autocomplate': 'current-password'}))
    new_password1 = forms.CharField(label='New password', strip=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplate': 'new-password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='New password confirmation', strip=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplate': 'new-password'}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_('Enter your email to reset '), widget=forms.EmailInput(
        attrs={'class': 'form-control', 'autocomplate': 'email', 'autofocus': True,'PlaceHolder':'Enter your email to reset password'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autofocus': True, 'autocomplate': 'new-password'}), help_text=password_validation.password_validators_help_text_html)
    new_password2 = forms.CharField(label='New password confirmation', strip=True, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'autocomplate': 'new-password'}))

# customer profile creation form

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        exclude=('user',)
        widgets={ 'name':forms.TextInput(attrs={'class':'form-control border-dark'}),
        'locality':forms.TextInput(attrs={'class':'form-control border-dark'}),
        'city':forms.TextInput(attrs={'class':'form-control border-dark'}),
        'state':forms.Select(attrs={'class':'form-control border-dark'}),
        'pincode':forms.NumberInput(attrs={'class':'form-control border-dark'}),
        'phone':forms.NumberInput(attrs={'class':'form-control border-dark'}),
         }

        