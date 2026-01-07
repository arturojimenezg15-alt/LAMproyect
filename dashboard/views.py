from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from store.models import Product
from pedidos.models import Pedido
from django.contrib.auth.models import User
import json

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard_home(request):
    # Key Metrics
    total_products = Product.objects.count()
    total_orders = Pedido.objects.count()
    unique_customers = Pedido.objects.values('comprador').distinct().count()
    
    # Calculate Total Revenue
    total_revenue = Pedido.objects.aggregate(
        total=Sum('total')
    )['total'] or 0

    # Recent Orders
    recent_orders = Pedido.objects.select_related('comprador', 'producto').order_by('-fecha_creacion')[:5]

    # Monthly Sales Data for Chart
    sales_data = Pedido.objects.annotate(
        month=TruncMonth('fecha_creacion')
    ).values('month').annotate(
        total_sales=Sum('total'),
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
