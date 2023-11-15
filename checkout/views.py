from django.shortcuts import render,HttpResponse
import random
import string
from django.shortcuts import redirect, render
from coupon.models import Coupon
from wishlist.models import Wishlist
from .models import Order, OrderItem
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Address,Wallet
from django.contrib import messages
from django.core.mail import EmailMessage
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

# for checking out from cart
def checkout(request):
    request.session['coupon_session']=0
    request.session['coupon_id']= None
    
    if request.method == 'POST':
        coupon_name = request.POST.get('coupon')
        
        if not coupon_name:
            messages.error(request, 'coupon field is cannot empty!')
            return redirect('checkout')
        
        try:
            check_coupons =Coupon.objects.filter(coupon_code=coupon_name).first()
            cartitems = Cart.objects.filter(user=request.user)
    
            total_price = 0
            offer_price = 0
            offer_price_total=0
            all_offer =0
            
            for item in cartitems:
                
                if item.variant.product.category.offer:
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    offer_price = item.variant.product.category.offer.discount_amount
                    offer_price_total =offer_price*item.product_qty
                    total_price= total_price - offer_price_total
                    all_offer= all_offer+offer_price_total
                else:     
                    product_price = item.variant.product.product_price
                    total_price += product_price * item.product_qty
                    
            grand_total = total_price
            
            if grand_total>=check_coupons.min_price:
                coupon=check_coupons.coupon_discount_amount
                coupon_id=check_coupons.id
                request.session['coupon_session']= coupon
                request.session['coupon_id']= coupon_id
                messages.success(request, 'This coupon added successfully')
            else:
                coupon=False 
                messages.error(request, ' purchase minimum price')    
                
            address = Address.objects.filter(user= request.user,is_available=True)
            cart_count =Cart.objects.filter(user =request.user).count()
            wishlist_count =Wishlist.objects.filter(user=request.user).count()
            coupon_checkout =Coupon.objects.filter(is_available=True)
            
            if offer_price_total == 0:
                offer_price_total =False
            else:
                offer_price_total
            context = {
                'all_offer':all_offer,
                'offer' :offer_price_total,
                'coupon_checkout':coupon_checkout,
                'cartitems': cartitems,
                'total_price': total_price,
                'grand_total': grand_total,
                'address': address,
                'wishlist_count':wishlist_count,
                'cart_count' :cart_count,   
                'coupon':coupon
            }
            
            if total_price==0:
                return redirect('home')
            else:
                return render(request,'user/checkout.html',context) 
            
        except ObjectDoesNotExist:
            messages.error(request, 'This coupon not valid!')
            # change into checkout
            return redirect('checkout')
        
    cartitems = Cart.objects.filter(user=request.user)
    
    total_price = 0
    offer_price = 0
    offer_price_total=0
    all_offer= 0
    
    for item in cartitems:
        if item.variant.product.category.offer:
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
            offer_price = item.variant.product.category.offer.discount_amount
            offer_price_total =offer_price*item.product_qty
            total_price= total_price - offer_price_total
            all_offer= all_offer+offer_price_total
        else:     
            product_price = item.variant.product.product_price
            total_price += product_price * item.product_qty
    
    grand_total = total_price 

    address = Address.objects.filter(user= request.user,is_available=True)
    cart_count =Cart.objects.filter(user =request.user).count()
    wishlist_count =Wishlist.objects.filter(user=request.user).count()
    coupon_checkout =Coupon.objects.filter(is_available=True)
    coupon =False
    
    if offer_price_total == 0:
        offer_price_total =False
    else:
        offer_price_total

    context = {
        'all_offer':all_offer,
        'offer' :offer_price_total,
        'coupon_checkout':coupon_checkout,
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'address': address,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,  
        'coupon':coupon
    }
    
    if total_price==0:
       return redirect('home')
    else:
        return render(request,'user/checkout.html',context)


# to generate pdf invoice to user chat gpt
def generate_pdf_invoice(order):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    
    # Create the PDF content
    p.drawString(100, 750, f"Order ID: {order.id}")
    p.drawString(100, 730, f"Tracking Number: {order.tracking_no}")
    p.drawString(100, 710, "Invoice Details:")
    y = 690  # Vertical position for line items
    for item in order.orderitem_set.all():
        p.drawString(100, y, f"{item.variant.product.name} x {item.quantity}: ${item.price * item.quantity}")
        y -= 20
    p.drawString(100, y, f"Total Price: ${order.total_price}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer

# placing order after checkout 
def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        user = request.user
        
        # Retrieve the address ID from the form data
        coupon = request.POST.get('couponOrder')
        print(coupon,'couponnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)
        # coupons=Coupon.objects.get(coupon_discount_amount=coupon)

        # Create a new Order instance and set its attributes
        neworder = Order()
        neworder.address=address
        neworder.user = user
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.message = request.POST.get('order_note')
        session_coupon_id=request.session.get('coupon_id')
        if session_coupon_id!=None:
            session_coupons =Coupon.objects.get(id=session_coupon_id)
        else:
            session_coupons = None
               
        neworder.coupon = session_coupons
        
        # Calculate the cart total price 
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = 0
        offer_total_price = 0
        
        for item in cart_items:
            if item.variant.product.category.offer:
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty
                offer_total_price =item.variant.product.category.offer.discount_amount
                offer_total_price = offer_total_price*item.product_qty
                cart_total_price = cart_total_price - offer_total_price  
                
            else:    
                product_price = item.variant.product.product_price
                cart_total_price += product_price * item.product_qty
            
        session_coupon=request.session.get('coupon_session')
        cart_total_price = cart_total_price - session_coupon
        neworder.total_price = cart_total_price

        # Generate a unique tracking number
        track_no = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = random.randint(1111111, 9999999)
        neworder.tracking_no = track_no

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)

        neworder.save()
       
        # Create OrderItem instances for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty,   
            )

            # Decrease the product quantity from the available stock
            product = Variant.objects.filter(id=item.variant.id).first()
            product.quantity -= item.product_qty
            product.save()

        # Delete the cart items after the order is placed 
            cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod' or payment_mode == 'razorpay' :
            del request.session['coupon_session']
            del request.session['coupon_id']
            
            return JsonResponse({'status': "Your order has been placed successfully"})
        
            
    
    return redirect('checkout')



# generating payment id 
def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

# razarpay ui
def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    total_offer = 0
    for item in cart:
        if item.variant.product.category.offer:
            total_price = total_price + item.variant.product.product_price * item.product_qty
            total_offer = item.variant.product.category.offer.discount_amount*item.product_qty
            total_price = total_price-total_offer
        else:    
            total_price = total_price + item.variant.product.product_price * item.product_qty
    session_coupon=request.session.get('coupon_session')
    total_price = total_price - session_coupon  
    
         
    return JsonResponse({'total_price': total_price})