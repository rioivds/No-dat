import datetime
from django.shortcuts import render, redirect
from .models import Curso

def index(request):
    if (not request.user.is_authenticated):
        return redirect('iniciar_sesion')
        
    cursos = Curso.objects.all()
    today = datetime.datetime.now()
    return render(request, 'index.html', {
        'today': today,
        'cursos': cursos
    })
