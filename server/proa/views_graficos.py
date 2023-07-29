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
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count, Case, When, FloatField
from django.db.models.functions import Cast
def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'graficos/index.html',{ "alumnos": alumnos})


def index(request):
    cursos = Curso.objects.all()
    datos_grafico = []

    for curso in cursos:
        notas = Calificaciones.objects.filter(materia_id=201, curso=curso)  # Reemplaza 1 con el ID de la materia específica que deseas
        promedio = notas.aggregate(promedio=Avg('nota'))['promedio']
        datos_grafico.append({
            'nombre_curso': curso.anio,
            'promedio': promedio,
        })
    print(promedio)
    datos_json = json.dumps(datos_grafico)

    return render(request, 'graficos/index.html', {'datos_grafico': datos_json})

def grafico_torta(request):
    queryset = Calificaciones.objects.filter(materia_id=201)  # Filtrar por el ID de la materia 'Programacion IV'

    # Obtener el total de alumnos por curso
    cursos = queryset.values('curso__anio').annotate(total_alumnos=Count('alumno', distinct=True))

    # Obtener la cantidad de alumnos aprobados en cada rango de nota
    aprobados = queryset.values('curso__anio') \
        .annotate(
            aprobados_mas_de_nueve=Count(Case(When(nota__gt=9, then=1), output_field=FloatField())),
            aprobados_entre_siete_y_nueve=Count(Case(When(nota__range=[7, 9], then=1), output_field=FloatField())),
            aprobados_entre_cuatro_y_seis=Count(Case(When(nota__range=[4, 6], then=1), output_field=FloatField())),
            desaprobados_entre_cero_y_tres=Count(Case(When(nota__range=[0, 3], then=1), output_field=FloatField()))
        )

    # Calcular el porcentaje de aprobados en cada rango
    for datos in aprobados:
        total_alumnos = cursos.get(curso__anio=datos['curso__anio'])['total_alumnos']
        datos['aprobados_mas_de_nueve'] = datos['aprobados_mas_de_nueve'] / total_alumnos * 100
        datos['aprobados_entre_siete_y_nueve'] = datos['aprobados_entre_siete_y_nueve'] / total_alumnos * 100
        datos['aprobados_entre_cuatro_y_seis'] = datos['aprobados_entre_cuatro_y_seis'] / total_alumnos * 100
        datos['desaprobados_entre_cero_y_tres'] = datos['desaprobados_entre_cero_y_tres'] / total_alumnos * 100

    # Convertir el resultado a un objeto JSON válido
    datos_json = list(aprobados)

    return render(request, 'graficos/grafico_torta.html', {'datos_grafico_torta': datos_json})