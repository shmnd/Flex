from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Size
from cart.models import Cart

# Create your views here.
@login_required(login_url='signin')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user).order_by('id')
        variants=wishlist.values_list('variant',flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')
        cart_count =Cart.objects.filter(user=request.user).count()
        
        
        size=Size.objects.all()
        
        context={
            'wishlist':wishlist,
            'img':img,
            'size':size,
        }
        return render(request,'user/wishlist/wishlist.html',context)
    else:
        return redirect(request,'user/wishlist/wishlist.html')
        
# def add_wishlist(request):
#     print("hloooooooooooooooooooooooooooooooooooooooo")
#     if request.method =='POST':
#         if request.user.is_authenticated:
            
#             variant_id = request.POST.get('variant_id')
#             add_size =request.POST.get('add_size')
           
              
#             if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():
                
#                 return JsonResponse({'status': 'Product already in Wishlist'})
            
        
#             else:
#                 Wishlist.objects.create(user=request.user, variant_id=variant_id)
#                 return JsonResponse({'status': 'Product added successfully in Wishlist'})    
#         else:
#             return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
#     return redirect('home')    


@login_required(login_url='signin')
def removewishlist(request,wish_id):
    try:
        Wishlist_remove=Wishlist.objects.get(id=wish_id)
        Wishlist_remove.delete()
        messages.success(request,'your product deleted succesfully')
    except:
        return redirect('wishlist')
    
    return redirect('wishlist')

# //////////////////////////////new

def add_wishlist1(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_size =request.POST.get('add_size')
            # try:
            #     variant_check =Variant.objects.get(id=variant_id )
            #     if variant_check.size==add_size:
            #         pass
            #     else:
            #         product=variant_check.product
            #         color= variant_check.color
            #         try:
            #             check_variant=Variant.objects.get(product=product, color=color, size=add_size)
            #             variant_id= check_variant.id
            #         except Variant.DoesNotExist:
            #             return JsonResponse({'status': 'Sorry! this variant not available'})  
                        
            # except Variant.DoesNotExist:
            #     return JsonResponse({'status': 'No such prodcut found'})
              
            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in Wishlist'})
            
        
            else:
                Wishlist.objects.create(user=request.user, variant_id=variant_id)
                return JsonResponse({'status': 'Product added successfully in Wishlist'})    
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
    return redirect('home')      
        
    
# //////////////////////////////////



# Create your views here.
@login_required(login_url='signin')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user).order_by('id')
        variants=wishlist.values_list('variant',flat=True)
        img = VariantImage.objects.filter(variant__in=variants).distinct('variant')
        cart_count =Cart.objects.filter(user=request.user).count()
        
        
        size=Size.objects.all()
        
        context={
            'wishlist':wishlist,
            'img':img,
            'size':size,
        }
        return render(request,'user/wishlist/wishlist.html',context)
    else:
        return redirect(request,'user/wishlist/wishlist.html')
        
# def add_wishlist(request):
#     print("hloooooooooooooooooooooooooooooooooooooooo")
#     if request.method =='POST':
#         if request.user.is_authenticated:
            
#             variant_id = request.POST.get('variant_id')
#             add_size =request.POST.get('add_size')
           
              
#             if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():
                
#                 return JsonResponse({'status': 'Product already in Wishlist'})
            
        
#             else:
#                 Wishlist.objects.create(user=request.user, variant_id=variant_id)
#                 return JsonResponse({'status': 'Product added successfully in Wishlist'})    
#         else:
#             return JsonResponse({'status': 'you are not login please Login to continue'})
            
            
#     return redirect('home')    


def removewishlist(request,wish_id):
    try:
        Wishlist_remove=Wishlist.objects.get(id=wish_id)
        Wishlist_remove.delete()
        messages.success(request,'your product deleted succesfully')
    except:
        return redirect('wishlist')
    
    return redirect('wishlist')

# //////////////////////////////new

        
    
