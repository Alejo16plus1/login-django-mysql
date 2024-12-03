from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from .models import PerfilUsuario
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string
# Create your views here.

def home(request):
    return render(request, 'core/home.html')

@login_required
def cursos(request):
    return render(request, 'core/cursos.html')

def myprofile(request):
    return render(request, 'core/profile.html')

def exit(request):
    logout(request)
    return redirect('home')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()

            PerfilUsuario.objects.create(
                user=user,
                cedula=user_creation_form.cleaned_data['cedula'],
                nacionalidad=user_creation_form.cleaned_data['nacionalidad'],
                fecha_nacimiento=user_creation_form.cleaned_data['fecha_nacimiento']
            )

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)

            subject = 'Bienvenido a Nuestro Sitio' 
            from_email = 'tucorreo@gmail.com' 
            to_email = [user.email] 
            html_content = render_to_string('emails/bienvenida.html', {'user': user}) 
            # Crear el correo electrónico con HTML 
            msg = EmailMultiAlternatives(subject, '', from_email, to_email) 
            msg.attach_alternative(html_content, "text/html") 
            msg.send()

            return redirect('home')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)