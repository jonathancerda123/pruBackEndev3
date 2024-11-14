from django.urls import path
from . import views

app_name = 'blogMascota'

urlpatterns = [
    path('', views.lista_mascota, name='listaMascota'),
    path('imagen/<int:pk>/', views.detalle_mascota, name='detalleMascota'),
    path('subir/', views.subir_mascota, name='subirMascota'),
    path('imagen/<int:pk>/editar/', views.editar_mascota, name='editarMascota'),
    path('imagen/<int:pk>/eliminar/', views.eliminar_mascota, name='eliminarMascota'),
]