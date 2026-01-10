from django.db import models
from django.contrib.auth.models import User
from store.models import Product

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente de Pago'),
        ('pagado', 'Pagado / Verificando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('pago_movil', 'Pago Móvil'),
        ('zelle', 'Zelle'),
        ('paypal', 'PayPal'),
        ('cashea', 'Cashea'),
        ('transferencia', 'Transferencia Bancaria'),
    ]

    comprador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas')
    producto = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unidad = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.producto.name if self.producto else 'Producto eliminado'}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion']
