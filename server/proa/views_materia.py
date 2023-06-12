import datetime
from math import prod
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Cursos, Materias, Profesores
from django.db import connection


TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    materias = Materias.objects.all()
    profesores = Profesores.objects.all()
    cursos = Cursos.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})


def guardar_materia(request):
    materia = request.POST ["materia"]
    profesor = request.POST ["profesor"]
    curso = request.POST ["curso"]
    existe_materia = Materias.objects.filter(curso_id = curso, profesor_id = profesor, materia =  materia).exists()    
 
    if not existe_materia:
        insert = Materias(profesor = Profesores.objects.get(id = profesor), materia = materia, curso = Cursos.objects.get(id=curso))
        insert.save()
        
    materias = Materias.objects.all()
    profesores = Profesores.objects.all()
    cursos = Cursos.objects.all()
    return render(request, 'materias/index.html',{  "materias": materias, "cursos": cursos, "profesores": profesores})

def eliminar_materia(request):
    id = request.GET["id"]
    delete = Materias(id = id)
    delete.delete()
    materias = Materias.objects.all()
    profesores = Profesores.objects.all()
    cursos = Cursos.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})

def editar_materia(request):
    id = request.GET["id"]
    materias = Materias.objects.all()
    materias_editar = Materias.objects.get(id = id)
    materias = Materias.objects.all()
    profesores = Profesores.objects.all()
    cursos = Cursos.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})

def guardar_edit(request):
    id = request.GET["id"]
    materia = request.POST ["materia"]
    profesor = request.POST ["profesor"]
    curso = request.POST ["curso"]
    materias = Materias.objects.all()
    Materias.objects.filter(id = id).update(profesor = Profesores.objects.get(nombre = profesor), materia = materia, curso = Cursos.objects.get(id=curso))
    materias = Materias.objects.all()
    profesores = Profesores.objects.all()
    cursos = Cursos.objects.all()
    return render(request, 'materias/index.html',{ "materias": materias, "cursos": cursos, "profesores": profesores})
