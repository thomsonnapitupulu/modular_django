# product_module/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Product(models.Model):
    """Model representing a product."""
    name = models.CharField(_("Product name"), max_length=200)
    barcode = models.CharField(_("Barcode"), max_length=100, unique=True)
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock = models.IntegerField(_("Stock"), default=0)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])