from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Order
from django.contrib import messages
from django.forms import ModelForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image']

def is_superuser(user):
    return user.is_superuser

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'store/forms.html', {'form': form, 'title': 'Sign Up', 'action': 'Sign Up'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/forms.html', {'form': form, 'title': 'Log In', 'action': 'Log In'})

def logout_view(request):
    logout(request)
    return redirect('product_list')

def product_list(request):
    products = Product.objects.all()
    user_orders = []
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(user=request.user)
    return render(request, 'store/home.html', {'products': products, 'user_orders': user_orders})

@user_passes_test(is_superuser)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/forms.html', {'form': form, 'title': 'Create Product', 'action': 'Create'})

@user_passes_test(is_superuser)
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/forms.html', {'form': form, 'title': 'Update Product', 'action': 'Update'})

@user_passes_test(is_superuser)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
    return redirect('product_list')

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id) 
    Order.objects.create(user=request.user, product=product)
    messages.success(request, f"Order placed for {product.name}!")
    return redirect('product_list')
