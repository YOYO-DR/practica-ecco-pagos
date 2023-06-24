from django.shortcuts import get_object_or_404, redirect,render
from django.views.generic import TemplateView, View
from .models import Cart, CartItem
from apps.store.models import Product, Variation
from django.utils.decorators import method_decorator # para la vista en el dispatch
from django.contrib.auth.decorators import login_required
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

      current_user = request.user
      if current_user.is_authenticated:
          # aqui en este bloque agregaremos la logica del carrito de compras cuando el usuario esta autenticado
          # para obtener las variantes del cartitem
        product_variation = []
        if request.method=='POST':
          for item in request.POST:
            if item=='csrfmiddlewaretoken':
              continue
            key = item
            value = request.POST[key]
            variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)

            #lo agrego a la lista
            product_variation.append(variation)
        # pregunto si el cartitem existe y lo obtengo
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
          # obtengo todos los cartItems con ese producto y ese cart
          cart_item = CartItem.objects.filter(product=product,user=current_user)

          ex_var_list = []
          id = []
          # recorreo cada cartitem
          for item in cart_item:
              # obtengo las variantes de ese cartitem
              existing_variation = item.variations.all()
              # guardo como un arreglo esas variantes en el arreglo ex_var_list
              ex_var_list.append(list(existing_variation))
              # guardo el id del cartitem
              id.append(item.id)
          
          # pregunto si las variantes de ese carrito estan en algun acartitem existente, como el product_variation es un arreglo con las variantes, pregunto si ese arreglo esta dentro de los arreglos que estan dentro de ex_var_list el cual son las combinaciones del cartitem de ese producto
          if product_variation in ex_var_list:
              #obtengo el index de esa variante existente, porque se guardaron conjuntamente con el id del item
              index = ex_var_list.index(product_variation)
              # obtengo el id del item de esa variante por el index en el ex_var_list
              item_id = id[index]
              #obtengo el cartitem expecifico
              item = CartItem.objects.get(product=product,id=item_id)
              # si existe, obtengo el cartitem y solo le sumo 1
              item.quantity+=1
              item.save()
          else:
              # si no existe, creo el cartitem y le agrego las variantes que se mandaron
              item = CartItem.objects.create(product=product,user=current_user)
              if len(product_variation)>0:
              #limpie los valores que tenga el cart_item
                item.variations.clear()
                # como ya las tengo en una lista, puedo solamente pasarlo con un * para desempaquetar la lista, y no hacer un for
                item.variations.add(*product_variation)
                # for item in product_variation:
                # como es de muchos a muchos, y puede recibir varios valores, se lo agrego asi, llamo al atributo que lo relaciona y con la funcion add le paso el item o variation
                  # item.variations.add(item)
              item.save()
        else:
            # si no existe un cartitem con ese producto, entonces lo creo y le paso las variantes
            cart_item = CartItem.objects.create(
                product=product,
                user=current_user,
            )
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

            cart_item.save()
      #si no se crea, osea, se obtiene, le sumo 1 al quantity y lo guardo
      # if not creado:
          # cart_item.quantity+=1
          # cart_item.save()

      # lo redirecciono al carrito
        return redirect('cart')
      else:

        # para obtener las variantes del cartitem
        product_variation = []
        if request.method=='POST':
          for item in request.POST:
            if item=='csrfmiddlewaretoken':
              continue
            key = item
            value = request.POST[key]
            variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)

            #lo agrego a la lista
            product_variation.append(variation)
        # creo u obtengo el carrito del usuario, si si se crea, utiliza la funcion de cart_id, y tiene un "_" al inicio pq sera una funcion solo para este archivo
        cart,creado = Cart.objects.get_or_create(cart_id=_cart_id(request))

        # pregunto si el cartitem existe y lo obtengo
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
          # obtengo todos los cartItems con ese producto y ese cart
          cart_item = CartItem.objects.filter(product=product,cart=cart)

          ex_var_list = []
          id = []
          # recorreo cada cartitem
          for item in cart_item:
              # obtengo las variantes de ese cartitem
              existing_variation = item.variations.all()
              # guardo como un arreglo esas variantes en el arreglo ex_var_list
              ex_var_list.append(list(existing_variation))
              # guardo el id del cartitem
              id.append(item.id)
          
          # pregunto si las variantes de ese carrito estan en algun acartitem existente, como el product_variation es un arreglo con las variantes, pregunto si ese arreglo esta dentro de los arreglos que estan dentro de ex_var_list el cual son las combinaciones del cartitem de ese producto
          if product_variation in ex_var_list:
              #obtengo el index de esa variante existente, porque se guardaron conjuntamente con el id del item
              index = ex_var_list.index(product_variation)
              # obtengo el id del item de esa variante por el index en el ex_var_list
              item_id = id[index]
              #obtengo el cartitem expecifico
              item = CartItem.objects.get(product=product,id=item_id)
              # si existe, obtengo el cartitem y solo le sumo 1
              item.quantity+=1
              item.save()
          else:
              # si no existe, creo el cartitem y le agrego las variantes que se mandaron
              item = CartItem.objects.create(product=product,cart=cart)
              if len(product_variation)>0:
              #limpie los valores que tenga el cart_item
                item.variations.clear()
                # como ya las tengo en una lista, puedo solamente pasarlo con un * para desempaquetar la lista, y no hacer un for
                item.variations.add(*product_variation)
                # for item in product_variation:
                # como es de muchos a muchos, y puede recibir varios valores, se lo agrego asi, llamo al atributo que lo relaciona y con la funcion add le paso el item o variation
                  # item.variations.add(item)
              item.save()
        else:
            # si no existe un cartitem con ese producto, entonces lo creo y le paso las variantes
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
            )
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

            cart_item.save()
      #si no se crea, osea, se obtiene, le sumo 1 al quantity y lo guardo
      # if not creado:
          # cart_item.quantity+=1
          # cart_item.save()

      # lo redirecciono al carrito
        return redirect('cart')
      
class DeleteCart(View):
    def get(self, request, *args, **kwargs):
        product=get_object_or_404(Product, id=self.kwargs.get('product_id'))
        cart_item_id=self.kwargs.get('cart_item_id')
        try:
          if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
          else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
          
          if cart_item.quantity > 1:
              cart_item.quantity -= 1
              cart_item.save()
          else:
              cart_item.delete()
        except:
            pass
          # lo redirecciono al carrito
        return redirect('cart')

class DeleteCartItem(View):
    def get(self, request, *args, **kwargs):
        cart_item_id=self.kwargs.get('cart_item_id')
        product=get_object_or_404(Product, id=self.kwargs.get('product_id'))
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
          cart=Cart.objects.get(cart_id=_cart_id(request))
          cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        cart_item.delete()

        # lo redirecciono al carrito
        return redirect('cart')

def cart(request,total=0,quantity=0,cart_items=None):
    context={}
    try: 
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
          cart = Cart.objects.get(cart_id=_cart_id(request))
          cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
          total+=cart_item.product.price * cart_item.quantity
          quantity +=cart_item.quantity
    except:
        pass
    context["total"] = total
    context["quantity"] = quantity
    context["cart_items"] = cart_items
    context["tax"] = (2*total)/100
    context["grand_total"] = context["tax"]+total
    return render(request,'store/cart.html',context)

#@login_required(login_url='login')
class CheckoutView(TemplateView):
    template_name = 'store/checkout.html'

    @method_decorator(login_required(login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=self.request.user,is_active=True)
        else:
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