from django.shortcuts import render, redirect
from proa.models import Curso, Materia, Profesor
from .importaciones import importar_materias
import openpyxl

def index(request):
    materias = Materia.objects.all()
    for materia in materias:
        print(materia.profesor)

    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'materias/index.html', {'materias': materias, 'cursos': cursos, 'profesores': profesores})

def guardar_materia(request):
    nombre = request.POST['materia']  
    profesor = request.POST['profesor']
    curso = request.POST['curso']
    horas_catedra = request.POST['horas-catedra']

    existe_materia = Materia.objects.filter(curso_id=curso, profesor_id=profesor, nombre=nombre).exists()
    if not existe_materia:
        insert = Materia(
            profesor=Profesor.objects.get(dni=profesor),
            nombre=nombre,  
            curso=Curso.objects.get(id=curso),
            horas_catedra=horas_catedra
        )
        insert.save()

    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'materias/index.html', {'materias': materias, 'cursos': cursos, 'profesores': profesores})

def eliminar_materia(request):
    id = request.GET['id']
    materia = Materia(id=id)
    materia.delete()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'materias/index.html', {'materias': materias, 'cursos': cursos, 'profesores': profesores})

def editar_materia(request):
    id = request.GET['id']
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    materias = Materia.objects.all()
    materias_editar = Materia.objects.get(id=id)

    return render(request, 'materias/index.html', {
        'mensaje': '',
        'materias': materias,
        'materias_edit': materias_editar,
        'cursos': cursos,
        'profesores': profesores
    })

def guardar_edit(request):
    id = request.GET['id']
    materia = request.POST['nombre']
    profesor = request.POST['profesor']
    curso = request.POST['curso']
    horas = request.POST['horas-catedra']
    Materia.objects.filter(id=id).update(profesor_id=profesor, nombre=materia, curso_id=curso, horas_catedra=horas)

    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()

    return render(request, 'materias/index.html', {'materias': materias, 'cursos': cursos, 'profesores': profesores})

def importar_materias_view(request):
    # mensaje = ''  # Inicializar la variable mensaje
    # if request.method == 'POST' and request.FILES.get('archivo_excel'):
    #     archivo_excel = request.FILES['archivo_excel']
    #     try:
    #         workbook = openpyxl.load_workbook(archivo_excel)
    #         sheet = workbook.active

    #         for row in sheet.iter_rows(min_row=2, values_only=True):
    #             nombre = row[0]
    #             horas_catedra = row[1]
    #             horario = row[2]
    #             profesor_nombre = row[3]  # Suponiendo que en la columna 4 del Excel tienes el nombre del profesor
    #             curso_anio = row[4]  # Suponiendo que en la columna 5 del Excel tienes el año del curso

    #             # Obtener o crear el profesor
    #             profesor, _ = Profesor.objects.get_or_create(nombre=profesor_nombre)

    #             # Obtener el curso
    #             curso, _ = Curso.objects.get_or_create(anio=curso_anio)

    #             # Crear la materia
    #             materia = Materia(nombre=nombre, horas_catedra=horas_catedra, horario=horario, profesor=profesor, curso=curso)
    #             materia.save()

    #         mensaje = 'Materias importadas correctamente.'
    #     except Exception as e:
    #         mensaje = f'Error al importar las materias: {e}'

    if request.method == 'GET':
        return render(request, 'materias/importar_materias.html', {'mensaje': ''})

    archivo = request.FILES['archivo_excel']
    importar_materias(archivo)

    return redirect('/materias')
