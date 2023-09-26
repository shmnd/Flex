from django.shortcuts import redirect, render
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from wishlist.models import Wishlist
from .models import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
# Create your views here.

@login_required(login_url='signin')
def cart(request):
    # print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiilllllllllllllllllllllll')
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user).order_by('id')
        variants=cart.values_list('variant',flat=True)
        cart_count=Cart.objects.filter(user=request.user).count()
        img =VariantImage.objects.filter(variant__in=variants).distinct('variant')
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        
        total_price = 0
        tax = 0
        grand_total =0
        single_product_total = 0
        offer_total_price =0
        single_total_offer=0
        
        for item in cart:
            total_price=total_price+item.variant.product.product_price*item.product_qty
            # single_product_total+item.variant.product.product_price*item.product_qty
            
        grand_total = total_price 
        
        
        
        
        context={
            'cart':cart,
            'total_price':total_price,
            'grand_total':grand_total,
            'single_product_total':single_product_total,
            'img':img,
            'cart_count':cart_count,
            'wishlist_count':wishlist_count,
        }
        return render(request,'user/cart/cart.html',context)
    else:
        return render(request,'user/cart/cart.html')
    
    
    
@login_required(login_url='signin')
def removecart(request,cart_id):
    try:
        cart_remove=Cart.objects.get(id=cart_id)
        cart_remove.delete()
        messages.success(request,'deleted successfully')
    except:
        return redirect('cart')
    
    return redirect('cart')
        
        
        
        
        
        
        
        
# ///////////////////////////////////////

# @login_required(login_url='signin')    
# def addcart(request):
#     if request.user.is_authenticated:
#         variant_id = request.POST.get('variant_id')
#         add_qty = request.POST.get('add_qty')
#         add_size = request.POST.get('add_size')

#     if add_qty is not None and add_qty.isdigit():
#         add_qty = int(add_qty)  # Convert add_qty to an integer



# /////////////////////////////////////////////////////
# @login_required(login_url='signin')    
# def addcart(request):
#     if request.user.is_authenticated:
        
#         variant_id = request.POST.get('variant_id')
#         add_qty = request.POST.get('add_qty')

#         add_size = request.POST.get('add_size')
        
#         if add_qty is not None and add_qty.isdigit():
#                 add_qty = int(add_qty)

#                 add_size = request.POST.get('add_size')
        
#         try:
#             variant_check = Variant.objects.get(id=variant_id)
#             if variant_check.size == add_size:
#                 pass
#             else:
#                 product = variant_check.product
#                 color = variant_check.color
#                 try:
#                     check_variant = Variant.objects.get(product=product, color=color, size=add_size)
#                     variant_id = check_variant.id
#                 except Variant.DoesNotExist:
#                     return JsonResponse({'status': 'Sorry this variant not available'})
#         except Variant.DoesNotExist:
#             return JsonResponse({'status': 'No such product found'})
        
#         # Check if the product is already in the user's cart
#         if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
#             return JsonResponse({'status': 'Product already in cart'})
        
#         else:
#             variant_qty = add_qty.strip()  # Remove leading/trailing whitespace

#             if variant_qty.isdigit():  # Check if variant_qty is a valid integer
#                 variant_qty = int(variant_qty)
                
#                 if variant_check.quantity >= variant_qty:  
#                     total = variant_qty * variant_check.product.product_price
#                     Cart.objects.create(user=request.user, variant_id=variant_id, product_qty=variant_qty, singletotal=total)
#                     return JsonResponse({'status': 'Product added successfully'})
#                 else:
#                     return JsonResponse({'status': 'Not enough stock for this variant'})
#             else:
#                 # return redirect('cart')
        
#                 return JsonResponse({'status': 'You are not logged in. Please log in to continue'})
    
#     # The following line will not be reached because the function will have returned a JsonResponse before this point.
#     # If you want to redirect, place it inside the else block or remove it.
# ////////////////////////////////////////////////////////////////
def addcart(request):
    print('5555555555555555555555555555555')
    
    if request.method =='POST':
        if request.user.is_authenticated:
        
            print('hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
              
            variant_id = request.POST.get('variant_id')
            product_id = request.POST.get('product_id')
            
            product_qty =request.POST.get('product_qty')
            print(product_qty,'uuuuuuuuuuuuuuuuuuuuu')
            
            # add_size =request.POST.get('add_size')
            # product_id=request.POST.get('product_id')
            # color_name=request.POST.get('color_name')
            # product_price=request.POST.get('product_price')
            
            
                
            if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():
            
                messages.warning(request, 'Product already in cart') 
            
                return  redirect('productshow',product_id,variant_id)
            else:
                Cart.objects.create(user=request.user,variant_id=variant_id,product_qty=product_qty )
                messages.success(request, 'Product added successfully in cart') 
                return  redirect('productshow',product_id,variant_id)              
        else:
            messages.error(request, 'you are not login please Login to continue') 
            return redirect('productshow',product_id,variant_id)
    else:
        redirect('productshow',product_id,variant_id)
    return redirect('home')    
    
        
            
    
            

#////////////////////////////////////////////////////////////////////////////////////////////
        
@login_required(login_url='signin')
def updatecart(request):
    if request.method=='POST':
        cart_id=request.POST.get('cart_id')
        if(Cart.objects.filter(user=request.user,id=cart_id)):
            prod_qty=int(request.POST.get('product_qty'))
            
            cart=Cart.objects.get(id=cart_id,user=request.user)
            cartes=Cart.Variant.quantity
            if int(cartes)>=int(prod_qty):
                cart.product_qty=prod_qty
                single=cart.single_total=prod_qty*cart.variant.product.product_price
                cart.save()
                
                carts=Cart.objects.filter(user=request.user).order_by('id')
                total_price=0
                for item in cart:
                    total_price=total_price+item.variant.product.product_price*item.product_qty
                return JsonResponse({'status': 'Updated successfully','sub_total':total_price,'single':single, 'product_price':cart.variant.product.product_price,'quantity':prod_qty})
            else:
                return JsonResponse({'status': 'Not allowed this Quantity'})
    return JsonResponse('something went wrong, reload page',safe=False)

 