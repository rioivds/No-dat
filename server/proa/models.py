from email.policy import default
from enum import auto
from pickle import TRUE
from tkinter import CASCADE
from tokenize import blank_re
from django.db import models
from .choices import cursos

# Create your models here.

class Cursos(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Curso')
    curso = models.CharField(max_length=50, null = False)
    #curso = models.CharField(choices=cursos, null=False)  <--IGNORAR

class Alumno(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id_alumno')
    nombre = models.CharField(max_length=50, null = False)
    apellido = models.CharField(max_length=50, null = False)
    email = models.EmailField(max_length=50)
    documento = models.IntegerField(null = False)
    curso = models.ForeignKey(Cursos, null=False, on_delete=models.CASCADE) #Relacion: Alumno-Curso  

class Profesores(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='id_profesor')
    nombre = models.CharField(max_length=50, null = False)
    apellido = models.CharField(max_length=50, null = False)
    email = models.EmailField(max_length=50)
    documento = models.IntegerField(null = False)

class Calificaciones(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Calificacion')
    nota = models.IntegerField(null=False)
    fecha = models.DateTimeField(null=False, blank=False)
    recuperatorio = models.BooleanField(blank=False, default=False)
    nota_final = models.IntegerField(null=False)
    profesor = models.ForeignKey(Profesores, null=True, on_delete=models.CASCADE) #Relacion: Calificacion-Profesor
    alumno = models.ForeignKey(Alumno, null=True, on_delete=models.CASCADE) #Relacion: Calificacion-Alumno

class Materias(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID Materia')
    materia = models.CharField(max_length=50) 
    profesor = models.ForeignKey(Profesores, null=True, on_delete=models.CASCADE) #Relacion: Materia-Profesor 
    curso = models.ForeignKey(Cursos, null=False, on_delete=models.CASCADE) #Relacion: Materia-Curso 
    



    

