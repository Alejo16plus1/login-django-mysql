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

    def __str__(self):
        return self.user.username