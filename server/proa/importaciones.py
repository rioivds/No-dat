import pandas
import PyPDF2
from datetime import datetime
from .models import Alumno, Profesor, Materia, Calificaciones, Curso

def importar_calificaciones(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        nota = float(row['nota'])
        final = row['final'].lower() == 'si'
        fecha = row['fecha']
        alumno = Alumno.objects.get(dni=int(row['alumno_dni']))
        profesor = Profesor.objects.get(dni=int(row['profesor_dni']))
        materia = Materia.objects.get(nombre=row['materia_nombre'], curso=alumno.curso)
        curso = alumno.curso

        # Crear la calificación.
        calificacion = Calificaciones.objects.create(
            nota=nota,
            final=final,
            fecha=fecha,
            alumno=alumno,
            profesor=profesor,
            materia=materia,
            curso=curso
        )
        calificacion.save()

        print(f'Se creó la calificación con el ID {calificacion.id}.')

def importar_materias(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        nombre = row['materia']
        horas = row['horas_catedra']
        curso = Curso.objects.get(anio=int(row['curso']))
        profesor = Profesor.objects.get(dni=int(row['profesor_dni']))

        # Crear la materia.
        materia = Materia.objects.create(
            nombre=nombre,
            horas_catedra=horas,
            curso=curso,
            profesor=profesor
        )
        materia.save()

        print(f'Se creó la materia {nombre}.')

def importar_profesores(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        dni = int(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        telefono = row.get('telefono', default='')
        email = row['email']

        # Crear o actualizar el profesor.
        profesor, creado = Profesor.objects.update_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'email': email
            }
        )

        if creado:
            print(f'Se creó el profesor {nombre} {apellido}.')
        else:
            print(f'Se actualizó el profesor {nombre} {apellido}.')

def importar_alumnos(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        dni = int(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        fecha_nacimiento = row.get('fecha_nacimiento', default=None)
        if type(fecha_nacimiento) == float:
            fecha_nacimiento = None
        email = row['email']
        curso = Curso.objects.get(anio=int(row['curso']))

        # Crear o actualizar el alumno.
        alumno, creado = Alumno.objects.update_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'fecha_nacimiento': fecha_nacimiento,
                'email': email,
                'repitio': 0,
                'curso': curso
            }
        )

        if creado:
            print(f'Se creó el alumno {nombre} {apellido}.')
        else:
            print(f'Se actualizó el alumno {nombre} {apellido}.')

# Código que hice a las apuradas para leer las calificaciones desde un PDF.
def importar_calificaciones_pdf(pdf):
    reader = PyPDF2.PdfReader(pdf) # Lector de PDF.
    content = reader.pages[0].extract_text() # Se extrae todo el contenido del PDF.

    pos = content.index('Curso:')

    # Obtener el nombre de la materia.
    subject = [] # Acá se va a ir guardando el nombre de la materia al revés.
    i = pos-1
    while content[i] != ':':
        subject.append(content[i])
        i -= 1
    subject.pop() # Eliminar espacio en blanco.
    subject.reverse() # Se da vuelta la palabra para que quede normal.
    subject = ''.join(subject)

    # Obtener el curso.
    grade = ''
    i = pos+7
    while content[i] != ' ':
        grade += content[i]
        i += 1

    parser = {
        'PRIMER': 1,
        'SEGUNDO': 2,
        'TERCER': 3,
        'CUARTO': 4,
        'QUINTO': 5,
        'SEXTO': 6
    }

    # Registro de errores al cargar las calificaciones.
    logs = []

    curso = Curso.objects.get(anio=parser[grade])
    materia = None
    try:
        materia = Materia.objects.get(nombre=subject, curso=curso)
    except:
        logs.append('ERROR AL CARGAR LAS CALIFICACIONES')
        logs.append(f'LA MATERIA "{subject}" NO EXISTE')
        return logs

    # Obtener los alumnos y sus notas.
    parts = content.split('\n')
    i = parts.index('Final')+1
    for j in range(i, len(parts)):
        # Obtener el apellido del alumno.
        lastname = ''
        k = 0
        while parts[j][k] != ',':
            lastname += parts[j][k]
            k += 1

        # Obtener el nombre del alumno.
        name = ''
        k += 2
        while not parts[j][k].isdigit():
            name += parts[j][k]
            k += 1

        alumno = None
        try:
            alumno = Alumno.objects.get(nombre=name, apellido=lastname, curso=curso)
        except:
            logs.append(f'"{name} {lastname}" NO SE ENCONTRÓ EN LOS REGISTROS')
            continue

        # Obtener notas.
        grades = parts[j][k:len(parts[j])].split(' ')
        for n in grades:
            Calificaciones.objects.create(
                alumno=alumno,
                curso=curso,
                materia=materia,
                profesor=materia.profesor,
                fecha=datetime.today(),
                nota=float(n),
                final=False
            )

    if logs:
        logs.append('LAS CALIFICACIONES FUERON CARGADAS CON ALGUNAS EXCEPCIONES')
    else:
        logs.append('TODAS LAS CALIFICACIONES FUERON CARGADAS CON ÉXITO')
    return logs
