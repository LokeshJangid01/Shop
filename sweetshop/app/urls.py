from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ProductListView,ProductCreateView,ProductUpdateView,ProductDeleteView,
                    OrderListView,OrderCreateView, OrderUpdateView,OrderDeleteView, OrderDetailView,
                    OrderItemViewSet)


# Create a router and register viewsets
router = DefaultRouter()
router.register(r'orderitem', OrderItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('products/',ProductListView.as_view(),name='product_list'),
    path('product/add',ProductCreateView.as_view(),name='product_create'),
    path('product/<int:pk>/edit',ProductUpdateView.as_view(),name='product_update'),
    path('product/<int:pk>/delete',ProductDeleteView.as_view(),name='product_delete'),
    # path('create-order/', CreateOrderView.as_view(), name='create_order'),
    path('orders/',OrderListView.as_view(),name='order_list'),
    path('orders/add',OrderCreateView.as_view(),name='order_create'),
    path('orders/<int:pk>/edit',OrderUpdateView.as_view(),name='order_update'),
    path('orders/<int:pk>/delete',OrderDeleteView.as_view(),name='order_delete'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]