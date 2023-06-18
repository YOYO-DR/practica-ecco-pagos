from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from .models import Cart, CartItem
from apps.store.models import Product
# Create your views here.

def _cart_id(request): # para generar el codigo del carrito con la key de la sesion del usuario
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# esta vista es para crear el cartItem
class AddCart(View):
    def get(self, request, *args, **kwargs):
      # obtengo el producto
      product = Product.objects.get(id=self.kwargs.get('product_id'))
      
      # creo u obtengo el carrito del usuario, si si se crea, utiliza la funcion de cart_id, y tiene un "_" al inicio pq sera una funcion solo para este archivo
      cart,creado = Cart.objects.get_or_create(cart_id=_cart_id(request))

      # creo u obtengo el cart_item, le paso el producto, el carrito y el quantity en 1 por si se crea
      cart_item,creado = CartItem.objects.get_or_create(product=product,cart=cart,quantity=1)

      #si no se crea, osea, se obtiene, le sumo 1 al quantity y lo guardo
      if not creado:
          cart_item.quantity+=1
          cart_item.save()

      # lo redirecciono al carrito
      return redirect('cart')
      
    

class CartView(TemplateView):
    template_name = 'store/cart.html'