import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_management.settings')
django.setup()

from store.models import Product
from inventory.models import Supplier, InventoryTransaction

def verify():
    print("Verifying Inventory App...")

    # Create a test product
    product, created = Product.objects.get_or_create(
        name='Test Product',
        defaults={'description': 'Test', 'price': 10.00, 'stock': 100}
    )
    initial_stock = product.stock
    print(f"Initial Product Stock: {initial_stock}")

    # Create a supplier
    supplier, created = Supplier.objects.get_or_create(
        name='Test Supplier',
        defaults={'email': 'test@example.com'}
    )
    print(f"Created Supplier: {supplier.name}")

    # Create an IN transaction (Purchase)
    print("Creating Purchase Transaction (+50)...")
    InventoryTransaction.objects.create(
        product=product,
        quantity=50,
        transaction_type='purchase',
        supplier=supplier,
        notes='Initial purchase'
    )

    # Refetch product
    product.refresh_from_db()
    print(f"Stock after purchase: {product.stock}")

    if product.stock == initial_stock + 50:
        print("SUCCESS: Stock updated correctly via signals.")
    else:
        print("FAILURE: Stock did not update correctly.")

    # Create an OUT transaction (Sale)
    print("Creating Sale Transaction (-10)...")
    InventoryTransaction.objects.create(
        product=product,
        quantity=-10,
        transaction_type='sale',
        notes='Sold to customer'
    )

    product.refresh_from_db()
    print(f"Stock after sale: {product.stock}")

    if product.stock == initial_stock + 50 - 10:
        print("SUCCESS: Stock updated correctly after sale.")
    else:
        print("FAILURE: Stock did not update correctly after sale.")
    
    # Cleanup
    print("Cleaning up test data...")
    # Product and Supplier might be kept, but for this test we can leave them or delete them.
    # Let's keep them as proof of work unless we want a clean state.
    # For now, just exiting.

if __name__ == '__main__':
    verify()
