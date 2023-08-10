from django.shortcuts import redirect
from buscador_id import rol_usuario_get

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            user = rol_usuario_get(request)
            if user.rol in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('error_no_permisos.html')
        return wrapper
    return decorator