import datetime
from math import prod
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso, Materia, Profesor, Calificaciones
from django.db import connection


TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})


def guardar_materia(request):
    nombre = request.POST["materia"]  
    profesor = request.POST["profesor"]
    curso = request.POST["curso"]
    horas_catedra = request.POST["horas_catedra"]
    horario = request.POST["horario"]

    existe_materia = Materia.objects.filter(curso_id=curso, profesor_id=profesor, nombre=nombre).exists()  

    if not existe_materia:
        insert = Materia(
            profesor=Profesor.objects.get(dni=profesor),
            nombre=nombre,  
            curso=Curso.objects.get(id=curso),
            horas_catedra=horas_catedra,
            horario=horario
        )
        insert.save()

    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html', {"materias": materias, "cursos": cursos, "profesores": profesores})

def eliminar_materia(request):
    id = request.GET["id"]
    delete = Materia(id = id)
    delete.delete()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})

def editar_materia(request):
    id = request.GET["id"]
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    materias = Materia.objects.all()  # Agregar esta línea
    materias_editar = Materia.objects.get(id=id)
    print("editar",materias_editar.nombre)
    return render(request, 'materias/index.html', {"mensaje": "", "materias": materias, "materias_edit": materias_editar , "cursos": cursos, "profesores": profesores})


def guardar_edit(request):
    id = request.GET["id"]
    materia = request.POST["nombre"]
    profesor = request.POST["profesor"]
    curso = request.POST["curso"]
    Materia.objects.filter(id=id).update(profesor_id=profesor, nombre=materia, curso_id=curso)
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html', {"materias": materias, "cursos": cursos, "profesores": profesores})

