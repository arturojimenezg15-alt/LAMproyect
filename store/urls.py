from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
]
