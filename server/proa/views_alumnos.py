import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso
from django.db import connection
from django.shortcuts import get_object_or_404

TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html',{ "alumnos": alumnos})


def guardar_alumnos(request):
    DNI = request.POST["DNI"]
    nombre = request.POST["nombre"]
    apellido = request.POST["apellido"]
    email = request.POST["email"]
    fecha_nacimiento = request.POST["fecha_nacimiento"]
    repitio = request.POST.get("repitio") == "on"  # Conversión a True si está marcado
    curso = request.POST["curso"]
    if Alumno.objects.filter(dni=DNI).exists():
        alumnos = Alumno.objects.all()
        return render(request, 'alumnos/index.html',{ "mensaje": "este alumno ya existe", "alumno": alumnos})
    else:
        insert = Alumno(nombre=nombre, apellido=apellido, email=email, dni=DNI, curso=Curso.objects.get(id=curso), fecha_nacimiento=fecha_nacimiento, repitio=repitio)
        insert.save()
        alumnos = Alumno.objects.all()
        return render(request, 'alumnos/index.html', {"mensaje": "Se insertó con éxito", "alumnos": alumnos})

def eliminar_alumno(request):
    DNI = request.GET["DNI"]
    delete = get_object_or_404(Alumno, dni=DNI)
    delete.delete()
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html',{ "mensaje": "Se elimino el alumno con exito", "alumnos": alumnos})

def editar_alumno(request):
    DNI = request.GET["DNI"]
    alumnos = Alumno.objects.all()
    alumnos_editar = Alumno.objects.get(dni=DNI)
    print("editar",alumnos_editar.nombre)
    return render(request, 'alumnos/index.html', {"mensaje": "", "alumnos": alumnos, "alumnos_edit": alumnos_editar})

def guardar_edit(request):
    
    DNI = request.POST["DNI"]
    nombre = request.POST["nombre"]
    apellido = request.POST["apellido"]
    email = request.POST["email"]
    fecha_nacimiento = request.POST["fecha_nacimiento"]
    repitio = request.POST.get("repitio") 
    curso = request.POST["curso"]

    alumnos = Alumno.objects.all()
    Alumno.objects.filter(dni = DNI).update(nombre=nombre, apellido=apellido, email=email, dni=DNI, curso=Curso.objects.get(id=curso), fecha_nacimiento=fecha_nacimiento, repitio=repitio)
    return render(request, 'alumnos/index.html', {"mensaje": "se editó correctamente", "alumnos": alumnos})


def curso(request):
    año = request.GET["curso"]
    print (año)
    if año == "1":
        alumnos = Alumno.objects.filter(curso=año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    elif año == "2":
        alumnos = Alumno.objects.filter(curso=año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    elif año == "3":
        alumnos = Alumno.objects.filter(curso = año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    elif año == "4":
        alumnos = Alumno.objects.filter(curso = año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    elif año == "5":
        alumnos = Alumno.objects.filter(curso = año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    elif año == "6":
        alumnos = Alumno.objects.filter(curso = año)
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
    else:
        alumnos = Alumno.objects.all()
        return render(request, 'alumnos/index.html',{ "alumnos": alumnos})