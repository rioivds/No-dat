import pandas
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
