# product_module/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseForbidden

from .models import Product
from .forms import ProductForm
from .permissions import has_product_permission


class ProductListView(ListView):
    """View for listing all products."""
    model = Product
    context_object_name = 'products'
    template_name = 'product_module/product_list.html'
    paginate_by = 10


class ProductDetailView(DetailView):
    """View for displaying a product's details."""
    model = Product
    context_object_name = 'product'
    template_name = 'product_module/product_detail.html'


@method_decorator(login_required, name='dispatch')
class ProductCreateView(CreateView):
    """View for creating a new product."""
    model = Product
    form_class = ProductForm
    template_name = 'product_module/product_form.html'
    success_url = reverse_lazy('product_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not has_product_permission(request.user, 'can_add'):
            return HttpResponseForbidden("You don't have permission to add products.")
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, _("Product created successfully."))
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductUpdateView(UpdateView):
    """View for updating an existing product."""
    model = Product
    form_class = ProductForm
    template_name = 'product_module/product_form.html'
    context_object_name = 'product'
    
    def dispatch(self, request, *args, **kwargs):
        if not has_product_permission(request.user, 'can_change'):
            return HttpResponseForbidden("You don't have permission to edit products.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, _("Product updated successfully."))
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProductDeleteView(DeleteView):
    """View for deleting a product."""
    model = Product
    template_name = 'product_module/confirm_delete.html'
    success_url = reverse_lazy('product_list')
    context_object_name = 'product'
    
    def dispatch(self, request, *args, **kwargs):
        if not has_product_permission(request.user, 'can_delete'):
            return HttpResponseForbidden("You don't have permission to delete products.")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _("Product deleted successfully."))
        return super().delete(request, *args, **kwargs)


def index(request):
    """Landing page for the product module."""
    return render(request, 'product_module/index.html')