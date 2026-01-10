from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from pedidos.models import Pedido
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
         # logic for ajax add
        cart.add(product=product, quantity=1)
        return JsonResponse({'cart_total': len(cart), 'success': True})
    
    # Fallback for non-ajax
    cart.add(product=product, quantity=1)
    return redirect('carrito:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carrito:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'carrito/detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('product_list')

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        referencia = request.POST.get('referencia_pago')
        
        # Validar método de pago
        valid_methods = [c[0] for c in Pedido.PAYMENT_METHOD_CHOICES]
        if metodo_pago not in valid_methods:
             messages.error(request, "Método de pago inválido.")
             return render(request, 'carrito/checkout.html', {'cart': cart})

        # Crear pedidos
        for item in cart:
            product = item['product']
            # Verificar stock
            if product.stock < item['quantity']:
                messages.error(request, f"Producto {product.name} sin stock suficiente.")
                return redirect('carrito:cart_detail')
            
            # Crear Pedido
            Pedido.objects.create(
                comprador=request.user,
                vendedor=product.seller, # Asumiendo que el producto tiene vendedor
                producto=product,
                cantidad=item['quantity'],
                precio_unidad=item['price'],
                total=item['total_price'],
                metodo_pago=metodo_pago,
                referencia_pago=referencia,
                estado='pagado' if referencia else 'pendiente'
            )
            
            # Actualizar stock
            product.stock -= item['quantity']
            product.save()
            
        cart.clear()
        messages.success(request, "¡Compra realizada con éxito!")
        return redirect('lista_pedidos')

    return render(request, 'carrito/checkout.html', {'cart': cart})
