# Agrega esto al inicio de tu views.py
import openpyxl
from django.http import HttpResponse
from django.db.models import F

# Agrega esta nueva vista después de las demás vistas existentes
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
