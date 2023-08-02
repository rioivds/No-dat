from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from proa.models import Curso, Materia, Calificaciones
from django.db import connection
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.shortcuts import render
from django.db.models import Count
import json
from django.http import JsonResponse
from urllib.parse import unquote
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Case, When, FloatField
from django.http import JsonResponse
from django.db.models import IntegerField, Q

def index(request):
    cursos = Curso.objects.all()
    todas_materias = Materia.objects.all()
    nombres_materias_unicas = set()

    for materia in todas_materias:
        nombres_materias_unicas.add(materia.nombre)

    datos_grafico = []

    for curso in cursos:
        todas_materias_curso = todas_materias.filter(curso=curso)

        for materia in todas_materias_curso:
            notas = Calificaciones.objects.filter(materia=materia, curso=curso)
            promedio = notas.aggregate(promedio=Avg('nota'))['promedio']

            if promedio is not None:
                datos_grafico.append({
                    'nombre_materia': materia.nombre,
                    'curso': curso.anio,
                    'promedio': promedio,
                })

    datos_json = json.dumps(datos_grafico)

    return render(request, 'graficos/index.html', {'datos_grafico': datos_json, "cursos": cursos, "materias": nombres_materias_unicas})

def materias_por_curso(request, curso_anio):
    materias = Materia.objects.filter(curso__anio=curso_anio).values_list('nombre', flat=True)
    return JsonResponse(list(materias), safe=False)

def grafico_materia(request, materia_nombre):
    materia_nombre_decoded = unquote(materia_nombre)  # Decodificar el nombre de la materia
    materias = Materia.objects.filter(nombre=materia_nombre_decoded)  # Filtrar por nombre de materia

    if materias.exists():  # Verificar si hay materias con ese nombre
        datos_grafico = []

        for materia in materias:
            cursos = Curso.objects.all()

            for curso in cursos:
                notas = Calificaciones.objects.filter(materia=materia, curso=curso)
                promedio = notas.aggregate(promedio=Avg('nota'))['promedio']

                # Verificar si hay promedio no nulo antes de agregar los datos al gráfico
                if promedio is not None:
                    datos_grafico.append({
                        'nombre_materia': materia.nombre,
                        'curso': curso.anio,  # Utilizar el año del curso
                        'promedio': promedio,
                    })

        return JsonResponse(datos_grafico, safe=False)

    else:
        # Si no se encontraron materias con ese nombre, retornar una respuesta vacía o un mensaje de error
        return JsonResponse([], safe=False)


