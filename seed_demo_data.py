import os
import django
import random
from decimal import Decimal
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'la_management.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, ExchangeRate
from inventory.models import Supplier, InventoryTransaction
from pedidos.models import Pedido

def seed_data():
    print("--- Inciando simulación de datos ---")

    # 1. Configurar Usuario Admin
    print("1. Configurando usuario admin...")
    admin_user, created = User.objects.get_or_create(username='admin')
    admin_user.set_password('1234')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f"   Admin {'creado' if created else 'actualizado'}. Usuario: admin, Clave: 1234")

    # 2. Crear usuarios de prueba (Compradores y Vendedores)
    print("2. Creando usuarios de prueba...")
    vendedor, _ = User.objects.get_or_create(username='vendedor_demo', defaults={'email': 'vendedor@demo.com'})
    if _: vendedor.set_password('vendedor123'); vendedor.save()
    
    comprador, _ = User.objects.get_or_create(username='comprador_demo', defaults={'email': 'comprador@demo.com'})
    if _: comprador.set_password('comprador123'); comprador.save()
    
    # 3. Configurar Tasa de Cambio
    print("3. Configurando tasa de cambio...")
    ExchangeRate.objects.update_or_create(id=1, defaults={'rate': Decimal('55.50')})

    # 4. Crear Proveedores
    print("4. Creando proveedores...")
    suppliers_data = [
        {'name': 'Textiles El Mundo', 'email': 'ventas@textiles.com', 'phone': '0212-5551234'},
        {'name': 'Importadora Calzado Plus', 'email': 'info@calzadoplus.com', 'phone': '0414-9998877'},
        {'name': 'Diseños Urbanos S.A.', 'email': 'contacto@du.com', 'phone': '0412-1112233'},
    ]
    suppliers = []
    for s_data in suppliers_data:
        s, created = Supplier.objects.get_or_create(name=s_data['name'], defaults=s_data)
        suppliers.append(s)

    # 5. Crear Productos
    print("5. Creando productos...")
    products_data = [
        {'name': 'Franela Básica Blanca', 'description': 'Franela de algodón 100% de alta calidad.', 'price': Decimal('15.00'), 'stock': 0},
        {'name': 'Jean Slim Fit Azul', 'description': 'Pantalón jean moderno y resistente.', 'price': Decimal('35.99'), 'stock': 0},
        {'name': 'Zapatos Deportivos Runner', 'description': 'Zapatos ideales para correr y entrenamiento.', 'price': Decimal('55.00'), 'stock': 0},
        {'name': 'Chaqueta de Cuero Sintético', 'description': 'Elegante chaqueta negra para cualquier ocasión.', 'price': Decimal('85.50'), 'stock': 0},
        {'name': 'Gorra Snapback Urban', 'description': 'Accesorio moderno con estilo urbano.', 'price': Decimal('12.00'), 'stock': 0},
        {'name': 'Sudadera con Capucha Gris', 'description': 'Comodidad y estilo para días frescos.', 'price': Decimal('28.00'), 'stock': 0},
        {'name': 'Cinturón de Cuero Marrón', 'description': 'Cinturón clásico de cuero genuino.', 'price': Decimal('18.75'), 'stock': 0},
        {'name': 'Reloj de Pulsera Análogo', 'description': 'Reloj elegante con correa metálica.', 'price': Decimal('45.00'), 'stock': 0},
    ]
    
    products = []
    for p_data in products_data:
        p, created = Product.objects.get_or_create(
            name=p_data['name'], 
            defaults={
                'description': p_data['description'], 
                'price': p_data['price'], 
                'stock': p_data['stock'],
                'seller': vendedor
            }
        )
        products.append(p)

    # 6. Crear Transacciones de Inventario (Compras)
    print("6. Agregando stock inicial...")
    for p in products:
        # Solo agregar stock si está en 0 o bajo
        if p.stock < 20:
            qty = random.randint(50, 100)
            InventoryTransaction.objects.create(
                product=p,
                quantity=qty,
                transaction_type='purchase',
                supplier=random.choice(suppliers),
                notes='Carga inicial de inventario'
            )
            print(f"   Stock añadido a {p.name}: +{qty}")

    # 7. Crear Pedidos (Simular ventas distribuidas en el tiempo)
    print("7. Simulando pedidos y ventas distribuidas en el tiempo...")
    status_list = ['pendiente', 'pagado', 'enviado', 'entregado']
    payment_methods = ['pago_movil', 'zelle', 'transferencia']
    
    # Limpiar pedidos previos para que la gráfica se vea limpia
    Pedido.objects.all().delete()
    
    now = timezone.now()
    
    for month_back in range(6, -1, -1): # Últimos 6 meses
        orders_this_month = random.randint(3, 8)
        for _ in range(orders_this_month):
            product = random.choice(products)
            qty = random.randint(1, 3)
            
            # Crear fecha aleatoria dentro del mes
            days_back = (month_back * 30) + random.randint(0, 28)
            order_date = now - timezone.timedelta(days=days_back)
            
            estado = random.choice(status_list)
            metodo = random.choice(payment_methods)
            
            pedido = Pedido.objects.create(
                comprador=comprador,
                vendedor=vendedor,
                producto=product,
                cantidad=qty,
                precio_unidad=product.price,
                total=product.price * qty,
                estado=estado,
                metodo_pago=metodo,
                referencia_pago=f'REF-{random.randint(100000, 999999)}' if estado != 'pendiente' else '',
                fecha_creacion=order_date
            )
            # Forzar la fecha de creación ya que auto_now_add suele ignorar el valor al crear
            Pedido.objects.filter(id=pedido.id).update(fecha_creacion=order_date)
            
            if estado in ['pagado', 'enviado', 'entregado']:
                InventoryTransaction.objects.create(
                    product=product,
                    quantity=-qty,
                    transaction_type='sale',
                    notes=f'Venta del pedido #{pedido.id}',
                    date=order_date
                )
                # Forzar la fecha también para transacciones
                InventoryTransaction.objects.filter(product=product, date__gt=order_date).update(date=order_date)

    print("\n--- Simulación completada con éxito ---")
    print(f"Productos totales: {Product.objects.count()}")
    print(f"Pedidos simulados: {Pedido.objects.count()}")
    print(f"Administrador: admin / 1234")

if __name__ == '__main__':
    seed_data()
