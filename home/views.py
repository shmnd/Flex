from django.shortcuts import render,redirect
import re
from django.contrib import messages,auth
from variant.models import VariantImage, Variant
from django.db.models import Q ,Avg,Sum
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from product.models import Product, ProductReview,Size,Color
from category.models import category
from cart.models import Cart
from wishlist.models import Wishlist

# main page of userside 
def home(request):
    if  request.user.is_superuser:
        messages.error(request,'admin cannot acess the userside')
        return redirect('adminsignin') 
    
    categories=category.objects.all()
    products=Product.objects.all()
    reviews = ProductReview.objects.all()
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))

    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count=False
        wishlist_count=False

    variant_images=(VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product'))
    
    context={
        'categories':categories,
        'products':products,
        'ratings' : ratings,
        'reviews':reviews,
        'variant_images':variant_images,
        'wishlist_count':wishlist_count,
        'cart_count':cart_count,
    }

    return render(request,'user/home/index.html',context)


# to dispaly the product on userside
def productshow(request,prod_id,img_id):
    variant=VariantImage.objects.filter(variant=img_id,is_available=True)
    variant_images=(VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('varianat_product'))
    size=Size.objects.all()
    color=VariantImage.objects.filter(variant__product__id=prod_id,is_available=True).distinct('variant__color')
    
    reviews = ProductReview.objects.filter(product=prod_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    rev_count=ProductReview.objects.filter(product=prod_id).count()
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    try:
     average_rating = int(average_rating)
    except:
        average_rating=0
    context={
        'variant':variant,
        'size':size,
        'color':color,
        'variant_images':variant_images,
        'reviews':reviews,
        'average_rating':average_rating ,
        'wishlist_count':wishlist_count,
        'cart_count' :cart_count,
        'rev_count':rev_count,
        
    }
    return render(request,'user/product/productshow.html',context)

# to show the category on product page on userside
def usercategoryshow(request,category_id):
    variant=VariantImage.objects.filter(variant__product__category=category_id,is_available=True).distinct('variant_color')
    rating=Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    context={
        'variant':variant,
    }
    return render(request,'user/category/categoryuser.html',context)

# to blog page on userside
def blog(request):
    return render(request, 'user/blog/blog.html')