import datetime
from xml.dom.minidom import Document
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.db.models import Q
from proa.models import Alumno, Curso
from django.db import connection
from django.shortcuts import get_object_or_404
from datetime import datetime

def index(request):
    alumnos = Alumno.objects.all()
    return render(request, 'informes/index.html',{ "alumnos": alumnos})

def generar_informe(request):
    alumnos = Alumno.objects.all()
    return render(request, 'informes/index.html',{ "alumnos": alumnos})
