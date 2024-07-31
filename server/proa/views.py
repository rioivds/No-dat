import datetime
from django.shortcuts import render
from .models import Curso

def index(request):
    cursos = Curso.objects.all()
    today = datetime.datetime.now()
    return render(request, 'index.html', {
        'today': today,
        'cursos': cursos
    })
