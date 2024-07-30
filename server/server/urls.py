from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proa/', include('proa.urls')),
    path('', include('proa.urls')),
]
