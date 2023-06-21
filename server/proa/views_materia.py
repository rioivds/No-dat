import datetime
from math import prod
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso, Materia, Profesor
from django.db import connection


TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})


def guardar_materia(request):
    materia = request.POST ["materia"]
    profesor = request.POST ["profesor"]
    curso = request.POST ["curso"]
    existe_materia = Materia.objects.filter(curso_id = curso, profesor_id = profesor, materia =  materia).exists()    
 
    if not existe_materia:
        insert = Materia(profesor = Profesor.objects.get(id = profesor), materia = materia, curso = Curso.objects.get(id=curso))
        insert.save()
        
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{  "materias": materias, "cursos": cursos, "profesores": profesores})

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
    materias = Materia.objects.all()
    materias_editar = Materia.objects.get(id = id)
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})

def guardar_edit(request):
    id = request.GET["id"]
    materia = request.POST ["materia"]
    profesor = request.POST ["profesor"]
    curso = request.POST ["curso"]
    materias = Materia.objects.all()
    Materia.objects.filter(id = id).update(profesor = Profesor.objects.get(nombre = profesor), materia = materia, curso = Curso.objects.get(id=curso))
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})
