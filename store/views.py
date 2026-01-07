from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Product


from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    ordering = ['-created_at']
    

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'forms.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'forms.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.seller


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'

