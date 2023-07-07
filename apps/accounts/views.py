import os
from django.shortcuts import get_object_or_404, redirect, render
from .models import Account, UserProfile
from apps.accounts.forms import RegistrationForm, UserForm, UserProfileForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from apps.orders.models import Order
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.views.generic import TemplateView

from apps.carts.views import _cart_id
from apps.carts.models import CartItem,Cart

import requests
# crear contraseña para aplicacion https://support.google.com/accounts/answer/185833?sjid=11686343906281568208-NA

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['email'].split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_number=phone_number
            user.save()

            # creo el userprofile al usuario cuando se registra
            profile=UserProfile()
            profile.user_id=user.id
            profile.save()

            #proceso para enviar un correo de verificacion
            current_site = get_current_site(request) # url del sitio, puede ser el localhost o donde lo tenga desplegado
            # verifico si estoy en desarrollo o produccion
            if 'WEBSITE_HOSTNAME' in os.environ:
                current_site = 'https://'+str(current_site)
            else:
                current_site = 'http://'+str(current_site)
            mail_subject = "Por favor activa tu cuenta en Yoyo DR" # asunto o titulo
            body = render_to_string('account/account_verification_email.html',{ # creo el html que va a ir en el mensaje
                # son parametors que iran en el mensaje
                'user':user, # usuario
                'domain':current_site, # el dominio
                # codificar el id del usuario por seguridad
                'uid':urlsafe_base64_encode(force_bytes(user.pk)), # codifico el id sel usuario
                'token':default_token_generator.make_token(user) # y tambien un token segun el usuario
            })
            to_email=email
            send_email = EmailMessage(mail_subject,body,to=[to_email])
            send_email.send()
            #messages.success(request,'Se registro el usuario exitosamente')
            return redirect('/accounts/login/?command=verification&email='+email)
    context = {
        'form': form,
    }
    return render(request,'account/register.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
              cart = Cart.objects.get(cart_id=_cart_id(request))
              is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
              if is_cart_item_exists:
                cart_item = CartItem.objects.filter(cart=cart)

                #obtengo las variantes que tiene el producto
                product_variation=[]
                for item in cart_item:
                    variation = item.variations.all()
                    #le paso la variacion del producto del carrito actual, y que cantidad lleva
                    product_variation.append([list(variation),item.quantity])
                
                #obtengo los cartitems que tenga el usuario
                cart_item = CartItem.objects.filter(user=user)
                ex_var_list=[]
                id=[]
                #obtengo en un arreglo las variantes de los cart item que tenga los cartitem del usuario
                for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)
                
                # product_variation [1,2,3,4,5]
                # ex_var_list [5,6,7,8]

                #recorreo las variantes del producto
                for pr in product_variation:
                    # rpegunto si esa variante esta en la lista de las variantes de los cartitem existentes del usuario
                    if pr[0] in ex_var_list:
                        #obtengo el id del item
                        index=ex_var_list.index(pr[0])
                        item_id=id[index]
                        #busco el item con su id
                        item=CartItem.objects.get(id=item_id)
                        # le sumo 1 al cuantity, le asigno el usuairo y guardo
                        item.quantity+=pr[1] #le simo la cantidad que tiene en el carrito en la sesion anonima
                        item.user=user
                        item.save()
                    #si no esta en los existentes, entonces traigo los cartitem que pertenezcan a la sesion actual o cart, y le asigno el usuario nomas, y guardo
                    else:
                        cart_item=CartItem.objects.filter(cart=cart)
                        for item in cart_item:
                            item.user=user
                            item.save()
            except Exception as e:
                print(str(e))
            #http://127.0.0.1:8000/accounts/login/?next=/cart/checkout/
            
            auth.login(request,user)
            messages.success(request,'Has iniciado sesion exitosamente')

            url = request.META.get('HTTP_REFERER') #capturar la url http://127.0.0.1:8000/accounts/login/?next=/cart/checkout/
            try:
                query = requests.utils.urlparse(url).query # obtengo los parametros, por ejemplo el next
                params={x.split('=')[0]:x.split('=')[1] for x in query.split('&')}
                if 'next' in params:
                    nextPage=params['next']
                    return redirect(nextPage)
            except:
                # si no encuentra el next
                return redirect('dashboard')

        else:
            messages.error(request,'Las credenciales son incorrectas')
    return render(request,'account/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Has salido de sesión')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        #obtener el id del usuario decodificando el valor
        uid = urlsafe_base64_decode(uidb64).decode()
        # obtengo el usuario de esta forma
        user = Account._default_manager.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist): # por si sale algun error de estos
        user = None
    
    if user is not None and default_token_generator.check_token(user, token): # verificar si existe el usuario y si el token es correcto
      user.is_active = True # activo el usuario
      user.save() # guardo el valor
      messages.success(request,'Felicidades, tu cuenta esta activada')
      return redirect('login')
    else:
        messages.error(request,'La activación es invalida')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    orders=Order.objects.filter(user_id=request.user.id,is_ordered=True).order_by('-created_at')
    orders_count=orders.count()
    context = {
        'orders_count':orders_count
    }
    return render(request, 'account/dashboard.html',context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #enviar correo
            current_site = get_current_site(request)
            if 'WEBSITE_HOSTNAME' in os.environ:
                current_site = 'https://'+str(current_site)
            else:
                current_site = 'http://'+str(current_site)
            mail_subject = 'Resetear password'
            body = render_to_string('account/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email=EmailMessage(mail_subject, body,to=[to_email])
            send_email.send()

            messages.success(request,'Un email fue enviado a tu bandeja de entrada para resetear tu password')
            return redirect('login')
        # si no eixte ese usuario
        else:
            messages.error(request,'La cuenta de usuario no existe')
            return redirect('forgotPassword')
    return render(request, 'account/forgotPassword.html')

def resetPassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Por favor resetea tu password')
        return redirect('resetPassword')
    # si ya expiro el token
    else:
        messages.success(request,'El link ha expirado')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(password) # cambiar contraseña
            user.save()
            messages.success(request,'El password se reseteo correctamente')
            return redirect('login')
        else:
            messages.success(request,'El password de confirmación no concuerda')
            return redirect('resetPassword')
    else:
        return render(request, 'account/resetPassword.html')

def my_orders(request):
    orders=Order.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders': orders
    }
    return render(request,'account/my_orders.html', context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Su informacion fue guardada con exito')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
    }
    return render(request,'account/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user=Account.objects.get(username__exact=request.user.username)
        if new_password==confirm_password:
            success=user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                auth.login(request,user)

                messages.success(request,"La contraseña se actualizo exitosamente")
                return redirect('change_password')
            else:
                messages.error(request,"Porfavor ingrese un password valido")
                return redirect('change_password')
        else:
            messages.error(request,"La contraseña no coincide con la confirmación de la contraseña")
            return redirect('change_password')
    return render(request, 'account/change_password.html')