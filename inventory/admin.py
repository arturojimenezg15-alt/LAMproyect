from django.contrib import admin
from .models import Supplier, InventoryTransaction

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'date', 'supplier')
    list_filter = ('transaction_type', 'date', 'supplier')
    search_fields = ('product__name', 'notes')
    date_hierarchy = 'date'
