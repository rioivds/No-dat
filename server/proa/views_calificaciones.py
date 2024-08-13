import datetime
from django.shortcuts import render, redirect
from proa.models import Alumno, Curso, Calificaciones, Profesor, Materia
from datetime import datetime
from .importaciones import importar_calificaciones, importar_calificaciones_pdf
from .common import Common

def index(request):
    cursos = Curso.objects.all()
    return render(request, 'calificaciones/index.html', {'cursos': cursos})

def mostrar_calificaciones(request, curso):
    calificaciones = Calificaciones.objects.filter(curso_id=curso)
    alumnos = Alumno.objects.filter(curso_id=curso)
    materias = Materia.objects.filter(curso_id=curso)
    profesores = Profesor.objects.all()

    return render(request, 'calificaciones/mostrar_calificaciones.html', {
        'calificaciones': calificaciones,
        'alumnos': alumnos,
        'materias': materias,
        'profesores': profesores,
        'curso': curso
    })

def guardar_calificaciones(request):
    alumno = request.POST['alumno']
    curso = request.POST['curso']
    materia=request.POST['materia']
    profesor=request.POST['profesor']
    fecha_nota_str = datetime.strptime(request.POST['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
    nota = request.POST['nota']
    final = request.POST.get('final') == 'on'  # Conversión a True si está marcado

    insert = Calificaciones(
        alumno=Alumno.objects.get(dni=alumno),
        curso=Curso.objects.get(id=curso),
        materia=Materia.objects.get(id=materia),
        profesor=Profesor.objects.get(dni=profesor),
        fecha=fecha_nota_str,
        nota=nota,
        final=final
    )
    insert.save()

    return redirect(f'/calificaciones/mostrar/{curso}/')

def eliminar_calificaciones(request):
    calificacion = Calificaciones.objects.get(id=request.GET['id'])
    calificacion.delete()
    return redirect(f'/calificaciones/mostrar/{calificacion.curso.anio}/')

def editar_calificaciones(request):
    id = request.GET['id']
    calificaciones = Calificaciones.objects.all()
    calificaciones_editar = Calificaciones.objects.get(id=id)
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()

    return render(request, 'calificaciones/index.html', {
        'mensaje': '',
        'calificaciones_edit': calificaciones_editar,
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def guardar_edit(request):
    id = request.GET['id']
    alumno = request.POST['alumno']
    curso = request.POST['curso']
    materia = request.POST['materia']
    profesor = request.POST['profesor']
    fecha = request.POST['fecha']
    fecha_nota_str = Common.parse_fecha(fecha)
    nota = float(request.POST['nota'].replace(',', '.'))
    final = request.POST.get('final', False) == 'True'
    calificaciones = Calificaciones.objects.all()
    materias = Materia.objects.all()
    profesores = Profesor.objects.all()
    cursos = Curso.objects.all()
    alumnos = Alumno.objects.all()
    Calificaciones.objects.filter(id=id).update(alumno=Alumno.objects.get(dni=alumno), curso=Curso.objects.get(id=curso), materia=Materia.objects.get(id=materia), profesor=Profesor.objects.get(dni=profesor),  fecha=fecha_nota_str, nota=nota, final=final)

    return render(request, 'calificaciones/index.html', {
        'mensaje': 'Se editó correctamente',
        'calificaciones': calificaciones,
        'materias': materias,
        'cursos': cursos,
        'profesores': profesores,
        'alumnos': alumnos
    })

def importar_calificaciones_view(request):
    if request.method == 'GET':
        return render(request, 'calificaciones/importar_calificaciones.html', {'mensajes': None})

    archivo = request.FILES['archivo_excel']
    print(archivo)
    extension = str(archivo).split('.')[-1]

    logs = None
    if extension == 'pdf':
        logs = importar_calificaciones_pdf(archivo)
    elif extension == 'xlsx':
        importar_calificaciones(archivo)

    return render(request, 'calificaciones/importar_calificaciones.html', {'mensajes': logs})

def calificaciones_json (request, dni):
    alumno = Alumno.objects.get(dni = dni).dni
    calificaciones = Calificaciones.objects.filter(alumno = alumno)
    res = {}

    for i in calificaciones:
        try:
            res[f'{i.materia.nombre}'].append(i.nota);
        except:
            res[f'{i.materia.nombre}'] = []
            res[f'{i.materia.nombre}'].append(i.nota)

    return HttpResponse(json.dumps(res), content_type="application/json")

