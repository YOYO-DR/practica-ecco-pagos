from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from apps.store.forms import ReviewForm
from .models import Product, ProductGallery, ReviewRating
from apps.category.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages
from apps.orders.models import OrderProduct
# Create your views here.

class StoreView(TemplateView):
    template_name='store/store.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category_slug'): #obtengo el slug de la categoria
            categories = get_object_or_404(Category,slug=self.kwargs.get('category_slug')) #obtengo la categoria y si no existe, retorno un 404 not found

            products = Product.objects.filter(is_available=True,category=categories).order_by('id')# obtengo los productos disponibles y que sean de la categoria buscada
        else:
            products = Product.objects.filter(is_available=True).order_by('id') #traigo todas las categorias
            
        paginator = Paginator(products, 6) # creo el paginador, le paso el query, y la cantidad en la cual quiero dividirlos
        page = self.request.GET.get('page') # obtengo el numero de la pagina a accedes
        context['products']=paginator.get_page(page) # le paso los productos, el cual cuando lo recorra, accedere a los productos normalmente, pero el "products" contendra toda la informacion del paginador para poder utilizarlo

        context["product_count"] = products.count() # le paso la cantidad de productos encontrados
        return context

class ProductDetailView(TemplateView):
  template_name = 'store/product_detail.html'

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      if self.kwargs.get('product_slug'):
          single_product=get_object_or_404(Product,category__slug=self.kwargs.get('category_slug'),slug=self.kwargs.get('product_slug'))

          in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(self.request),product=single_product).exists()
          if self.request.user.is_authenticated:
            orderproduct=OrderProduct.objects.filter(user=self.request.user,product_id=single_product.id).exists()
            if not orderproduct:
              orderproduct=None
          else:
              orderproduct=None
          
          reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)

          product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

          context["single_product"] = single_product
          context["in_cart"] = in_cart
          context["orderproduct"] = orderproduct
          context["reviews"] = reviews
          context["product_gallery"] = product_gallery
      return context
  
class SearchView(TemplateView):
    template_name = 'store/store.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.GET.get('keyword'):
          return redirect('store')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            if keyword:
                products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)).order_by('-created_date')
                
      
        context["products"] = products
        context["product_count"] = products.count()

        return context
    
def submit_review(request,product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews=ReviewRating.objects.get(user_id=request.user.id,product_id=product_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request, "Muchas gracias!, tu comentario ha sido actualizado")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data["subject"]
                data.rating=form.cleaned_data["rating"]
                data.review=form.cleaned_data["review"]
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,"Muchas gracias, tu comentario fue enviado con exito!")
                return redirect(url)
