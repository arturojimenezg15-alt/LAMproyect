from django.shortcuts import render
from django.db.models import Sum
from .models import InventoryTransaction

def inventory_index(request):
    transactions = InventoryTransaction.objects.all().order_by('-date')
    return render(request, 'inventory/index.html', {'transactions': transactions})
