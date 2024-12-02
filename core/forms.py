from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario

class CurstomUserCreationForm(UserCreationForm):
    cedula = forms.CharField(max_length=20, required=True)
    nacionalidad = forms.CharField(max_length=50, required=True)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cedula', 'nacionalidad', 'fecha_nacimiento']