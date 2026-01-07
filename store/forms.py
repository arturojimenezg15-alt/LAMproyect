from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']
        labels = {
            'name': 'Nombre del Producto',
            'description': 'Descripción',
            'price': 'Precio ($)',
            'stock': 'Cantidad en Stock',
            'image': 'Imagen del Producto',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Camiseta Elegante'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe los detalles del producto...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
