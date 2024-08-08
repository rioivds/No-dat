from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

def entrar(request):
    if request.method == 'GET':
        return render(request, 'login/index.html', {'user_exists': True})

    # Trata de autenticar el usuario con los datos brindados.
    user = authenticate(
        request,
        username=request.POST['dni'],
        password=request.POST['password']
    )

    # Si el usuario que se ingresó no existe, se devolverá un mensaje de error.
    if user is None:
        return render(request, 'login/index.html', {'user_exists': False})

    # Se inicia la sesión del usuario y carga la página principal.
    login(request, user)
    return redirect('/')
