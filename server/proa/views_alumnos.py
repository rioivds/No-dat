# import datetime
# from xml.dom.minidom import Document
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import F
# from django.db.models import Q
# from proa.models import Alumno, Curso
# from django.db import connection


# TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


# def index(request):
#     alumnos = Alumno.objects.all()
#     return render(request, 'alumnos/index.html',{ "alumnos": alumnos})


# def guardar_alumnos(request):
#     DNI = request.POST ["DNI"]
#     nombre = request.POST ["nombre"]
#     apellido = request.POST ["apellido"]
#     email = request.POST ["email"]
#     curso = request.POST ["curso"]

#     insert = Alumno(nombre = nombre, apellido = apellido, email = email, documento = DNI, curso = Curso.objects.get(id=curso))
#     insert.save()
#     alumnos = Alumno.objects.all()
#     return render(request, 'alumnos/index.html',{ "mensaje": "Se inserto con exito", "alumnos": alumnos})

# def eliminar_alumno(request):
#     id = request.GET["id"]
#     delete = Alumno(id = id)
#     delete.delete()
#     alumnos = Alumno.objects.all()
#     return render(request, 'alumnos/index.html',{ "mensaje": "Se elimino el alumno con exito", "alumnos": alumnos})

# def editar_alumno(request):
#     DNI = request.GET["DNI"]
#     alumnos = Alumno.objects.all()
#     alumnos_editar = Alumno.objects.get(documento=DNI)
#     print("editar",alumnos_editar.nombre)
#     return render(request, 'alumnos/index.html',{ "mensaje": "", "alumnos": alumnos, "alumnos_edit": alumnos_editar})

# def guardar_edit(request):
#     id = request.GET["id"]
#     DNI = request.POST ["DNI"]
#     nombre = request.POST ["nombre"]
#     apellido = request.POST ["apellido"]
#     email = request.POST ["email"]
#     curso = request.POST ["curso"]
#     alumnos = Alumno.objects.all()
#     Alumno.objects.filter(id = id).update(documento = DNI, nombre = nombre, apellido = apellido, email = email, curso = Curso.objects.get(id=curso))
#     return render(request, 'alumnos/index.html',{ "mensaje": "se edito correctamente", "alumnos": alumnos})

# def curso(request):
#     año = request.GET["curso"]
#     print (año)
#     if año == "1":
#         print("si")
#         alumnos = Alumno.objects.filter(curso=año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     elif año == "2":
#         alumnos = Alumno.objects.filter(curso=año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     elif año == "3":
#         alumnos = Alumno.objects.filter(curso = año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     elif año == "4":
#         alumnos = Alumno.objects.filter(curso = año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     elif año == "5":
#         alumnos = Alumno.objects.filter(curso = año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     elif año == "6":
#         alumnos = Alumno.objects.filter(curso = año)
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})
#     else:
#         alumnos = Alumno.objects.all()
#         return render(request, 'alumnos/index.html',{ "alumnos": alumnos})