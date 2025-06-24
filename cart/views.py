from django.shortcuts import redirect, render
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from wishlist.models import Wishlist
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
# Create your views here.

# to view cart on userside
@login_required(login_url='signin')
def cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user).order_by('id')
        variants=cart.values_list('variant',flat=True)
        cart_count=Cart.objects.filter(user=request.user).count()
        img =VariantImage.objects.filter(variant__in=variants).distinct()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        
        total_price = 0
        tax = 0
        grand_total =0
        single_product_total = 0
        offer_total_price =0
        single_total_offer=0
        
        for item in cart:
            if item.variant.product.category.offer:  
                total_price=total_price+item.variant.product.product_price*item.product_qty
                single_product_total+item.variant.product.product_price*item.product_qty    
                offer_total_price = offer_total_price + item.variant.product.category.offer.discount_amount * item.product_qty
                single_total_offer =single_total_offer+item.variant.product.category.offer.discount_amount * item.product_qty
                
            else:    
                total_price = total_price + item.variant.product.product_price * item.product_qty
                single_product_total+item.variant.product.product_price * item.product_qty
                
        single_product_total =single_product_total-single_total_offer
        total_price=total_price-offer_total_price
        grand_total = total_price 
        
        context={
            'cart':cart,
            'total_price':total_price,
            'tax':tax,
            'grand_total':grand_total,
            'single_product_total':single_product_total,
            'img':img,
            'cart_count':cart_count,
            'wishlist_count':wishlist_count,
        }
        return render(request,'user/cart/cart.html',context)
    else:
        return render(request,'user/cart/cart.html')
    
    
# to remove product from cart on userside 
@login_required(login_url='signin')
def removecart(request,cart_id):
    try:
        cart_remove=Cart.objects.get(id=cart_id)
        cart_remove.delete()
        messages.success(request,'deleted successfully')
    except:
        return redirect('cart')
    
    return redirect('cart')
        
  
# to add product into cart on userside
def addcart(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_qty =int(request.POST.get('add_qty'))
            add_size =request.POST.get('add_size')
            try:
                variant_check =Variant.objects.get(id=variant_id )
                if variant_check.size==add_size:
                    pass
                else:
                    product=variant_check.product
                    color= variant_check.color
                    try:
                        check_variant=Variant.objects.get(product=product, color=color, size=add_size)
                        variant_check =check_variant
                        variant_id= variant_check.id
                    except Variant.DoesNotExist:
                        return JsonResponse({'status': 'Sorry! this variant not available'})  
                        
            except Variant.DoesNotExist:
                return JsonResponse({'status': 'No such prodcut found'})
              
            if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in cart'})
            
        
            else:
                variant_qty = add_qty
                
                if variant_check.quantity >= variant_qty:
                    
                    if variant_check.product.category.offer:
                        product_offer =variant_qty*variant_check.product.category.offer.discount_amount
                        total = variant_qty*variant_check.product.product_price
                        total = total - product_offer
                    else:
                        total = variant_qty * variant_check.product.product_price

                    Cart.objects.create(user=request.user, variant_id=variant_id, product_qty=variant_qty, single_total=total)
                    return JsonResponse({'status': 'Product added successfully'})

                else:
                    return JsonResponse({'status': "Only few quantity available"})
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
    return redirect('home')    
        
            
    
            
# to update cart after removing or adding product including offer price 
@login_required(login_url='user_login1')
def updatecart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        if (Cart.objects.filter(user=request.user, id=cart_id)):
            prod_qty =int (request.POST.get('product_qty'))
           
            cart = Cart.objects.get(id=cart_id, user=request.user)
            cartes = cart.variant.quantity
            if int(cartes) >= int(prod_qty)  :
                
                cart.product_qty = prod_qty
                cart.variant.product.offer

                if cart.variant.product.category.offer:
                    offer_discount = cart.variant.product.category.offer.discount_amount
                    single = prod_qty * (cart.variant.product.product_price - offer_discount)
                else:
                    single = prod_qty * cart.variant.product.product_price

                cart.single_total = single
           
                cart.save()

                carts = Cart.objects.filter(user = request.user).order_by('id')
                total_price = 0
                offer_price = 0
                for item in carts:
                    product_price = item.variant.product.product_price
                    product_qty = item.product_qty

                    if item.variant.product.category.offer:
                        offer_discount = item.variant.product.category.offer.discount_amount
                        total_price += (product_price - offer_discount) * product_qty
                    else:
                        total_price += product_price * product_qty
    
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'single':single, 'product_price':cart.variant.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False) 