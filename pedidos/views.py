from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pedido
from store.models import Product

@login_required
def crear_pedido(request, product_id):
    producto = get_object_or_404(Product, id=product_id)
    
    if producto.stock <= 0:
        messages.error(request, "Lo sentimos, esta pieza ya no está disponible.")
        return redirect('product_detail', pk=product_id)
        
    if request.method == 'POST':
        metodo = request.POST.get('metodo_pago')
        referencia = request.POST.get('referencia_pago')
        
        pedido = Pedido.objects.create(
            comprador=request.user,
            vendedor=producto.seller,
            producto=producto,
            precio_unidad=producto.price,
            total=producto.price, # Por ahora 1 unidad
            metodo_pago=metodo,
            referencia_pago=referencia,
            estado='pagado' if referencia else 'pendiente'
        )
        
        # Descontar stock
        producto.stock -= 1
        producto.save()
        
        messages.success(request, f"¡Pedido #{pedido.id} realizado con éxito!")
        return redirect('lista_pedidos')
        
    return redirect('product_detail', pk=product_id)

@login_required
def lista_pedidos(request):
    # Pedidos realizados por el usuario (Compras)
    mis_compras = Pedido.objects.filter(comprador=request.user)
    # Pedidos recibidos por el usuario (Ventas)
    mis_ventas = Pedido.objects.filter(vendedor=request.user)
    
    return render(request, 'pedidos/lista.html', {
        'compras': mis_compras,
        'ventas': mis_ventas
    })

@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Solo comprador o vendedor pueden ver el detalle
    if request.user != pedido.comprador and request.user != pedido.vendedor:
        return redirect('lista_pedidos')
        
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})
