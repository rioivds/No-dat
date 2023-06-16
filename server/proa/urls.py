"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from . import views
from . import views_alumnos,views_profesores,views_materia

urlpatterns = [
    path('', views.index),
    path('alumnos', views_alumnos.index),
    path('alumnos/nuevo2/', views_alumnos.guardar_alumnos),
    path('alumnos/delete/', views_alumnos.eliminar_alumno),
    path('alumnos/editar/', views_alumnos.editar_alumno),
    path('alumnos/guardar/', views_alumnos.guardar_edit),
    path('alumnos/curso/', views_alumnos.curso),
    path('profesores', views_profesores.index),
    path('profesores/nuevo2/', views_profesores.guardar_profesores),
    path('profesores/delete/', views_profesores.eliminar_profesores),
    path('profesores/editar/', views_profesores.editar_profesores),
    path('profesores/guardar/', views_profesores.guardar_edit),
    path('materias', views_materia.index),
    path('materias/nuevo2/', views_materia.guardar_materia),
    path('materias/delete/', views_materia.eliminar_materia),
    path('materias/editar/', views_materia.editar_materia),
    path('materias/guardar/', views_materia.guardar_materia),
]
