import datetime
from django.shortcuts import render
from proa.models import Alumno, Curso
from django.shortcuts import get_object_or_404
from datetime import datetime
from .forms import ImportarAlumnosForm
from django.http import HttpResponse, HttpResponseRedirect
import openpyxl
from .importaciones import importar_alumnos
from .common import Common

def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html',{ 'alumnos': alumnos})

def guardar_alumnos(request):
    alumnos = Alumno.objects.all()
    DNI = request.POST['DNI']  
    nombre = request.POST['nombre']

    if not nombre.isalpha():
        return render(request, 'alumnos/index.html', {'mensaje': 'Por favor, ingrese bien el nombre', 'alumnos': alumnos})

    apellido = request.POST['apellido']
    if not apellido.isalpha():
        return render(request, 'alumnos/index.html', {'mensaje': 'Por favor, ingrese bien el apellido', 'alumnos': alumnos})

    email = request.POST['email']
    if Common.email_check(email):
        return render(request, 'alumnos/index.html', {'mensaje': 'Por favor, ecriba bien el email o asegurese que sea intitucional (@escuelasproa.edu.ar)', 'alumnos': alumnos})

    fecha_nacimiento = datetime.strptime(request.POST['fecha_nacimiento'], '%Y-%m-%d').strftime('%Y-%m-%d')
    repitio = request.POST.get('repitio') == 'on'  # Conversión a True si está marcado
    curso = request.POST['curso']

    if Alumno.objects.filter(dni=DNI).exists():
        return render(request, 'alumnos/index.html', {'mensaje': 'Este alumno ya existe', 'alumnos': alumnos})

    insert = Alumno(
        nombre=nombre,
        apellido=apellido,
        email=email,
        dni=DNI,
        curso=Curso.objects.get(id=curso),
        fecha_nacimiento=fecha_nacimiento,
        repitio=repitio
    )
    insert.save()

    return render(request, 'alumnos/index.html', {'mensaje': 'Se insertó con éxito', 'alumnos': alumnos})

def eliminar_alumno(request):
    DNI = request.GET['DNI']
    delete = get_object_or_404(Alumno, dni=DNI)
    delete.delete()
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html',{ 'mensaje': 'Se eliminó el alumno con éxito', 'alumnos': alumnos})

def editar_alumno(request):
    DNI = request.GET['DNI']
    alumnos = Alumno.objects.all()
    alumnos_editar = Alumno.objects.get(dni=DNI)
    return render(request, 'alumnos/index.html', {'mensaje': '', 'alumnos': alumnos, 'alumnos_edit': alumnos_editar})

def guardar_edit(request):
    DNI = request.POST['DNI']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    email = request.POST['email']
    fecha_nacimiento = Common.parse_fecha(None if request.POST['fecha_nacimiento'] == 'None' else request.POST['fecha_nacimiento'])
    repitio = request.POST.get('repitio')
    curso = Curso.objects.get(id=request.POST['curso'])

    alumnos = Alumno.objects.all()
    Alumno.objects.filter(dni=DNI).update(nombre=nombre, apellido=apellido, email=email, dni=DNI, curso=curso, fecha_nacimiento=fecha_nacimiento, repitio=repitio)

    return render(request, 'alumnos/index.html', {'mensaje': 'Se editó correctamente', 'alumnos': alumnos})

def importar_alumnos_view(request):
    if request.method == 'POST':
        form = ImportarAlumnosForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES['archivo_excel']
            importar_alumnos(archivo_excel)
            return HttpResponseRedirect('/alumnos')  # Redirigir a la página principal después de la importación
    else:
        form = ImportarAlumnosForm()
    return render(request, 'alumnos/importar_alumnos.html', {'form': form})

def exportar_alumnos(request):
    alumnos = Alumno.objects.all()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Alumnos'

    # Encabezados de las columnas
    sheet['A1'] = 'DNI'
    sheet['B1'] = 'Nombre'
    sheet['C1'] = 'Apellido'
    sheet['D1'] = 'Fecha de Nacimiento'
    sheet['E1'] = 'Email'
    sheet['F1'] = 'Repitio'
    sheet['G1'] = 'Año'

    # Llenar el contenido con los datos de los alumnos
    for index, alumno in enumerate(alumnos, start=2):
        sheet[f'A{index}'] = alumno.dni
        sheet[f'B{index}'] = alumno.nombre
        sheet[f'C{index}'] = alumno.apellido
        sheet[f'D{index}'] = alumno.fecha_nacimiento.strftime('%Y-%m-%d')
        sheet[f'E{index}'] = alumno.email
        sheet[f'F{index}'] = 'Si' if alumno.repitio else 'No'
        sheet[f'G{index}'] = alumno.curso.anio

    # Agregar estilo a los encabezados
    header_font = openpyxl.styles.Font(bold=True)
    for cell in sheet['1']:
        cell.font = header_font

    # Generar la respuesta con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=alumnos.xlsx'
    workbook.save(response)

    return response
