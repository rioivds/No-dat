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
from django.db.models import Avg
from django.shortcuts import render
from django.db.models import Count
import json
def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'graficos/index.html',{ "alumnos": alumnos})


def index(request):
    cursos = Curso.objects.all()
    datos_grafico = []

    for curso in cursos:
        notas = Calificaciones.objects.filter(materia_id=4, curso=curso)  # Reemplaza 1 con el ID de la materia específica que deseas
        promedio = notas.aggregate(promedio=Count('nota'))['promedio']
        datos_grafico.append({
            'nombre_curso': curso.anio,
            'promedio': promedio,
        })

    datos_json = json.dumps(datos_grafico)

    return render(request, 'graficos/index.html', {'datos_grafico': datos_json})
