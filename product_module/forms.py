# product_module/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Product


class ProductForm(forms.ModelForm):
    """Form for creating and updating products."""
    
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        # Validate the barcode is not empty
        if not barcode:
            raise forms.ValidationError(_("Barcode cannot be empty."))
        
        # Check if barcode already exists for a different product
        if Product.objects.filter(barcode=barcode).exclude(id=self.instance.id if self.instance.id else None).exists():
            raise forms.ValidationError(_("A product with this barcode already exists."))
        
        return barcode
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        # Validate the price is positive
        if price <= 0:
            raise forms.ValidationError(_("Price must be greater than zero."))
        
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        # Validate stock is not negative
        if stock < 0:
            raise forms.ValidationError(_("Stock cannot be negative."))
        
        return stock