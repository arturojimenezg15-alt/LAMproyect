from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:product_id>/', views.crear_pedido, name='crear_pedido'),
    path('mis-pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('detalle/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]
