from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'comprador', 'vendedor', 'producto', 'total', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'metodo_pago', 'fecha_creacion')
    search_fields = ('comprador__username', 'vendedor__username', 'producto__name', 'referencia_pago')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    fieldsets = (
        ('Información de las Partes', {
            'fields': ('comprador', 'vendedor', 'producto')
        }),
        ('Detalles Económicos', {
            'fields': ('cantidad', 'precio_unidad', 'total')
        }),
        ('Estado y Pago', {
            'fields': ('estado', 'metodo_pago', 'referencia_pago')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
