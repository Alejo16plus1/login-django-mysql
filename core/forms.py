from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario
from datetime import date

class CustomUserCreationForm(UserCreationForm): 
    NACIONALIDADES_CHOICES = [ ('VE', 'Venezuela'), 
         ('CO', 'Colombia'), 
         ('AR', 'Argentina'), 
         ('BR', 'Brasil'), 
         ('CL', 'Chile'),
         ]
        
    cedula = forms.CharField(max_length=20, required=True)
    nacionalidad = forms.ChoiceField(choices=NACIONALIDADES_CHOICES, required=True)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    direccion = forms.CharField(max_length=255, required=True,)
    facebook = forms.CharField(max_length=20, required=False)
    instagram = forms.CharField(max_length=20, required=False)
    tiktok = forms.CharField(max_length=20, required=False)
    twitter = forms.CharField(max_length=20, required=False)
    descripcion = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cedula', 'nacionalidad', 'fecha_nacimiento', 'direccion', 'facebook', 'instagram', 'tiktok', 'twitter', 'descripcion']
        widgets = {
            'descripcion': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'})
        }
        
    def clean_fecha_nacimiento(self): 
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento'] 
        if fecha_nacimiento and fecha_nacimiento > date.today(): 
            raise forms.ValidationError("La fecha de nacimiento no puede ser una fecha futura.") 
        return fecha_nacimiento