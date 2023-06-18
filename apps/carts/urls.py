from django.urls import path
from .views import CartView,AddCart
urlpatterns = [
  path('',CartView.as_view(),name='cart'),
  path('add_cart/<int:product_id>/',AddCart.as_view(),name='add_cart')
]
