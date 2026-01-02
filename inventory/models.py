from django.db import models
from store.models import Product

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('purchase', 'Purchase (In)'),
        ('sale', 'Sale (Out)'),
        ('adjustment', 'Adjustment (+/-)'),
        ('return', 'Return (In)'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory_transactions')
    quantity = models.IntegerField(help_text="Positive for addition, negative for deduction")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity})"
