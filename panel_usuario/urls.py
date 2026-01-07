from django.urls import path
from . import views

urlpatterns = [
    path('panelusuario/', views.dashboard, name='user_panel'),
]
