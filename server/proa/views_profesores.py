import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Profesor
from django.db import connection


TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html',{ "profesores": profesores})

def guardar_profesores(request):
    DNI = request.POST ["DNI"]
    nombre = request.POST ["nombre"]
    apellido = request.POST ["apellido"]
    email = request.POST ["email"]

    if Profesor.objects.filter(dni=DNI).exists():
        profesores = Profesor.objects.all()
        return render(request, 'profesores/index.html',{ "mensaje": "este alumno ya existe", "profesores": profesores})
    else:
        insert = Profesor(nombre = nombre, apellido = apellido, email = email, dni = DNI)
        insert.save()
        profesores = Profesor.objects.all()
        return render(request, 'profesores/index.html',{ "mensaje": "Se inserto con exito", "profesores": profesores})

def eliminar_profesores(request):
    id = request.GET["id"]
    delete = Profesor(id = id)
    delete.delete()
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html',{ "mensaje": "Se elimino el alumno con exito", "profesores": profesores})

def editar_profesores(request):
    DNI = request.GET["DNI"]
    profesores = Profesor.objects.all()
    profesores_editar = Profesor.objects.get(dni=DNI)
    print("editar",profesores_editar.nombre)
    return render(request, 'profesores/index.html',{ "mensaje": "", "profesores": profesores, "profesores_edit": profesores_editar})

def guardar_edit(request):
    id = request.GET["id"]
    DNI = request.POST ["DNI"]
    nombre = request.POST ["nombre"]
    apellido = request.POST ["apellido"]
    email = request.POST ["email"]

    profesores = Profesor.objects.all()
    Profesor.objects.filter(dni = DNI).update(dni = DNI, nombre = nombre, apellido = apellido, email = email)
    return render(request, 'profesores/index.html',{ "mensaje": "se edito correctamente", "profesores": profesores})