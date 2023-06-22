import os
from django.shortcuts import redirect, render
from .models import Account
from apps.accounts.forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage

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
            auth.login(request,user)
            messages.success(request,'Has iniciado sesion exitosamente')
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
    return render(request, 'account/dashboard.html')

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
