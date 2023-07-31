import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso, Materia, Calificaciones
from django.db import connection
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Case, When, Count, IntegerField, Q


def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'informes/index.html',{ "alumnos": alumnos})

def generar_informe(request):
    lista_notas = []
    notass = []
    DNI = request.GET["DNI"] 
    alumno = Alumno.objects.get(dni=DNI)
    materias = Materia.objects.filter(curso = alumno.curso)
    for materia in materias:
        notas = Calificaciones.objects.filter(alumno = alumno, materia = materia, curso = alumno.curso)
        print(notas)
        notass= []
        
        for aux in notas:
            notass.append(int(aux.nota))

        while len(notass)  < 3:
            notass.append("")
            
        notass.insert(0, materia.nombre)
        lista_notas.append(notass)
    return render(request, 'informes/etapa_1.html',{ "alumno": alumno, "curso": alumno.curso.anio, "materias": materias, "lista_notas": lista_notas, "i": 0})
