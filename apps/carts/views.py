from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .models import Cart, CartItem
from apps.store.models import Product, Variation
# Create your views here.

def _cart_id(request): # para generar el codigo del carrito con la key de la sesion del usuario
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# esta vista es para crear el cartItem
def addCart(request,product_id):
      # obtengo el producto
      product = Product.objects.get(id=product_id)
      product_variation = []
      if request.method=='POST':
        for item in request.POST:
          if item=='csrfmiddlewaretoken':
            continue
          key = item
          value = request.POST[key]
          variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)

          product_variation.append(variation)
      # creo u obtengo el carrito del usuario, si si se crea, utiliza la funcion de cart_id, y tiene un "_" al inicio pq sera una funcion solo para este archivo
      cart,creado = Cart.objects.get_or_create(cart_id=_cart_id(request))

      # creo u obtengo el cart_item, le paso el producto, el carrito y el quantity en 1 por si se crea
      cart_item,creado = CartItem.objects.get_or_create(product=product,cart=cart)
      
      if len(product_variation)>0:
          #limpie los valores que tenga el cart_item
          cart_item.variations.clear()
          for item in product_variation:
              # como es de muchos a muchos, y puede recibir varios valores, se lo agrego asi, llamo al atributo que lo relaciona y con la funcion add le paso el item o variation
              cart_item.variations.add(item) 

      #si no se crea, osea, se obtiene, le sumo 1 al quantity y lo guardo
      if not creado:
          cart_item.quantity+=1
          cart_item.save()

      # lo redirecciono al carrito
      return redirect('cart')
      
class DeleteCart(View):
    def get(self, request, *args, **kwargs):
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(Product, id=self.kwargs.get('product_id'))
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        # lo redirecciono al carrito
        return redirect('cart')

class DeleteCartItem(View):
    def get(self, request, *args, **kwargs):
        cart=Cart.objects.get(cart_id=_cart_id(request))
        product=get_object_or_404(Product, id=self.kwargs.get('product_id'))
        cart_item=CartItem.objects.get(product=product,cart=cart)
        cart_item.delete()

        # lo redirecciono al carrito
        return redirect('cart')

class CartView(TemplateView):
    template_name = 'store/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cart = Cart.objects.get(cart_id=_cart_id(self.request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        total=0
        quantity=0
        for cart_item in cart_items:
            total+=cart_item.product.price * cart_item.quantity
            quantity +=cart_item.quantity

        context["total"] = total
        context["quantity"] = quantity
        context["cart_items"] = cart_items
        context["tax"] = (2*total)/100
        context["grand_total"] = context["tax"]+total

        return context
    
