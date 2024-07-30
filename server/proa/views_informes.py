from django.shortcuts import render
from proa.models import Alumno, Materia, Calificaciones

def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'informes/index.html', {'alumnos': alumnos})

def generar_informe(request):
    lista_notas = []
    DNI = request.GET['DNI'] 
    alumno = Alumno.objects.get(dni=DNI)

    materias = Materia.objects.filter(curso=alumno.curso)
    for materia in materias:
        calificaciones = Calificaciones.objects.filter(alumno=alumno, materia=materia, curso=alumno.curso)
        notas = []

        for calificacion in calificaciones:
            notas.append(int(calificacion.nota))

        while len(notas) < 3:
            notas.append('')

        notas.insert(0, materia.nombre)
        lista_notas.append(notas)

    return render(request, 'informes/etapa_1.html', {
        'alumno': alumno,
        'curso': alumno.curso.anio,
        'materias': materias,
        'lista_notas': lista_notas,
        'i': 0
    })
