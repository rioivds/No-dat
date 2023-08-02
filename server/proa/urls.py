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

from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path, re_path
from . import views_alumnos,views_profesores,views_materia,views_calificaciones, views_informes, views_graficos_barra,views_graficos_torta

urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('materias/guardar/', views_materia.guardar_edit),
    path('calificaciones', views_calificaciones.index),
    path('calificaciones/nuevo2/', views_calificaciones.guardar_calificaciones),
    path('calificaciones/delete/', views_calificaciones.eliminar_calificaciones),
    path('calificaciones/editar/', views_calificaciones.editar_calificaciones),
    path('calificaciones/guardar/', views_calificaciones.guardar_edit),
    path('informes', views_informes.index),
    path('informes/generar', views_informes.generar_informe),
    path('graficos/', views_graficos_barra.index, name='index'),
    path('alumnos/importar/', views.importar_alumnos_view, name='importar_alumnos'),
    path('alumnos/exportar/', views.exportar_alumnos, name='exportar_alumnos'),
    path('materias/importar_materias/', views.importar_materias, name='importar_materias'),
    path('calificaciones/importar_calificaciones/', views.importar_calificaciones, name='importar_calificaciones'),
    re_path(r'^graficos/materia/(?P<materia_nombre>.+)/$', views_graficos_barra.grafico_materia, name='grafico_materia'),
    path('graficos/materias_por_curso/<int:curso_anio>/', views_graficos_barra.materias_por_curso, name='materias_por_curso'),
    path('graficos/grafico_torta/', views_graficos_torta.grafico_torta, name='grafico_torta'),
    path('graficos/torta/<int:materia_id>/', views_graficos_torta.grafico_torta_materia, name='grafico_torta_materia'),
    



]