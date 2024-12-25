from django.urls import path, include
from .views import OrderListView,OderBill

urlpatterns = [
    path('orderslist/',OrderListView.as_view(),name='orders_list'),
    path('ordersbill/<int:pk>',OderBill,name='orders_bill'),
]