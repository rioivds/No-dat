import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso, Calificaciones,Profesor,Materia
from django.db import connection
from django.shortcuts import get_object_or_404
from datetime import datetime


TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    calificaciones = Calificaciones.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    materias=Materia.objects.all()
    alumnos=Alumno.objects.all()
    return render(request, 'calificaciones/index.html',{ "calificaciones": calificaciones,"materias": materias, "cursos": cursos, "profesores": profesores, "alumnos":alumnos})

def parse_fecha(fecha_str):
    meses = {
        'enero': '01',
        'febrero': '02',
        'marzo': '03',
        'abril': '04',
        'mayo': '05',
        'junio': '06',
        'julio': '07',
        'agosto': '08',
        'septiembre': '09',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12'
    }
    
    partes = fecha_str.split(' ')
    dia = partes[0]
    mes = meses[partes[2]]
    anio = partes[4]
    
    return f"{anio}-{mes}-{dia}"

def guardar_calificaciones(request):
    alumno=request.POST["alumno"]
    curso = request.POST["curso"]
    materia=request.POST["materia"]
    profesor=request.POST["profesor"]
    fecha = request.POST["fecha"]
    fecha_nota_str = datetime.strptime(fecha, "%m/%d/%Y").strftime("%Y-%m-%d")
    nota = request.POST["nota"]
    final = request.POST.get("final") == "on"  # Conversión a True si está marcado
    
    insert = Calificaciones(
        alumno=Alumno.objects.get(dni=alumno),
        curso=Curso.objects.get(id=curso),
        materia=Materia.objects.get(id=materia),
        profesor=Profesor.objects.get(dni=profesor),
        fecha=fecha_nota_str,
        nota=nota,
        final=final,
        )
    insert.save()
    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, 'calificaciones/index.html', {"mensaje": "Se insertó calificación con éxito", "calificaciones": calificaciones,"materias": materias, "cursos": cursos, "profesores": profesores, "alumnos": alumnos})


def eliminar_calificaciones(request):
    id = request.GET["id"]
    delete = get_object_or_404(Calificaciones, id=id)
    delete.delete()
    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, 'calificaciones/index.html', {"mensaje": "Se elimino calificación con éxito", "calificaciones": calificaciones,"materias": materias, "cursos": cursos, "profesores": profesores, "alumnos": alumnos})

def editar_calificaciones(request):
    id = request.GET["id"]
    calificaciones = Calificaciones.objects.all()
    calificaciones_editar = Calificaciones.objects.get(id=id)
    print("editar", calificaciones_editar.id)
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    return render(request, 'calificaciones/index.html', {"mensaje": "","calificaciones_edit":calificaciones_editar, "calificaciones": calificaciones,"materias": materias, "cursos": cursos, "profesores": profesores, "alumnos": alumnos})

def guardar_edit(request):
    id = request.GET["id"]
    alumno=request.POST["alumno"]
    curso=request.POST["curso"]
    materia=request.POST["materia"]
    profesor=request.POST["profesor"]
    fecha = request.POST["fecha"]
    fecha_nota_str = parse_fecha(fecha)
    nota = request.POST["nota"]
    nota = request.POST["nota"].replace(",", ".")
    nota = float(nota)
    final = request.POST.get('final', False) == 'True'
    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    Calificaciones.objects.filter(id = id).update(alumno=Alumno.objects.get(dni=alumno), curso=Curso.objects.get(id=curso), materia=Materia.objects.get(id=materia), profesor=Profesor.objects.get(dni=profesor),  fecha=fecha_nota_str, nota=nota, final=final)
    return render(request, 'calificaciones/index.html', {"mensaje": "se editó correctamente", "calificaciones": calificaciones,"materias": materias, "cursos": cursos, "profesores": profesores, "alumnos": alumnos})


