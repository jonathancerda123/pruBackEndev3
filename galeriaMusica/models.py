from django.db import models
from django.contrib.auth.models import User

class Imagen(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='imagenes/')
    compositor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imagenes_galeria_musica')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo