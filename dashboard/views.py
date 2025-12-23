from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from store.models import Product, Order
from django.contrib.auth.models import User
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    # Key Metrics
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    unique_customers = Order.objects.values('user').distinct().count()
    
    # Calculate Total Revenue (Simple calculation since Order maps to Product)
    # We sum the price of the product associated with each order
    total_revenue = Order.objects.aggregate(
        total=Sum('product__price')
    )['total'] or 0

    # Recent Orders
    recent_orders = Order.objects.select_related('user', 'product').order_by('-created_at')[:5]

    # Monthly Sales Data for Chart
    # Group by month and sum product prices
    sales_data = Order.objects.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        total_sales=Sum('product__price'),
        count=Count('id')
    ).order_by('month')

    # Prepare data for Chart.js
    labels = []
    data = []
    for entry in sales_data:
        if entry['month']:
            labels.append(entry['month'].strftime('%b %Y'))
            data.append(float(entry['total_sales']))

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'unique_customers': unique_customers,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }

    return render(request, 'dashboard/home.html', context)
