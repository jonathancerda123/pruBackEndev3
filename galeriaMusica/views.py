from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Imagen
from .forms import ImagenForm
from django.contrib.auth.decorators import login_required

# Create your views here.



def lista_musica(request):
    imagenes = Imagen.objects.all().order_by('-fecha_subida')
    return render(request, 'galeriaMusica/lista_musica.html', {'imagenes': imagenes})

def detalle_musica(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    return render(request, 'galeriaMusica/detalle_musica.html', {'imagen': imagen,'request':request})

@login_required
def subir_musica(request):
    if request.user.perfil.rol in ['editor', 'administrador']:
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES)
            if form.is_valid():
                imagen = form.save(commit=False)
                imagen.compositor = request.user
                imagen.save()
                return redirect('galeriaMusica:detalle_musica', pk=imagen.pk)
        else:
            form = ImagenForm()
        return render(request, 'galeriaMusica/subir_musica.html', {'form': form})
    else:
        return redirect('galeriaMusica:lista_musica')
    

@login_required
def editar_musica(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.compositor or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES, instance=imagen)
            if form.is_valid():
                form.save()
                messages.success(request, 'Imagen actualizada exitosamente.')
                return redirect('galeriaMusica:detalle_musica', pk=imagen.pk)
        else:
            form = ImagenForm(instance=imagen)
        return render(request, 'galeriaMusica/editar_musica.html', {'form': form, 'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para editar esta imagen.')
        return redirect('galeriaMusica:detalle_musica', pk=pk)

@login_required
def eliminar_musica(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.compositor or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            imagen.delete()
            messages.success(request, 'Imagen eliminada exitosamente.')
            return redirect('galeriaMusica:lista_musica')
        else:
            return render(request, 'galeriaMusica/eliminar_musica.html', {'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para eliminar esta imagen.')
        return redirect('galeriaMusica:detalle_musica', pk=pk)