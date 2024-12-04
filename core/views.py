from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .models import PerfilUsuario
from .tokens import account_activation_token  # Asegúrate de importar tu generador de tokens

User = get_user_model()

def home(request):
    return render(request, 'core/home.html')

@login_required
def cursos(request):
    return render(request, 'core/cursos.html')

@login_required
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
            user = user_creation_form.save(commit=False)
            user.is_active = False  # El usuario no estará activo hasta que confirme su correo
            user.save()

            PerfilUsuario.objects.create(
                user=user,
                cedula=user_creation_form.cleaned_data['cedula'],
                nacionalidad=user_creation_form.cleaned_data['nacionalidad'],
                fecha_nacimiento=user_creation_form.cleaned_data['fecha_nacimiento'],
                direccion=user_creation_form.cleaned_data['direccion'], 
                facebook=user_creation_form.cleaned_data['facebook'], 
                instagram=user_creation_form.cleaned_data['instagram'], 
                tiktok=user_creation_form.cleaned_data['tiktok'], 
                twitter=user_creation_form.cleaned_data['twitter'], 
                descripcion=user_creation_form.cleaned_data['descripcion']
            )

            # Enviar correo de confirmación
            current_site = get_current_site(request)
            subject = 'Confirma tu cuenta'
            from_email = 'hiperjesus17@gmail.com'
            to_email = [user.email]
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            html_content = render_to_string('emails/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('password_reset_done')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        # Enviar correo de bienvenida
        subject = 'Bienvenido a Nuestro Sitio'
        from_email = 'hiperjesus17@gmail.com'
        to_email = [user.email]
        html_content = render_to_string('emails/bienvenida.html', {'user': user})

        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')


