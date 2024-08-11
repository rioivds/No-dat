from django.shortcuts import render, redirect

def index(request):
    if (not request.user.is_authenticated):
        return redirect('iniciar_sesion')
    return render(request, 'chat.html')