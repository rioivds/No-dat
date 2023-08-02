import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from .models import Alumno, Curso

def importar_alumnos(desde_archivo):
    df = pd.read_excel(desde_archivo, engine='openpyxl')

    for _, row in df.iterrows():
        dni = str(row['dni'])
        nombre = row['nombre']
        apellido = row['apellido']
        fecha_nacimiento = row['fecha_nacimiento']
        email = row['email']
        repitio = row['repitio']
        curso_anio = row['curso']

        # Buscar el curso por año (puedes adaptar esto según la estructura de tus datos)
        try:
            curso = Curso.objects.get(anio=curso_anio)
        except ObjectDoesNotExist:
            print(f"El curso {curso_anio} no existe en la base de datos.")
            continue

        # Crear o actualizar el alumno
        alumno, creado = Alumno.objects.update_or_create(
            dni=dni,
            defaults={
                'nombre': nombre,
                'apellido': apellido,
                'fecha_nacimiento': fecha_nacimiento,
                'email': email,
                'repitio': repitio,
                'curso': curso,
            }
        )

        if creado:
            print(f"Se creó el alumno {nombre} {apellido}.")
        else:
            print(f"Se actualizó el alumno {nombre} {apellido}.")

if __name__ == "__main__":
    archivo_excel = "ruta/del/archivo.xlsx"  # Ruta al archivo Excel que deseas importar
    importar_alumnos(archivo_excel)
