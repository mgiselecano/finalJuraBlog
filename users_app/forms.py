from django import forms
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import *
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# POST
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Form_new_post (forms.Form):
    title = forms.CharField(label="Título", widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField (label="Texto", widget=forms.Textarea (attrs={"class": "form:control" }))
    author = forms.CharField (label="Autor", widget=forms.TextInput (attrs={"class": "form:control" }))
    category = forms.CharField (label="Categoría", widget=forms.TextInput (attrs={"class": "form:control" }))
    tags = forms.CharField (label="Etiquetas", widget=forms.TextInput (attrs={"class": "form:control" }))


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AUTHOR
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Form_new_author (forms.Form):
    email = forms.EmailField (label="E-mail")
    pseudonym = forms.CharField(label="Alias")
    expertise = forms.CharField(label="Especialización")
    academic_titles = forms.CharField(label="Profesión")


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class User_update_form(UserChangeForm):
    username = forms.CharField(label="Usuario")
    email = forms.CharField(label="E-mail")
    first_name = forms.CharField(label="Nombres")
    last_name = forms.CharField(label="Apellidos")

    password = forms.CharField(
        label="Contraseña actual",
        help_text="",
        required=True,
        widget=forms.PasswordInput,
    )

    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Repita la contraseña",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password1', 'password2')


    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return password2



# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AVATAR
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Avatar_Create_Form (forms.Form):
    imagen = forms.ImageField(label="Imagen de perfil")
  


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTACT FORM
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class Contact_form(forms.Form):
    name = forms.CharField(label='Nombres', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Asunto', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Mensaje', widget=forms.Textarea(attrs={'class': 'form-control'}))
    

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        body = f"Nombre: {name}\nEmail: {email}\n\nMensaje:\n{message}"
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_TO_EMAIL])
