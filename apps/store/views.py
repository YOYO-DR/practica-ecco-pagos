from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from apps.carts.models import CartItem
from apps.carts.views import _cart_id
from .models import Product
from apps.category.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator
# Create your views here.

class StoreView(TemplateView):
    template_name='store/store.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('category_slug'): #obtengo el slug de la categoria
            categories = get_object_or_404(Category,slug=self.kwargs.get('category_slug')) #obtengo la categoria y si no existe, retorno un 404 not found

            products = Product.objects.filter(is_available=True,category=categories)# obtengo los productos disponibles y que sean de la categoria buscada
        else:
            products = Product.objects.filter(is_available=True) #traigo todas las categorias
            
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

          context["single_product"] = single_product
          context["in_cart"] = in_cart
      return context
  