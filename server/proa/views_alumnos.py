from django.shortcuts import render
from proa.models import Alumno, Curso
from django.http import HttpResponse
import openpyxl
from .importaciones import importar_alumnos, importar_alumnos_pdf
from .common import Common

def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html',{ 'alumnos': alumnos})

def guardar_alumnos(request):
    alumnos = Alumno.objects.all()
    DNI = request.POST['DNI']  
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']

    email = request.POST['email']
    if Common.email_check(email):
        return render(request, 'alumnos/index.html', {'mensaje': 'Por favor, asegurese que el email sea institucional (@escuelasproa.edu.ar)', 'alumnos': alumnos})

    fecha_nacimiento = request.POST['fecha_nacimiento']
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
    dni = request.GET['DNI']
    alumno = Alumno.objects.get(dni=dni)
    alumno.delete()

    alumnos = Alumno.objects.all()
    return render(request, 'alumnos/index.html', {'mensaje': 'Se eliminó el alumno con éxito', 'alumnos': alumnos})

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
    repitio = request.POST.get('repitio') == 'on'
    curso = Curso.objects.get(id=request.POST['curso'])

    Alumno.objects.filter(dni=DNI).update(nombre=nombre, apellido=apellido, email=email, dni=DNI, curso=curso, fecha_nacimiento=fecha_nacimiento, repitio=repitio)
    alumnos = Alumno.objects.all()

    return render(request, 'alumnos/index.html', {'mensaje': 'Se editó correctamente', 'alumnos': alumnos})

def importar_alumnos_view(request):
    if request.method == 'GET':
        return render(request, 'alumnos/importar_alumnos.html', {'mensajes': None})

    archivo = request.FILES['archivo_excel']
    extension = str(archivo).split('.')[-1]

    logs = None
    if extension == 'pdf':
        logs = importar_alumnos_pdf(archivo)
    elif extension == 'xlsx':
        importar_alumnos(archivo)

    return render(request, 'alumnos/importar_alumnos.html', {'mensajes': logs})

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
