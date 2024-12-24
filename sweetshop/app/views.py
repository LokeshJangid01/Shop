from django.shortcuts import render,redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.views import View
from rest_framework.viewsets import ModelViewSet
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Product, Order,OrderItem
from .forms import ProductForm,OrderForm, OrderItemForm
from .serializers import OrderItemSerializer
# Create your views here.


"""
                        Creation of product

"""

class ProductListView(ListView):
    model = Product
    template_name = 'app/product_list.html'
    context_object_name = 'products'

class ProductCreateView(CreateView):    
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):    
    model = Product
    form_class = ProductForm
    template_name = 'app/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'app/Product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

#####################
#       Order       #
#####################

class OrderListView(ListView):
    model = Order
    template_name = 'app/order_list.html'
    context_object_name = 'orders'

class OrderCreateView(CreateView):    
    model = Order
    form_class = OrderForm
    template_name = 'app/order_form.html'
    success_url = reverse_lazy('order_list')

class OrderUpdateView(UpdateView):    
    model = Order
    form_class = OrderForm
    template_name = 'app/order_form.html'
    success_url = reverse_lazy('order_list')

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'app/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

class OrderDetailView(DetailView):
    model = Order
    template_name = 'app/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.object.orderitem_set.all()
        context['products'] = Product.objects.all()
        print(context['order_items'].values())
        return context
    
#############
#  Order Item
    ######

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


##########################
#       Ordercreation    #
##########################
class CreateOrderView(View):
    def get(self, request):
        order_form = OrderForm()
        OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=1, can_delete=True)
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())
        return render(request, 'app/create_order.html', {'order_form': order_form, 'formset': formset})

    def post(self, request):
        order_form = OrderForm(request.POST)
        print(request.POST)
        OrderItemFormSet = modelformset_factory(OrderItem, form=OrderItemForm, extra=0, can_delete=True)
        formset = OrderItemFormSet(request.POST)

        if order_form.is_valid() and formset.is_valid():
            # Save the Order
            order = order_form.save()

            # Save each OrderItem
            for form in formset:
                order_item = form.save(commit=False)
                order_item.order = order
                order_item.save()

            return redirect('product_list')  # Redirect to a success page or the order list

        return render(request, 'app/create_order.html', {'order_form': order_form, 'formset': formset})
