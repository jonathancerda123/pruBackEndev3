from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Imagen
from .forms import ImagenForm
from django.contrib.auth.decorators import login_required

def lista_zapatillas(request):
    imagenes = Imagen.objects.all().order_by('-fecha_subida')
    return render(request, 'galeriaZapatillas/lista_zapatillas.html', {'imagenes': imagenes})

def detalle_zapatillas(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    return render(request, 'galeriaZapatillas/detalle_zapatillas.html', {'imagen': imagen,'request':request})

@login_required
def subir_zapatillas(request):
    if request.user.perfil.rol in ['editor', 'administrador']:
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES)
            if form.is_valid():
                imagen = form.save(commit=False)
                imagen.marca = request.user
                imagen.save()
                return redirect('galeriaZapatillas:detalle_zapatillas', pk=imagen.pk)
        else:
            form = ImagenForm()
        return render(request, 'galeriaZapatillas/subir_zapatillas.html', {'form': form})
    else:
        return redirect('galeriaZapatillas:lista_zapatillas')

@login_required
def editar_zapatillas(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.marca or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            form = ImagenForm(request.POST, request.FILES, instance=imagen)
            if form.is_valid():
                form.save()
                messages.success(request, 'Imagen actualizada exitosamente.')
                return redirect('galeriaZapatillas:detalle_zapatillas', pk=imagen.pk)
        else:
            form = ImagenForm(instance=imagen)
        return render(request, 'galeriaZapatillas/editar_zapatillas.html', {'form': form, 'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para editar esta imagen.')
        return redirect('galeriaZapatillas:detalle_zapatillas', pk=pk)
    
@login_required
def eliminar_zapatillas(request, pk):
    imagen = get_object_or_404(Imagen, pk=pk)
    if request.user == imagen.marca or request.user.perfil.rol == 'administrador':
        if request.method == 'POST':
            imagen.delete()
            messages.success(request, 'Imagen eliminada exitosamente.')
            return redirect('galeriaZapatillas:lista_zapatillas')
        else:
            return render(request, 'galeriaZapatillas/eliminar_zapatillas.html', {'imagen': imagen})
    else:
        messages.error(request, 'No tienes permiso para eliminar esta imagen.')
        return redirect('galeriaZapatillas:detalle_zapatillas', pk=pk)