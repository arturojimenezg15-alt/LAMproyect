from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'image']
    template_name = 'forms.html'
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock', 'image']
    template_name = 'forms.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

