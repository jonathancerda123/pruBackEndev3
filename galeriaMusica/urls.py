from django.urls import path
from . import views

app_name = 'musica'

urlpatterns = [
    path('', views.lista_musica, name='lista_musica'),
    path('imagen/<int:pk>/', views.detalle_musica, name='detalle_musica'),
    path('subir/', views.subir_musica, name='subir_musica'),
    path('imagen/<int:pk>/editar/', views.editar_musica, name='editar_musica'),
    path('imagen/<int:pk>/eliminar/', views.eliminar_musica, name='eliminar_musica'),
]