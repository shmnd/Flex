from django.shortcuts import render,redirect
import re
from django.contrib import messages,auth
from variant.models import VariantImage, Variant
from django.db.models import Q 
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from product.models import Product,Size,Color
from category.models import category







def home(request):
    if  request.user.is_superuser:
        return redirect('dashboard')
    
    categories=category.objects.all()
    products=Product.objects.all()

    # try:
    #     cart_count=Cart.objects.filter(user=request.user).count()
    #     whishlist_count=Wishlist.objects.filter(user=request.user).count()
    # except:
    #     cart_count=False
    #     whishlist_count=False

    variant_image=(VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product'))
    
    context={
        'categories':categories,
        'products':products,
        'variant_images':variant_image,
        # 'wishlist_count':wishlist_count,
        # 'cart_count':cart_count,
    }

    return render(request,'user/home/index.html',context)



def productshow(request,prod_id,img_id):

def blog(request):
    return render(request,'blog/blog.html')