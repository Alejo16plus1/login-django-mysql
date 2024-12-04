from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .forms import CustomUserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from .models import PerfilUsuario, Preg_user, Preguntas, Capturas
from django.contrib.auth.models import User
from .forms import EditProfileForm
from .tokens import account_activation_token  # Asegúrate de importar tu generador de tokens
from django.contrib import messages #mensajes de error
#resetear contraseña
from django.contrib.auth.hashers import make_password
#captura
import imgkit
import uuid


def nosotros(request):
    return render(request, 'core/nosotros.html')


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
                descripcion=user_creation_form.cleaned_data['descripcion'],
                url=user_creation_form.cleaned_data['url']
            )

            
            archivo = user_creation_form.cleaned_data['url']
            nombre_archivo = f"{user.username}_{uuid.uuid4().hex}.jpg"
            direccion_archivo= "static/"+nombre_archivo
            config = imgkit.config(wkhtmltoimage="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe")
            
            
            try:
                imgkit.from_url(archivo, direccion_archivo, config=config)
                Capturas.objects.create(usuario=user, archivo=nombre_archivo)
            except Exception as e:
                messages.error(request, f"Error generando la captura: {e}")
            
                

            messages.success(request, "Registro completado exitosamente. Revisa tu correo para confirmar tu cuenta.")
            
            
            
            

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

        return redirect('registration/preguntas_seguridad')
    else:
        return render(request, 'registration/activation_invalid.html')

#Vista para elegir metodo de recuperacion
def eleccion(request):
    return render(request, 'registration/password_reset.html')

#vista para ir a las preguntaws de seguridad
def recuperar_preguntas(request, aux):
    if aux == 1:
        preguntas=Preguntas.objects.all()
        coleccion={
            'aux' : aux,
            'preguntas':preguntas
        }
        return render(request, 'registration/recuperacion.html', coleccion)
    elif aux== 0:
        username=request.POST.get('usuario')
        if not username:
            messages.error(request, 'El nombre de usuario es obligatorio.')
            return redirect('recuperar_preguntas', aux=1)
        try:
            # Intentar obtener el usuario
            usuario = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'El usuario no existe.')
            return redirect('recuperar_preguntas', aux=1)
        usuario=User.objects.get(username=username)
        if usuario:
            respuestas_correctas=True
            preguntas= Preg_user.objects.filter(usuario=usuario)
            
            for pregunta in preguntas:
                respuesta_usuario=request.POST.get(str(pregunta.pregunta.id))
            
                if respuesta_usuario != pregunta.respuesta:
                    respuestas_correctas = False
            

            if  respuestas_correctas:
                request.session['usuario_id'] = usuario.id #mouseque herramienta misteriosa que nos ayudará mas tarde
                return redirect('reestablecer_contrasena')
            else:
                messages.error(request, 'Las respuestas dadas son incorrectas.')
                return redirect('recuperar_preguntas', aux=1)
        else:
            messages.error(request, 'El usuario no existe.')
            return redirect('recuperar_preguntas', aux=1)
        


# vista para confirmar que las preguntas se guarden
@login_required
def pregunta(request):
    if request.method == 'POST':
        for id_preg, respuesta in request.POST.items():
            if id_preg.isdigit():
                pregunta = Preguntas.objects.get(id=id_preg)

                Preg_user.objects.create(
                    usuario=request.user,
                    pregunta=pregunta,
                    respuesta=respuesta
                )
        return redirect('home')
    preguntas= Preguntas.objects.all()
    return render(request, 'registration/preguntas_seguridad.html', {'preguntas' : preguntas})

#vista para reestablecer contraseña
def reestablecer_contrasena(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            nueva_password = form.cleaned_data.get('nueva_password')

            # agarrar usuario de la mousque herramienta misteriosa
            usuario_id = request.session.get('usuario_id')  
            if not usuario_id:
                messages.error(request, 'Hubo un problema al identificar al usuario.')
                return redirect('recuperar_preguntas', aux=1)
            
            try:
                #crear contraseña
                usuario = User.objects.get(id=usuario_id)
                usuario.password = make_password(nueva_password)  
                usuario.save()
                messages.success(request, 'La contraseña se ha actualizado correctamente.')
                #enviar correo de confirmacion
                subject = 'Cambio de contraseña'
                from_email = 'hiperjesus17@gmail.com'
                to_email = [usuario.email]
                html_content = render_to_string('emails/peligro.html', {'user': usuario})

                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return redirect('home')  
            except User.DoesNotExist:
                messages.error(request, 'El usuario no existe.')
                return redirect('recuperar_preguntas', aux=1)
    else:
        form = PasswordResetForm()
    
    return render(request, 'registration/reestablecer_contrasena.html', {'form': form})


from .models import PerfilUsuario
#Edición de perfil
@login_required
def edit_profile(request):
    try:
        perfil = request.user.perfilusuario
    except PerfilUsuario.DoesNotExist:
        perfil = PerfilUsuario(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito')
            return redirect('myprofile')
    else:
        form = EditProfileForm(instance=perfil)

    context = {
        'form': form
    }
    return render(request, 'core/edit_profile.html', context)


