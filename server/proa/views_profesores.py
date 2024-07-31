from django.shortcuts import render
from proa.models import Profesor
from django.shortcuts import get_object_or_404

def index(request):
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html', {'profesores': profesores})

def guardar_profesores(request):
    DNI = request.POST['DNI']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    email = request.POST['email']
    telefono = request.POST['telefono']

    if Profesor.objects.filter(dni=DNI).exists():
        profesores = Profesor.objects.all()
        return render(request, 'profesores/index.html', {'mensaje': 'Este profesor ya existe', 'profesores': profesores})

    insert = Profesor(nombre=nombre, apellido=apellido, email=email, dni=DNI, telefono=telefono)
    insert.save()

    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html', {'mensaje': 'Se inserto con exito', 'profesores': profesores})

def eliminar_profesores(request):
    DNI = request.GET['DNI']
    profesor = get_object_or_404(Profesor, dni=DNI)
    profesor.delete()
    profesores = Profesor.objects.all()
    return render(request, 'profesores/index.html', {'mensaje': 'Se eliminó el Profesor con éxito', 'profesores': profesores})

def editar_profesores(request):
    DNI = request.GET['DNI']
    profesores = Profesor.objects.all()
    profesores_editar = Profesor.objects.get(dni=DNI)
    return render(request, 'profesores/index.html', {'mensaje': '', 'profesores': profesores, 'profesores_edit': profesores_editar})

def guardar_edit(request):
    DNI = request.POST ['DNI']
    nombre = request.POST ['nombre']
    apellido = request.POST ['apellido']
    email = request.POST ['email']
    telefono=request.POST['telefono']

    profesores = Profesor.objects.all()
    Profesor.objects.filter(dni=DNI).update(dni=DNI, nombre=nombre, apellido=apellido, email=email, telefono=telefono)

    return render(request, 'profesores/index.html', {'mensaje': 'Se editó correctamente', 'profesores': profesores})


