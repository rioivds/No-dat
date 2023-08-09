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

    nombres_materias_unicas=["ARTES VISUALES",                           
                             "BIOLOGÍA",
                             "CIUDADANÍA Y PARTICIPACIÓN",
                             "CIUDADANÍA Y POLÍTICA",
                             "CLUB DE ARTE",
                             "CLUB DE CIENCIAS",
                             "CLUB DE DEPORTES",
                             "DESARROLLO DE APLICACIONES MÓVILES",
                             "DISEÑO DE INTERFACE",
                             "EDUCACIÓN FISICA",
                             "ESTRUCTURA Y ALMACENAMIENTO DE DATOS",
                             "ÉTICA Y LEGISLACIÓN",
                             "FÍSICA",
                             "FILOSOFÍA",
                             "FPVT",
                             "GEOGRAFÍA",
                             "HISTORIA",
                             "INGLÉS",
                             "LENGUA Y LITERATURA",
                             "MATEMÁTICA",
                             "MÚSICA",
                             "PROGRAMACIÓN Y ENTORNOS DIGITALES",
                             "PSICOLOGÍA",
                             "QUÍMICA",
                             "ROBÓTICA",
                             "SISTEMAS OPERATIVOS",
                             "TALLER DE INGLES APLICADO",
                             "TEATRO",
                             "TESTING"
                            ]

    datos_grafico = []

    for curso in cursos:
        todas_materias_curso = todas_materias.filter(curso=curso)

        for materia in todas_materias_curso:
            notas = Calificaciones.objects.filter(materia=materia,curso=curso)
            promedio = notas.aggregate(promedio=Avg('nota'))['promedio']

            if promedio is not None:
                datos_grafico.append({
                    'nombre_materia': materia.nombre,
                    'curso': curso.anio,
                    'promedio': promedio,
                })

    datos_json = json.dumps(datos_grafico)

    return render(request, 'graficos/index.html', {'datos_grafico': datos_json, "cursos": cursos, "materias":nombres_materias_unicas })



def materias_por_curso(request, curso_anio):
    materias = Materia.objects.filter(curso__anio=curso_anio).values_list('nombre', flat=True)
    return JsonResponse(list(materias), safe=False)


def grafico_materia(request, materia_nombre):
    materia_nombre_decoded = unquote(materia_nombre) # Decodificar el nombre de la materia


    # Si la materia es INGLÉS, se filtra por el nombre exacto, asi no entra en conflicto con INGLÉS APLICADO
    if materia_nombre_decoded == "INGLÉS":
        materias = Materia.objects.filter(nombre=materia_nombre_decoded)

    # Si la materia es PROGRAMACIÓN Y ENTORNOS DIGITALES cambiar su nombre por -> PROGRAMACIÓN, para filtrar todas las materias que la contengan en su nombre 
    elif materia_nombre_decoded == "PROGRAMACIÓN Y ENTORNOS DIGITALES": 
        materias=Materia.objects.filter(Q(nombre__icontains="PROGRAMACIÓN")|Q(nombre__icontains="ENTORNOS DIGITALES"))
        
    # Si no, se filtra por las materias que la contengan en su nombre
    else:
        materias = Materia.objects.filter(nombre__icontains=materia_nombre_decoded)  


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