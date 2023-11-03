from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from product.models import Product,price_range,Size,Color,ProductReview
from django.db.models import Sum,Avg
from category.models import category
from cart.models import Cart
from wishlist.models import Wishlist

# Create your views here.

# show product on shop page in userside
def shop(request):
    variant_images=(VariantImage.objects.filter(variant__product__is_available=True).order_by('variant__product').distinct('variant__product'))
    
    ratings=Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    category_filter=category.objects.filter(is_available=True)
    size_filter=Size.objects.filter(is_available=True)
    color_filter=Color.objects.filter(is_available=True)
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        
    except:
        cart_count=False
        wishlist_count=False
    context={
        'variant_images':variant_images,
        'ratings':ratings,
        'cart_count':cart_count,
        'category_filter':category_filter,
        'size_filter':size_filter,
        'color_filter':color_filter,
        'wishlist_count':wishlist_count,
    }
    # for i in category_filter:
    #     print(i.id,i.categories,'ddddddddddddddddddddddddddddddddd')
    
    return render(request,'user/shop/shop.html',context)

# filter on shop page base on color,category,size
def shopfilter(request):
    
    variant_images=[]
    
    if request.method=='POST':
        color=request.POST.get('colorfilter')
        size=request.POST.get('sizefilter')
        categories=request.POST.get('categoryfilter')
        
        if color and size and categories:
            variant_images=(VariantImage.objects.filter
                            (variant__color__id=color,variant__size__id=size,
                            variant__product__category__id=categories,
                            variant__product__is_available=True)
                          .order_by('variant__product').distinct('variant__product'))
                
        elif color and size:
                variant_images=(VariantImage.objects.filter
                                (variant__color__id=color,variant__size__id=size,
                                variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))
                
        elif color and categories :
                variant_images=(VariantImage.objects.filter
                                (variant__product__category__id=categories,
                                variant__product__is_available=True,)
                            .order_by('variant__product').distinct('variant__product'))
        elif size and categories:    
             variant_images=(VariantImage.objects.filter
                                (variant__product__category__id=categories,
                                variant__size__id=size,
                                variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))
        
        elif size:
            variant_images = (VariantImage.objects.filter
                                (variant__size__id =size,
                                variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))
        elif color:
            variant_images = (VariantImage.objects.filter
                                (variant__color__id=color,
                                variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))     
        elif categories:
            variant_images = (VariantImage.objects.filter
                                (variant__product__category__id=categories,
                                variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))
        else:
            variant_images = (VariantImage.objects.filter
                            (variant__product__is_available=True)
                            .order_by('variant__product').distinct('variant__product'))   
                  
    ratings=Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    
    category_filter= category.objects.filter(is_available=True)
    size_filter=Size.objects.filter(is_available=True)
    color_filter=Color.objects.filter(is_available=True)
    
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count=False
        wishlist_count=False
    context={
              'variant_images': variant_images,
              'ratings':ratings,
              'wishlist_count':wishlist_count,
              'cart_count' :cart_count,
              'category_filter':category_filter,
              'size_filter':size_filter,
              'color_filter':color_filter,
            }
    
    return render(request,'user/shop/shop.html',context)

# sorting on shop page userside
def shopsort(request):
    name = request.POST.get('sort_select')
    
    variant_images = VariantImage.objects.filter(variant__product__is_available=True)
    
    if name == 'aplus':
        variant_images = variant_images.order_by('variant__product__product_name')
    elif name == 'aminus':
        variant_images = variant_images.order_by('-variant__product__product_name')
    elif name == 'priceplus':
        variant_images = variant_images.order_by('variant__product__product_price')
    elif name == 'priceminus':
        variant_images = variant_images.order_by('-variant__product__product_price')
    else:
        variant_images = variant_images.order_by('variant__product')
    if name == 'aplus'or name == 'aminus':
        variant_images = variant_images.distinct('variant__product__product_name')  
    if  name == 'priceplus' or name == 'priceminus':
        variant_images = variant_images.distinct('variant__product__product_price') 
    
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    category_filter = category.objects.filter(is_available=True)
    size_filter = Size.objects.filter(is_available=True)
    color_filter = Color.objects.filter(is_available=True)
    try:
        cart_count =Cart.objects.filter(user =request.user).count()
        wishlist_count =Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count =False
        wishlist_count =False 
    
    context = {
        'variant_images': variant_images,
        'ratings': ratings,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
        'category_filter': category_filter,
        'size_filter': size_filter,
        'color_filter': color_filter,
    }
    
    return render(request, 'user/shop/shop.html', context)