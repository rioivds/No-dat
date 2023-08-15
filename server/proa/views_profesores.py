import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Profesor, Usuario
from django.db import connection
from django.shortcuts import get_object_or_404
import openpyxl
from proa.verificador import role_required

TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')

@role_required(allowed_roles=[2,3])
def index(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html',{ "profesores": profesores})

@role_required(allowed_roles=[2,3])
def guardar_profesores(request):
    DNI = request.POST ["DNI"]
    nombre = request.POST ["nombre"]
    apellido = request.POST ["apellido"]
    email = request.POST ["email"]
    telefono= request.POST["telefono"]

    if Profesor.objects.filter(dni=DNI).exists():
        profesores = Profesor.objects.all()
        return render(request, 'profesores/index.html',{ "mensaje": "este profesor ya existe", "profesores": profesores})
    elif Usuario.objects.filter(email = email).exists():
        return render(request, 'alumnos/index.html', {"mensaje": "Ya existe un alumno con ese email", "alumnos": profesores})
    else:
        insert = Usuario(
            email = email,
            contrasenia = DNI,
            rol = 1
        )
        insert.save()
        insert = Profesor(
            nombre=nombre,
            apellido=apellido,
            email=email,
            dni=DNI,
            telefono = telefono,
            usuario = Usuario.objects.get(email = email, contrasenia = DNI)
        )
        insert.save()
        profesores = Profesor.objects.all()
        return render(request, 'profesores/index.html',{ "mensaje": "Se inserto con exito", "profesores": profesores})

@role_required(allowed_roles=[2,3])
def eliminar_profesores(request):
    DNI = request.GET["DNI"]
    profesor = get_object_or_404(Profesor, dni=DNI)
    profesor.delete()
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html', {"mensaje": "Se eliminó el Profesor con éxito", "profesores": profesores})

@role_required(allowed_roles=[2,3])
def editar_profesores(request):
    DNI = request.GET["DNI"]
    profesores = Profesor.objects.all()
    profesores_editar = Profesor.objects.get(dni=DNI)
    print("editar",profesores_editar.nombre)
    return render(request, 'profesores/index.html',{ "mensaje": "", "profesores": profesores, "profesores_edit": profesores_editar})

@role_required(allowed_roles=[2,3])
def guardar_edit(request):
    id = request.GET["id"]
    DNI = request.POST ["DNI"]
    nombre = request.POST ["nombre"]
    apellido = request.POST ["apellido"]
    email = request.POST ["email"]
    telefono=request.POST["telefono"]

    profesores = Profesor.objects.all()
    Profesor.objects.filter(dni = DNI).update(dni = DNI, nombre = nombre, apellido = apellido, email = email, telefono=telefono)
    return render(request, 'profesores/index.html',{ "mensaje": "se edito correctamente", "profesores": profesores})

@role_required(allowed_roles=[2,3])
def exportar_profesores(request):
    profesores = Profesor.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'registro_profesores-noDat'

    # Encabezados de las columnas
    sheet['A1'] = 'nombre'
    sheet['B1'] = 'apellido'
    sheet['C1'] = 'email'
    sheet['D1'] = 'dni'
    sheet['E1'] = 'telefono'

    # Llenar el contenido con los datos de los alumnos
    for index, profesor in enumerate(profesores, start=2):
        sheet[f'A{index}'] = profesor.nombre
        sheet[f'B{index}'] = profesor.apellido
        sheet[f'C{index}'] = profesor.email
        sheet[f'D{index}'] = profesor.dni
        sheet[f'E{index}'] = profesor.telefono

    # Agregar estilo a los encabezados
    header_font = openpyxl.styles.Font(bold=True)
    for cell in sheet['1']:
        cell.font = header_font

    # Generar la respuesta con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=registro_profesores-noDat'
    workbook.save(response)
    return response

@role_required(allowed_roles=[2,3])
def filtro_profesores(request):
    query = request.GET.get('query', '')
    campo_busqueda = request.GET.get('campo', 'nombre')  # Por defecto, buscar por nombre

    if campo_busqueda == 'dni':
        profesores = Profesor.objects.filter(dni__icontains=query)
    elif campo_busqueda == 'nombre':
        profesores = Profesor.objects.filter(nombre__icontains=query)
    elif campo_busqueda == 'apellido':
        profesores = Profesor.objects.filter(apellido__icontains=query)
    elif campo_busqueda == 'email':
        profesores = Profesor.objects.filter(email__icontains=query)
    elif campo_busqueda == 'telefono':
        profesores = Profesor.objects.filter(telefono=query)
    
    return render(request, 'profesores/index.html', {'profesores': profesores, 'campo_busqueda': campo_busqueda, 'query': query})
   
