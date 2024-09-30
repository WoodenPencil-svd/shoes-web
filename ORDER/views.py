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


import paypalrestsdk

@login_required
def complete_transaction(request):
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        cart = Cart.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            return redirect('cart-view')

        # Kiểm tra phương thức thanh toán
        if payment_method == "paypal":
            return redirect('paypal_payment')  # Chuyển hướng đến PayPal
        
        # Xử lý cho các phương thức thanh toán khác (COD)
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

        # Xóa cart sau khi đặt hàng
        cart.items.all().delete()

        # Xóa session chứa thông tin giảm giá
        if 'discount' in request.session:
            del request.session['discount']
        
        messages.success(request, 'You have placed your order successfully')
        return redirect('order-history')

    return render(request, 'checkout.html')
def paypal_payment(request):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute",  
            "cancel_url": "http://localhost:8000/payment/cancel"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Shoe",
                    "sku": "001",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "This is the payment transaction description."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = link.href
                return redirect(approval_url)  # Chuyển hướng tới PayPal để thanh toán
    else:
        print(payment.error)
        return render(request, 'checkout/error.html', {"message": "Payment creation failed."})
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
    
    total_price += shipping_fee

    payment_method = request.POST.get('payment_method', 'cod')  # Nhận phương thức thanh toán

    context = {
        'cart': cart,
        'total_price': total_price,
        'profile': profile,
        'discount': discount,
        'shipping_fee': shipping_fee,
        'payment_method': payment_method  # Truyền vào template
    }

    return render(request, 'HomePage/confirm_info.html', context)

def paypal_cancel(request):
    messages.error(request, 'You have canceled your payment.')
    return redirect('cart-view')


import paypalrestsdk
from django.shortcuts import redirect, render
from django.contrib import messages

@login_required
def paypal_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        # Thanh toán thành công, tạo Order
        cart = Cart.objects.filter(user=request.user).first()
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

        messages.success(request, 'Payment successful and order created.')
        return redirect('order-history')
    else:
        print(payment.error)
        return render(request, 'checkout/error.html', {"message": "Payment execution failed."})



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at') 
    return render(request, 'Homepage/order_history.html',{'orders':orders})
