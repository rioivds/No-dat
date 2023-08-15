from django.shortcuts import redirect
from proa.buscador_id import rol_usuario_get
from django.http import HttpResponseRedirect

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = request.session.get('usuario_rol')
            print(user)  
            if user == None:
                return HttpResponseRedirect('/')
            if user in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('error_no_permisos/')
        return wrapper
    return decorator