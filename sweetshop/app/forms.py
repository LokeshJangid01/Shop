from django import forms
from .models import Product,Order,OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Enter price'}),
            
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name',)
        widgets = {
            'customer_name':forms.TextInput(attrs={'class':'form-control'}),
            
            
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']