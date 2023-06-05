from django.contrib.auth import password_validation
from store.models import Address, FeedBack, PayingWay
from django import forms
import django
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from django.forms.fields import CharField
from django.utils.translation import gettext, gettext_lazy as _
import re


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

class PayingWayForm(forms.ModelForm):
    class Meta:
        model = PayingWay
        fields = ['card_number', ]
        labels = {'card_number':"Номер картки", }
        widgets = {'card_number': forms.TextInput(attrs={'input_type': 'number','class': 'form-control', 'id':'card_number',
                                                 'placeholder': 'Введіть свій номер картки'}),}

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if len(str(card_number)) == 16:
            raise forms.ValidationError("Длина номера карты - 16 символов")
        return card_number

    # def clean(self):
    #     cleaned_data = super().clean()
    #     card_number = cleaned_data.get('card_number')
    #     cvv = cleaned_data.get('CVV')
    #     if not card_number:
    #         raise forms.ValidationError("Поле 'Номер картки' обязательно для заполнения.")
    #     if not cvv:
    #         raise forms.ValidationError("Поле 'CVV' обязательно для заполнения.")
    #     if len(str(cvv)) != 3:
    #         raise forms.ValidationError("CVV должен состоять из 3 цифр.")
    #     return cleaned_data

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['locality', 'city', 'state']
        labels = {'locality':"Країна", 'city':"Місто", 'state':"Штат"}
        widgets = {'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Країна'}),
                   'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місто'}),
                   'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Штат або столиця'})}

    def clean_locality(self):
        locality = self.cleaned_data['locality']
        if not re.match(r'^[A-Za-zА-Яа-яІіЇїЄєҐґ\s]*$', locality):
            raise forms.ValidationError("Введіть правильну країну")
        return locality

    def clean_city(self):
        city = self.cleaned_data['city']
        if not re.match(r'^[A-Za-zА-Яа-яІіЇїЄєҐґ\s]*$', city):
            raise forms.ValidationError("Введіть правильне місто")
        return city

    def clean_state(self):
        state = self.cleaned_data['state']
        if not re.match(r'^[A-Za-zА-Яа-яІіЇїЄєҐґ\s]*$', state):
            raise forms.ValidationError("Введіть правильний штат")
        return state

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['feedback']
        labels = {'feedback': "Повідомлення"}
        widgets = {'feedback': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введіть ваше повідомлення'})}

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise forms.ValidationError("Введіть правильну адресу електронної пошти")
        return email

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
