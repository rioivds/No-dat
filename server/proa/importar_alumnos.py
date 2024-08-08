import pandas
from .models import Alumno, Curso

def importar_alumnos(archivo):
    df = pandas.read_excel(archivo, engine='openpyxl')
    for _, row in df.iterrows():
        dni = int(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        fecha_nacimiento = row.get('fecha_nacimiento', default=None)
        email = row['email']
        curso = Curso.objects.get(anio=int(row['curso']))

        # Crear o actualizar el alumno
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
