from django.db import models
from django.contrib.auth.models import User

class Curso(models.Model):
    id = models.BigAutoField(primary_key=True,verbose_name='ID Curso')
    anio = models.IntegerField(verbose_name='Año')

class Profesor(models.Model):
    dni = models.BigIntegerField(primary_key=True, verbose_name='DNI Profesor')
    nombre = models.CharField(max_length=32, verbose_name='Nombre')
    apellido = models.CharField(max_length=32, verbose_name='Apellido')
    telefono = models.CharField(max_length=20, verbose_name='Telefono')
    email = models.EmailField(verbose_name='Email')
    faceid = models.CharField(max_length=512, verbose_name='FaceID', default = '0')

class Materia(models.Model):
    id = models.BigAutoField(primary_key=True,verbose_name='ID Materia')
    nombre = models.CharField(max_length=64, verbose_name='Nombre Materia')
    horas_catedra = models.IntegerField(verbose_name='Horas Catedra')
    profesor = models.ForeignKey(Profesor, null=True, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

class Alumno(models.Model):
    dni = models.BigIntegerField(primary_key=True, verbose_name='DNI Profesor')
    nombre = models.CharField(max_length=32, verbose_name='Nombre')
    apellido = models.CharField(max_length=32, verbose_name='Apellido')
    fecha_nacimiento = models.DateField(verbose_name='Fecha de nacimiento', blank=True, null=True)
    email = models.EmailField(verbose_name='Email')
    repitio = models.BooleanField(verbose_name='Repitio?',default=None, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, blank=True, null=True)
    faceid = models.CharField(max_length=512, verbose_name='FaceID', default = '0')

class Calificaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    fecha = models.DateField(verbose_name='Fecha')
    nota = models.FloatField(verbose_name='Nota')
    final = models.BooleanField(verbose_name='final')
