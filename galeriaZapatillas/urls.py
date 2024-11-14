from django.urls import path
from . import views

app_name = 'zapatillas'

urlpatterns = [
    path('', views.lista_zapatillas, name='lista_zapatillas'),
    path('imagen/<int:pk>/', views.detalle_zapatillas, name='detalle_zapatillas'),
    path('subir/', views.subir_zapatillas, name='subir_zapatillas'),
    path('imagen/<int:pk>/editar/', views.editar_zapatillas, name='editar_zapatillas'),
    path('imagen/<int:pk>/eliminar/', views.eliminar_zapatillas, name='eliminar_zapatillas'),
]