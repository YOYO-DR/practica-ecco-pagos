from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from .models import Product
from apps.category.models import Category
# Create your views here.

class StoreView(TemplateView):
    template_name='store/store.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category_slug'):
            categories = get_object_or_404(Category,slug=self.kwargs.get('category_slug'))
            context["products"] = Product.objects.filter(is_available=True,category=categories)
        else:
            context["products"] = Product.objects.filter(is_available=True)
        context["product_count"] = context["products"].count()
        return context

class ProductDetailView(TemplateView):
  template_name = 'store/product_detail.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      if self.kwargs.get('product_slug'):
          single_product=get_object_or_404(Product,category__slug=self.kwargs.get('category_slug'),slug=self.kwargs.get('product_slug'))

          in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request),product=single_product).exists()

          context["single_product"] = single_product
          context["in_cart"] = in_cart
      return context
  