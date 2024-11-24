from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/detalle_productos.html', {'producto': producto})

@login_required
def crear_producto(request):
    if request.user.perfil.rol in ['editor', 'administrador']:
        if request.method == 'POST':
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('productos:lista_productos')
        else:
            form = ProductoForm()
        return render(request, 'productos/crear_productos.html', {'form': form})
    else:
        return redirect('productos:lista_productos')

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_productos.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('productos:lista_productos')
    return render(request, 'productos/eliminar_productos.html', {'producto': producto})