from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect
from .models import *
from SHOES.forms import * 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from USER.models import Profile



@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'Homepage/cart.html', {'cart': cart})

@login_required
def delete_cartitem(request, id):
    item = get_object_or_404(CartItem,id = id )
    if  request.user:
        item.delete()
        messages.success(request, 'The item has been deleted from your Cart')
    return redirect('cart-view')


@login_required
def confirm_checkout(request):
    
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return redirect('cart-view')

    total_price = sum(float(item.shoe.price) for item in cart.items.all())
    discount = 0
    shipping_fee = 0

   
    profile = Profile.objects.get(user=request.user)
    if not profile.city.filter(name='Hồ Chí Minh').exists():
     shipping_fee = 5
    else:
     shipping_fee = 0

    
    voucher_code = request.POST.get('voucher_code', '')

    if voucher_code:
        try:
            voucher = Voucher.objects.get(code=voucher_code)
            if voucher.is_valid():
                discount = round(float(total_price * (voucher.discount_percentage / 100)), 1)
                total_price -= discount
                request.session['discount'] = discount
            else:
                messages.error(request, "Voucher is invalid or expired.")
        except Voucher.DoesNotExist:
            messages.error(request, "Voucher does not exist.")
    
    # Cộng thêm phí ship vào tổng giá
    total_price += shipping_fee

    context = {
        'cart': cart,
        'total_price': total_price,
        'profile': profile,
        'discount': discount,
        'shipping_fee': shipping_fee,
    }

    return render(request, 'HomePage/confirm_info.html', context)




@login_required
def complete_transaction(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        return redirect('cart-view')

    order = Order.objects.create(user=request.user, total_price=0)
    
    total_price = 0
    for item in cart.items.all():
        order_item = OrderItem.objects.create(
            order=order,
            shoe=item.shoe,
            size=item.size,
        )
        total_price += float(item.shoe.price)
    
    discount = request.session.get('discount', 0)
    total_price -= discount

    
    shipping_fee = 0
    profile = Profile.objects.get(user=request.user)
    if not profile.city.filter(name='Hồ Chí Minh').exists():
     shipping_fee = 5
    else:
     shipping_fee = 0

    
    total_price += shipping_fee

    order.total_price = total_price
    order.save()
    cart.items.all().delete()

    if 'discount' in request.session:
        del request.session['discount']
    messages.success(request, 'You have placed your order successfully')
    return redirect('order-history')



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at') 
    context = {
        'orders': orders,
    }
    return render(request, 'Homepage/order_history.html', context)



