from django.shortcuts import redirect, render
from .models import Account
from apps.accounts.forms import RegistrationForm
from django.contrib import messages


def register(request):
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
            messages.success(request,'Se registro el usuario exitosamente')
            return redirect('register')
    context = {
        'form': form,
    }
    return render(request,'account/register.html',context)

def login(request):
    return render(request,'account/login.html')

def logout(request):
    return