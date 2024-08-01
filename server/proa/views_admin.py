# proa/views_admin.py

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import requests
import os

@login_required
def index(request):
    router_ip = '192.168.200.1'
    port = '80'
    username = 'admin'
    password = 'proads.2024'

    scheme = 'https' if port == '443' else 'http'
    url = f'{scheme}://{router_ip}:{port}'

    try:
        response = requests.get(url, auth=(username, password), verify=False, timeout=10)

        if response.is_redirect or response.is_permanent_redirect:
            return HttpResponse(f"Redirigido a: {response.headers.get('Location')}")

        if response.status_code == 200:
            return HttpResponse(response.content)
        else:
            return HttpResponse(f"Error al acceder al router: {response.status_code}")

    except requests.RequestException as e:
        return HttpResponse(f"Error al acceder al router: {str(e)}")
