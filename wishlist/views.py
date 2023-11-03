from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from .models import Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Size
from cart.models import Cart

# Create your views here.

# view wishlist form userside
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
            'cart_count':cart_count,
        }
        return render(request,'user/wishlist/wishlist.html',context)
    else:
        return redirect(request,'user/wishlist/wishlist.html')
        
# remove product from wishlist
@login_required(login_url='signin')
def removewishlist(request,wish_id):
    try:
        Wishlist_remove=Wishlist.objects.get(id=wish_id)
        Wishlist_remove.delete()
        messages.success(request,'your product deleted succesfully')
    except:
        return redirect('wishlist')
    
    return redirect('wishlist')

# adding product into wishlist
def add_wishlist1(request):
    if request.method =='POST':
        if request.user.is_authenticated:
            
            variant_id = request.POST.get('variant_id')
            add_size =request.POST.get('add_size')
              
            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():
                
                return JsonResponse({'status': 'Product already in Wishlist'})
            
            else:
                Wishlist.objects.create(user=request.user, variant_id=variant_id)
                return JsonResponse({'status': 'Product added successfully in Wishlist'})    
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})
            
    return redirect('home')    



