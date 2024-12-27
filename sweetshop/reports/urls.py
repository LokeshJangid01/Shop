from django.urls import path, include
from .views import OrderListView,OderBill,reportlabview,reportlabtableview

urlpatterns = [
    path('orderslist/',OrderListView.as_view(),name='orders_list'),
    path('ordersbill/<int:pk>',OderBill,name='orders_bill'),
    path('reportlab/<int:pk>',reportlabtableview,name='reportlab'),
]