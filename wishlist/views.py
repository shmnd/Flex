from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from django.http import JsonResponse
from .models import Wishlist
# cart_count =Cart.objects.filter(user =request.user).count()
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Size

# Create your views here.
@login_required(login_url='signin')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user).order_by('id')
        variants=wishlist.values.list('variant',flat=True)
        img=VariantImage.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        size=Size.objects.all()
        
        context={
            'wishlist':wishlist,
            'img':img,
            'size':size,
            # 'cart_count':cart_count,
            'wishlist_count':wishlist_count,
        }
        return render(request,'wishlist/wishlist.html',context)
    else:
        return redirect(request,'wishlist/wishlist.html')
        

def addwishlist(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            variant_id=request.POST.get('variant_id')
            add_size=request.POST.get('add_size')
            
            if Wishlist.objects.filter(user=request.user,variant_id=variant_id).exists():
                return JsonResponse({'status':'Product added successfully in wishlist'})
            else:
                return JsonResponse({'status':'you are not login please Login to continue'})
    return redirect('home')


@login_required(login_url='signin')
def removewishlist(requset,wish_id):
    try:
        Wishlist_remove=Wishlist.objects.get(id=wish_id)
        Wishlist_remove.delete()
        messages.success(request,'your product deleted succesfully')
    except:
        return redirect('wishlist')
    
    return redirect('wishlist')
        
    
