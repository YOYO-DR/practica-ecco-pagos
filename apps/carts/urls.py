from django.urls import path
from .views import CartView, DeleteCart, DeleteCartItem, addCart
urlpatterns = [
  path('',CartView.as_view(),name='cart'),
  path('add_cart/<int:product_id>/',addCart,name='add_cart'),
  path('remove_cart/<int:product_id>/',DeleteCart.as_view(),name='remove_cart'),
  path('remove_cart_item/<int:product_id>/',DeleteCartItem.as_view(),name='remove_cart_item'),
]
