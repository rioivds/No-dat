from django.shortcuts import render
from django.db.models import Count, Case, When, FloatField
from django.db.models.functions import Cast
from .models import Alumno, Calificaciones
def grafico_torta(request):
    datos_grafico = Calificaciones.objects.filter(curso__anio=6, materia__nombre="Programacion IV") \
        .values('curso__nombre') \
        .annotate(
            aprobados_mas_de_nueve=Count(Case(When(nota__gt=9, then=1), output_field=FloatField())),
            aprobados_entre_siete_y_nueve=Count(Case(When(nota__range=(7, 9), then=1), output_field=FloatField())),
            aprobados_entre_cuatro_y_seis=Count(Case(When(nota__range=(4, 6), then=1), output_field=FloatField())),
            desaprobados_entre_cero_y_tres=Count(Case(When(nota__range=(0, 3), then=1), output_field=FloatField())),
        )

    # Calcular porcentajes para cada grupo
    total_alumnos = Alumno.objects.filter(curso__anio=6).count()
    for dato in datos_grafico:
        dato['aprobados_mas_de_nueve'] = round((dato['aprobados_mas_de_nueve'] / total_alumnos) * 100, 2)
        dato['aprobados_entre_siete_y_nueve'] = round((dato['aprobados_entre_siete_y_nueve'] / total_alumnos) * 100, 2)
        dato['aprobados_entre_cuatro_y_seis'] = round((dato['aprobados_entre_cuatro_y_seis'] / total_alumnos) * 100, 2)
        dato['desaprobados_entre_cero_y_tres'] = round((dato['desaprobados_entre_cero_y_tres'] / total_alumnos) * 100, 2)

    return render(request, 'graficos/grafico_torta.html', {'datos_grafico': datos_grafico})
