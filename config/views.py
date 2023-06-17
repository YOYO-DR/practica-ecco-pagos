from django.shortcuts import render
from apps.store.models import Product
from django.views.generic import TemplateView

class HomeView(TemplateView):
  template_name = 'home.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      products=Product.objects.all().filter(is_available=True)
      context["products"] = products
      return context
