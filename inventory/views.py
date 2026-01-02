from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.contrib import messages
from store.models import Product
from store.forms import ProductForm
from .models import InventoryTransaction

def inventory_index(request):
    products = Product.objects.all().order_by('-created_at')
    
    # Handle Search
    query = request.GET.get('q')
    if query:
        products = products.filter(name__istartswith=query)

    # Metrics
    total_products = products.count()
    low_stock = products.filter(stock__lt=10).count()
    total_value = products.aggregate(
        total=Sum(F('price') * F('stock'))
    )['total'] or 0

    # Add Product Form Handling
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('inventory_index')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'total_products': total_products,
        'low_stock': low_stock,
        'total_value': total_value,
        'form': form,
        'search_query': query if query else ''
    }
    return render(request, 'inventory/index.html', context)
