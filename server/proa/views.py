import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from proa.models import Cursos  
# Create your views here.
TEMPLATE_DIR = ('os.path.join(BASE_DIR,"templates")')


def index(request):
    cursos = Cursos.objects.all()
    today = datetime.datetime.now()
    return render(request, 'index.html',
                  {"today": today,
                   "titulo": ' Titulo desde la vista',
                   'texto': 'aca ponemos algo de texto desde la base',
                   'cursos': cursos
                   })

def guardar(request):
    return HttpResponse('Hola Sou guardar')


