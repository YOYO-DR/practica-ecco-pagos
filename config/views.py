from django.shortcuts import render
from apps.store.models import Product, ReviewRating
from django.views.generic import TemplateView

class HomeView(TemplateView):
  template_name = 'home.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      products=Product.objects.all().filter(is_available=True).order_by('-created_date')
      for product in products:
         reviews= ReviewRating.objects.filter(product_id=product.id,status=True)
      
      context["reviews"] = reviews
      context["products"] = products
      return context
