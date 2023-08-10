from proa.models import Usuario  # Asegúrate de importar tu modelo de usuario personalizado

def rol_usuario_get(request):
    # Obtener el ID del usuario autenticado de tu sistema de autenticación
    usuario_id = request.POST["id"]  


    if usuario_id:
        try:
            # Recuperar el usuario desde tu sistema de autenticación basado en el ID
            user = Usuario.objects.get(id=usuario_id)
            return user
        except Usuario.DoesNotExist:
            return None

    return None