from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.views.decorators.http import require_POST
from store.models import Product, ExchangeRate
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
    
    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
        
    return redirect('carrito:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('carrito:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    action = request.POST.get('action')
    
    current_quantity = cart.cart.get(str(product_id), {}).get('quantity', 0)
    
    if action == 'increase':
        cart.add(product=product, quantity=current_quantity + 1, override_quantity=True)
    elif action == 'decrease':
        cart.add(product=product, quantity=current_quantity - 1, override_quantity=True)
        
    # Prepare response data
    item = cart.cart.get(str(product_id))
    if item:
        item_total = Decimal(item['price']) * item['quantity']
        quantity = item['quantity']
    else:
        # Item removed
        item_total = 0
        quantity = 0
        
    return JsonResponse({
        'success': True,
        'quantity': quantity,
        'item_total': str(item_total),
        'cart_total': str(cart.get_total_price()),
        'cart_items_count': len(cart)
    })

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'carrito/detail.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('product_list')

    # Obtener tasa de cambio
    try:
        manual_rate = ExchangeRate.objects.latest().rate
    except ExchangeRate.DoesNotExist:
        manual_rate = None

    if request.method == 'POST':
        metodo_pago = request.POST.get('metodo_pago')
        referencia = request.POST.get('referencia_pago')
        
        # Validar método de pago
        valid_methods = [c[0] for c in Pedido.PAYMENT_METHOD_CHOICES]
        if metodo_pago not in valid_methods:
             messages.error(request, "Método de pago inválido.")
             return render(request, 'carrito/checkout.html', {
                 'cart': cart,
                 'manual_rate': manual_rate
             })

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

    return render(request, 'carrito/checkout.html', {
        'cart': cart, 
        'manual_rate': manual_rate
    })
