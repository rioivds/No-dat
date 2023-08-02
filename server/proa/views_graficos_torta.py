from django.shortcuts import render
from proa.models import Curso, Materia, Calificaciones
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

def grafico_torta(request):
    cursos = Curso.objects.all()
    selected_curso = request.GET.get('curso', None)
    materias = []
    if selected_curso:
        materias = Materia.objects.filter(curso_id=selected_curso)
    return render(request, 'graficos/grafico_torta.html', {'cursos': cursos, 'materias': materias})


def grafico_torta_materia(request, materia_id):
    calificaciones = Calificaciones.objects.filter(materia_id=materia_id)
    total_calificaciones = calificaciones.count()
    print("calificaciones",calificaciones)
    print("materia",materia_id)
    print("conteo",total_calificaciones)
    porcentajes = {'1_3': 0, '4_6': 0, '7_8': 0, '9_10': 0,}
    if total_calificaciones > 0:
        porcentajes['1_3'] = calificaciones.filter(nota__range=(1, 3)).count()
        porcentajes['4_6'] = calificaciones.filter(nota__range=(4, 6)).count() 
        porcentajes['7_8'] = calificaciones.filter(nota__range=(7, 8)).count() 
        porcentajes['9_10'] = calificaciones.filter(nota__range=(9, 10)).count() 

    # Convierte porcentajes a un diccionario antes de pasarlo a JsonResponse
    porcentajes_dict = {
        '1_3': porcentajes['1_3'],
        '4_6': porcentajes['4_6'],
        '7_8': porcentajes['7_8'],
        '9_10': porcentajes['9_10'],
        'total_calificaciones': total_calificaciones,
    }
    print (porcentajes_dict)
    return JsonResponse(porcentajes_dict, safe=False)