import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Profesor, Usuario, Alumno, Materia, Calificaciones
from django.db import connection
from django.shortcuts import get_object_or_404
import openpyxl


def filtro_materias(request):
    query = request.GET.get('query', '')
    campo_busqueda = request.GET.get('campo', 'nombre')  # Por defecto, buscar por nombre

    if campo_busqueda == 'id':
        materia = Materia.objects.filter(id__icontains=query)
    elif campo_busqueda == 'nombre':
        materia = Materia.objects.filter(nombre__icontains=query)
    elif campo_busqueda == 'curso':
        materia = Materia.objects.filter(curso=query)
    elif campo_busqueda == 'profesor':
        materia = Materia.objects.filter(profesor__nombre__icontains=query)
    elif campo_busqueda == 'horas_catedra':
        materia = Materia.objects.filter(horas_catedra=query)
    
    return render(request, 'materias/index.html', {'materias': materia, 'campo_busqueda': campo_busqueda, 'query': query})


def filtro_calificaciones(request):
    query = request.GET.get('query', '')
    campo_busqueda = request.GET.get('campo', 'alumno')  # Por defecto, buscar por nota

    if campo_busqueda == 'id':
        calificacion = Calificaciones.objects.filter(id__icontains=query)
    elif campo_busqueda == 'alumno':
        calificacion = Calificaciones.objects.filter(alumno__nombre__icontains=query)
    elif campo_busqueda == 'curso':
        calificacion = Calificaciones.objects.filter(curso=query)
    elif campo_busqueda == 'materia':
        calificacion = Calificaciones.objects.filter(materia__nombre__icontains=query)
    elif campo_busqueda == 'profesor':
        calificacion = Calificaciones.objects.filter(profesor__nombre__icontains=query)
    elif campo_busqueda == 'fecha':
        calificacion = Calificaciones.objects.filter(fecha=query)    
    elif campo_busqueda == 'nota':
        calificacion = Calificaciones.objects.filter(nota=query)    
    
    return render(request, 'calificaciones/index.html', {'calificaciones': calificacion, 'campo_busqueda': campo_busqueda, 'query': query})