import datetime
from django.shortcuts import redirect, render
from apps.carts.models import Cart, CartItem
from apps.orders.models import Order
from .forms import OrderForm
def place_order(request):
    current_user=request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax=0
    total=0
    quantity=0
    for cart_item in cart_items:
        total+=cart_item.product.price * cart_item.quantity
        quantity+=cart_item.quantity
    
    tax =(2*total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form= OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.addres_line_1=form.cleaned_data['addres_line_1']
            data.addres_line_2=form.cleaned_data['addres_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax = tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d=datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            #20230625
            order_number = current_date + str(data.id)
            data.order_number=order_number
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')

