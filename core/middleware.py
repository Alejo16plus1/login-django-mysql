from django.shortcuts import redirect
from django.urls import reverse
from .models import Preg_user

class redirect_preguntas:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Rutas excluidas de la redirección
            excluded_paths = [
                reverse('pregunta'),  
                reverse('exit'),              
            ]
            # Verificar si el usuario no ha completado las preguntas y no está en una ruta excluida
            if not Preg_user.preguntas_completadas(request.user) and request.path not in excluded_paths:
                return redirect('pregunta')  # Redirigir al formulario de preguntas

        return self.get_response(request)