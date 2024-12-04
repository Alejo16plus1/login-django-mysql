from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PerfilUsuario(models.Model):
    NACIONALIDADES_CHOICES = [ 
        ('VE', 'Venezuela'),
        ('CO', 'Colombia'),
        ('AR', 'Argentina'),
        ('BR', 'Brasil'),
        ('CL', 'Chile'), 
        # Agrega más nacionalidades según sea necesario 
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=20, unique=True)
    nacionalidad = models.CharField(max_length=50, choices=NACIONALIDADES_CHOICES)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True)
    facebook = models.CharField(max_length=20, null=True, blank=True)
    instagram = models.CharField(max_length=20, null=True, blank=True)
    tiktok = models.CharField(max_length=20, null=True, blank=True)
    twitter = models.CharField(max_length=20, null=True, blank=True)
    descripcion = models.CharField(max_length=250, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
# modelo para las preguntas de seguridad
class Preguntas(models.Model):
    OPCIONES_PREGUNTAS = [
        ('color_favorito', 'Color favorito'),
        ('auto_favorito', 'Auto favorito'),
        ('segundo_nombre_papa_mama', 'Segundo nombre de papá/mamá'),
        ('pelicula_favorita', 'Película favorita')
    ]

    Pregunta= models.CharField(max_length=30, choices=OPCIONES_PREGUNTAS)
    def __str__(self):
        # Devuelve el texto legible de la pregunta
        return dict(self.OPCIONES_PREGUNTAS).get(self.Pregunta, self.Pregunta)

# tabla intermedia entre user y preguntas
class Preg_user(models.Model):
    pregunta = models.ForeignKey(Preguntas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    respuesta = models.CharField(max_length=30, null=False)
    # funcion para definir si las preguntas llenas están completas
    @staticmethod
    def preguntas_completadas(usuario):
        
        preguntas_respondidas = Preg_user.objects.filter(usuario=usuario).count()
        return preguntas_respondidas == 4
    
#modelo de capturas
class Capturas(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    archivo = models.CharField(max_length=255)  
    fecha_creacion = models.DateTimeField(auto_now_add=True)
