from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Preg_user, Preguntas
from datetime import date
import bleach

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
    url = forms.URLField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cedula', 'nacionalidad', 'fecha_nacimiento', 'direccion', 'facebook', 'instagram', 'tiktok', 'twitter', 'descripcion','url']
        widgets = {
            'descripcion': forms.PasswordInput(attrs={'class': 'form-control form-control-sm'})
        }

    #validacion de fecha de nacimiento    
    def clean_fecha_nacimiento(self): 
        fecha_nacimiento = self.cleaned_data['fecha_nacimiento'] 
        if fecha_nacimiento and fecha_nacimiento > date.today(): 
            raise forms.ValidationError("La fecha de nacimiento no puede ser una fecha futura.") 
        return fecha_nacimiento
    # Validacion de cedula
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if PerfilUsuario.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError('El número de cedula ya se encuentra registrado')
        return cedula
    # validar url
    def clean_url(self):
        url = self.cleaned_data.get('url', '')
        if url and not url.startswith('https://'):
            raise forms.ValidationError('La URL debe comenzar con "https://".')
        return url
        
    # #validacion de correo temporalmente comentado
    # def clean_email(self):
    #     email=self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Este correo ya está registrado')
          #return email
    
    # def clean_descripcion(self):
    #     descripcion=self.cleaned_data.get('descripcion', '')

    #     etiquetas_permitidas =[
    #         'b','i','u','a','p','br','strong', 'em', 'mark'
    #     ]
    #     atributos_permitidos={
    #         'a' : ['href','tittle','target']
    #     }

    #     descripcion_depurada= bleach.clean(
    #         descripcion, tags=etiquetas_permitidas, attributes=atributos_permitidos, strip=True
    #     )
    #     return descripcion_depurada

    
    
class PasswordResetForm(forms.Form):
    nueva_password = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        required=True
    )
    confirmar_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get("nueva_password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if nueva_password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data
    
# formulario para la creacion de preguntas de seguridad

#*class preguntasform(forms.ModelForm):

    # preguntas = Preguntas.objects.all()
    # respuesta= []
    # pregunta = []
    # aux=1
    # for aux1 in preguntas:
    #     pregunta[aux]=aux1.Pregunta
    #     respuesta[aux]= forms.CharField(max_length=30, required=True)
    #     aux+=1

    # class Meta:
    #     model = Preg_user
    #     fields = ['pregunta', 'respuesta']
    #     widgets = {
    #         'pregunta': forms.Select(attrs={'class': 'form-control'}),
    #         'respuesta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu respuesta aquí'}),
    #     }
    #     labels = {
    #         'pregunta': 'Selecciona una pregunta de seguridad',
    #         'respuesta': 'Escribe tu respuesta'
