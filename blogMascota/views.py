from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Imagen
from .forms import ImagenForm
from django.contrib.auth.decorators import login_required

def lista(request):
    imagenes = Imagen.objects.all().order_by('-fecha_subida')
    return render(request, 'blogMascota/lista_mascota.html', {'imagenes': imagenes})

def detalle(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    return render(request, 'blogMascota/detalle_mascota.html', {'imagen': imagen,'request':request})

@login_required
def subir(request):
    if request.user.perfil.rol in ['editor', 'administrador']:
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES)
            if form.is_valid():
                imagen = form.save(commit=False)
                imagen.autor = request.user
                imagen.save()
                return redirect('blogMascota:detalleMascota', pk=imagen.pk)
        else:
            form = ImagenForm()
        return render(request, 'blogMascota/subir_mascota.html', {'form': form})
    else:
        return redirect('blogMascota:listaMascota')

@login_required
def editar(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.autor or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES, instance=imagen)
            if form.is_valid():
                form.save()
                messages.success(request, 'Imagen actualizada exitosamente.')
                return redirect('blogMascota:detalleMascota', pk=imagen.pk)
        else:
            form = ImagenForm(instance=imagen)
        return render(request, 'blogMascota/editar_mascota.html', {'form': form, 'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para editar esta imagen.')
        return redirect('blogMascota:detalleMascota', pk=pk)
    
@login_required
def eliminar(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.autor or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            imagen.delete()
            messages.success(request, 'Imagen eliminada exitosamente.')
            return redirect('blogMascota:listaMascota')
        else:
            return render(request, 'blogMascota/eliminar_mascota.html', {'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para eliminar esta imagen.')
        return redirect('blogMascota:detalleMascota', pk=pk)