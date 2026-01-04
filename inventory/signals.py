from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from .models import InventoryTransaction

@receiver(post_save, sender=InventoryTransaction)
def update_stock_on_save(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            product = instance.product
            product.stock += instance.quantity
            product.save()

# Note: Handling updates/deletes of transactions strictly to reverse stock changes 
# can be complex (e.g. if quantity changed). For V1, we simply handle creation.
# Ideally, you'd lock the row or use F() expressions for concurrency safety, 
# but this suffices for the initial implementation.
