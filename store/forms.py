from django.contrib.auth import password_validation
from store.models import Address
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label="Підтвердити Пароль", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Підтвердити Пароль'}))
    email = forms.CharField(label="Електронна пошта", required=True,
                            widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Електронна пошта'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': "Ім'я"}
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"})}


class LoginForm(AuthenticationForm):
    username = UsernameField(label=_("Ім'я"),widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Пароль"), strip=False, widget=forms.PasswordInput(attrs={
        'autocomplete': 'current-password', 'class': 'form-control'}))


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        widgets = {'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Популярне місце, '
                                                                                              'як ресторан, релігійний '
                                                                                              'сайт тощо.'}),
                   'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місто'}),
                   'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Штат або столиця'})}


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Старий пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'auto-focus': True, 'class': 'form-control',
               'placeholder': 'Поточний пароль'}))
    new_password1 = forms.CharField(label=_("Новий пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Новий пароль'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Підтвердити пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Підтвердити пароль'}))


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Електронна пошта"), max_length=254,
                             widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))


class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("Новий пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
                                    help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Підтвердити пароль"), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control'}))
