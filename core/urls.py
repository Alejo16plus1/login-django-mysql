"""
URL configuration for logintarea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import home, cursos, exit, register, myprofile, activate, eleccion, pregunta, recuperar_preguntas, reestablecer_contrasena, edit_profile, nosotros 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', home, name='home'),
    path('cursos/', cursos, name='cursos'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('myprofile/', myprofile, name='myprofile'),
    path('eleccion/', eleccion, name='eleccion'),
    path('pregunta/', pregunta, name='pregunta'),
    path('recuperar_preguntas/<int:aux>/', recuperar_preguntas, name='recuperar_preguntas'),
    path('reestablecer/', reestablecer_contrasena, name='reestablecer_contrasena'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', activate, name='activate'), 
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('nosotros/', nosotros, name='nosotros'),
]






