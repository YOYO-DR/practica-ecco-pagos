from django.urls import path
from .views import cart, DeleteCart, DeleteCartItem, addCart,CheckoutView
urlpatterns = [
  path('',cart,name='cart'),
  path('add_cart/<int:product_id>/',addCart,name='add_cart'),
  path('remove_cart/<int:product_id>/<int:cart_item_id>',DeleteCart.as_view(),name='remove_cart'),
  path('remove_cart_item/<int:product_id>//<int:cart_item_id>',DeleteCartItem.as_view(),name='remove_cart_item'),
  path('checkout/',CheckoutView.as_view(),name="checkout")
]
