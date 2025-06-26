
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include ('gestao.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('admin/', admin.site.urls),
]




