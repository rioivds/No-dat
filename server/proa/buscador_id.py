from proa.models import Usuario  # Asegúrate de importar tu modelo de usuario personalizado

def rol_usuario_get(request):
    # Obtener el ID del usuario autenticado de tu sistema de autenticación
    try:
        usuario_rol = request.session.get('rol_usuario')  
    except:
        usuario_rol = None

    if usuario_rol:
        try:
            # Recuperar el usuario desde tu sistema de autenticación basado en el ID
            user = Usuario.objects.get(id=usuario_rol)
            return user.rol
        except Usuario.DoesNotExist:
            return None

    return None