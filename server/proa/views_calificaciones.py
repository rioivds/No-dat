# Cambios

import datetime
from django.shortcuts import render
from proa.models import Alumno, Curso, Calificaciones,Profesor,Materia
from django.shortcuts import get_object_or_404
from datetime import datetime
import openpyxl

def index(request):
    calificaciones = Calificaciones.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    materias = Materia.objects.all()
    alumnos = Alumno.objects.all()

    return render(request, 'calificaciones/index.html', {
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos':alumnos
    })

def parse_fecha(fecha_str):
    meses = {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12'
    }

    partes = fecha_str.split(' ')
    dia = partes[0]
    mes = meses[partes[2]]
    anio = partes[4]

    return f'{anio}-{mes}-{dia}'

def guardar_calificaciones(request):
    alumno=request.POST['alumno']
    curso = request.POST['curso']
    materia=request.POST['materia']
    profesor=request.POST['profesor']
    fecha = request.POST['fecha']
    fecha_nota_str = datetime.strptime(fecha, '%m/%d/%Y').strftime('%Y-%m-%d')
    nota = request.POST['nota']
    final = request.POST.get('final') == 'on'  # Conversión a True si está marcado

    insert = Calificaciones(
        alumno=Alumno.objects.get(dni=alumno),
        curso=Curso.objects.get(id=curso),
        materia=Materia.objects.get(id=materia),
        profesor=Profesor.objects.get(dni=profesor),
        fecha=fecha_nota_str,
        nota=nota,
        final=final
    )
    insert.save()

    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()

    return render(request, 'calificaciones/index.html', {
        'mensaje': 'Se insertó calificación con éxito',
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def eliminar_calificaciones(request):
    id = request.GET['id']
    calificacion = get_object_or_404(Calificaciones, id=id)
    calificacion.delete()

    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()

    return render(request, 'calificaciones/index.html', {
        'mensaje': 'Se elimino calificación con éxito',
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def editar_calificaciones(request):
    id = request.GET['id']
    calificaciones = Calificaciones.objects.all()
    calificaciones_editar = Calificaciones.objects.get(id=id)
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()

    return render(request, 'calificaciones/index.html', {
        'mensaje': '',
        'calificaciones_edit': calificaciones_editar,
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def guardar_edit(request):
    id = request.GET['id']
    alumno = request.POST['alumno']
    curso = request.POST['curso']
    materia = request.POST['materia']
    profesor = request.POST['profesor']
    fecha = request.POST['fecha']
    fecha_nota_str = parse_fecha(fecha)
    nota = float(request.POST['nota'].replace(',', '.'))
    final = request.POST.get('final', False) == 'True'
    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    Calificaciones.objects.filter(id=id).update(alumno=Alumno.objects.get(dni=alumno), curso=Curso.objects.get(id=curso), materia=Materia.objects.get(id=materia), profesor=Profesor.objects.get(dni=profesor),  fecha=fecha_nota_str, nota=nota, final=final)

    return render(request, 'calificaciones/index.html', {
        'mensaje': 'Se editó correctamente',
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def importar_calificaciones(request):
    mensaje = ''  # Asignar un valor predeterminado o una cadena vacía

    if request.method == 'POST' and request.FILES.get('archivo_excel'):
        archivo_excel = request.FILES['archivo_excel']
        try:
            workbook = openpyxl.load_workbook(archivo_excel)
            sheet = workbook.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                alumno_dni = row[0]  # Suponiendo que en la columna 1 del Excel tienes el DNI del alumno
                curso_id = row[1]  # Suponiendo que en la columna 2 del Excel tienes el ID del curso
                materia_id = row[2]  # Suponiendo que en la columna 3 del Excel tienes el ID de la materia
                profesor_id = row[3]  # Suponiendo que en la columna 4 del Excel tienes el ID del profesor
                fecha = row[4]  # Suponiendo que en la columna 5 del Excel tienes la fecha de la calificación
                nota = row[5]  # Suponiendo que en la columna 6 del Excel tienes la nota de la calificación
                final = row[6]  # Suponiendo que en la columna 7 del Excel tienes un valor booleano para indicar si es final

                # Obtener o crear el alumno
                alumno, _ = Alumno.objects.get_or_create(dni=alumno_dni)

                # Obtener o crear la materia
                materia, _ = Materia.objects.get_or_create(id=materia_id)

                # Obtener o crear el profesor
                profesor, _ = Profesor.objects.get_or_create(dni=profesor_id)

                # Obtener o crear el curso
                curso, _ = Curso.objects.get_or_create(id=curso_id)

                # Crear la calificación
                calificacion = Calificaciones(alumno=alumno, curso=curso, materia=materia, profesor=profesor, fecha=fecha, nota=nota, final=final)
                calificacion.save()

            mensaje = 'Calificaciones importadas correctamente.'
        except Exception as e:
            mensaje = f'Error al importar las calificaciones: {e}'

    return render(request, 'calificaciones/importar_calificaciones.html', {'mensaje': mensaje})
