from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CurstomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import PerfilUsuario

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

@login_required
def cursos(request):
    return render(request, 'core/cursos.html')

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CurstomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CurstomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()  # Guarda el usuario

            # Crear el perfil asociado
            PerfilUsuario.objects.create(
                user=user,
                cedula=user_creation_form.cleaned_data['cedula'],
                nacionalidad=user_creation_form.cleaned_data['nacionalidad'],
                fecha_nacimiento=user_creation_form.cleaned_data['fecha_nacimiento']
            )

            # Autenticar y loguear al usuario
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
    return render(request, 'registration/Register.html', data)