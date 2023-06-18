from django.db import models
from apps.store.models import Product

class Cart(models.Model):
  cart_id = models.CharField(max_length=250, blank=True)
  date_added = models.DateField(auto_now_add=True)
  
  def __str__(self):
    return self.cart_id

class CartItem(models.Model):
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
  quantity = models.IntegerField(default=1)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.product.product_name

  def sub_total(self):
    return self.quantity*self.product.price