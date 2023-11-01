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
            
            print(check_coupons,'xxxxxxxxxxxxxxxxx')
            
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
                print('555555555555555')
                print(check_coupons.min_price,grand_total,'4444444444444444444444444')
                coupon=check_coupons.coupon_discount_amount
                coupon_id=check_coupons.id
                
                print(coupon,'chooooooooooooooooo')
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
            print(all_offer,'yyyyyyyyyyyyyyyyyy')
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

def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user
        user = request.user
        
        # Retrieve the address ID from the form data
        coupon = request.POST.get('couponOrder')
        # print(coupon,'suiiiiiiiiiiiiiiiiii')
        address_id = request.POST.get('address')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)

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
       
       # Generate the PDF invoice
        pdf_buffer = generate_pdf_invoice(neworder)     
       
        # Send the invoice as an email attachment
        subject = 'Invoice for Your Order'
        message = 'Thank you for your order!'
        from_email = 'hamzashamnad123@gmail.com'
        recipient_list = [user.email]  # Assuming user has an email field
        
        # Create the HTML email message
        html_message = """
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                }}
                .invoice {{
                    border: 1px solid #ccc;
                    padding: 20px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    text-align: center;
                }}
                .company-name {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                }}
                .invoice-details {{
                    margin-top: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                table, th, td {{
                    border: 1px solid #ccc;
                }}
                th, td {{
                    padding: 10px;
                    text-align: left;
                }}
                .total {{
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="invoice">
                <div class="header">
                    <div class="company-name">Your Company Name</div>
                    <div>Invoice</div>
                </div>
                <div class="invoice-details">
                    <table>
                        <tr>
                            <th>Order ID</th>
                            <td>{order_id}</td>
                        </tr>
                        <tr>
                            <th>Tracking Number</th>
                            <td>{tracking_number}</td>
                        </tr>
                        <tr>
                            <th>Order Date</th>
                            <td>{order_date}</td>
                        </tr>
                        <tr>
                            <th>Payment Method</th>
                            <td>{payment_method}</td>
                        </tr>
                        <tr>
                            <th>Total Price</th>
                            <td>{total_price}</td>
                        </tr>
                        <tr>
                            <th>Offer Price</th>
                            <td>{offer_price}</td>
                        </tr>
                    </table>
                </div>
                <div class="total">
                    <p><strong>Total Price:</strong> ${total_price}</p>
                </div>
            </div>
        </body>
        </html>
        """.format(
            order_id=neworder.id,
            tracking_number=neworder.tracking_no,
            order_date=neworder.created_at.date(),
            payment_method=neworder.payment_mode,
            total_price=neworder.total_price,
            offer_price=neworder.coupon.coupon_discount_amount if neworder.coupon else "N/A"
        )

        email = EmailMessage(subject, '', from_email, recipient_list)
        email.attach('invoice.pdf', pdf_buffer.read(), 'application/pdf')
        email.content_subtype = "html"
        email.body = html_message
        email.send()
        
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
            
            return JsonResponse({'status': "Your order has been placed successfully check your Mail for Invoice"})
    
    return redirect('checkout')




def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


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