from django.shortcuts import render,redirect
from variant.models import Variant,VariantImage
from product.models import Product,price_range,Size,Color
from django.db.models import Sum,Avg
from category.models import category
from cart.models import Cart
from wishlist.models import Wishlist

# Create your views here.


def shop(request):
    variant_images=(VariantImage.objects.filter(variant__product__is_available=True)
                    .order_by('variant__product').distinct('variant__product'))
    # ratings=Product.objects.annotate(avg_rating=Avg('review__rating'))
    catergory_filter=category.objects.filter(is_available=True)
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
        # 'ratings':ratings,
        'cart_count':cart_count,
        'category_filter':catergory_filter,
        'size_filter':size_filter,
        'color_filter':color_filter,
    }
    
    return render(request,'user/shop/shop.html')

def shopfilter(request):
    
    if request.method=='POST':
        color=request.POST.get('colorfilter')
        size=request.POST.get('sizefilter')
        categories=request.POST.get('categoryfilter')
        
        if color and size and categories:
            variant_image=(VariantImage.objects.filter
                            (variant__color__id=color,variant__size__id=size,
                            variant__product__category__id=categories,
                            variant__color__is_available=True)
                          .oderb_by('variant__product').distanct('variant__product'))
                
        elif color and size :
                variant_image=(VariantImage.objects.filter
                                (variant__color__id=color,variant__size__id=size,
                                variant__color__is_available=True)
                            .oderb_by('variant__product').distanct('variant__product'))
                
        elif color and categories :
                variant_image=(VariantImage.objects.filter
                                (variant__product__category__id=categories,
                                variant__color__is_available=True,)
                            .oderb_by('variant__product').distanct('variant__product'))
        elif size and categories:    
             variant_image=(VariantImage.objects.filter
                                (variant__product__category__id=categories,
                                variant__color__id=color,variant__size__id=size,)
                            .oderb_by('variant__product').distanct('variant__product'))
        
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
                  
    ratings=Product.objects.annotate(avg_rating=Avg('review_rating'))
    category_filter= category.objects.filter(is_available=True)
    size_filter=category.objects.filter(is_available=True)
    color_filter=Color.objects.filter(is_availble=True)
    
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.filter(user=request.user).count()
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


def shopsort(request):
    name=request.POST.get('sort_select')
    
    variant_images=VariantImage.objects.filter(variant__product__is_available=True)
    
    if name=='aplus':
        variant_images=variant_images.order_by('variant__product__product_name')
    elif name == 'aminus':
        variant_images = variant_images.order_by('-variant__product__product_name')
    elif name == 'priceplus':
        variant_images = variant_images.order_by('variant__product__product_price')
    elif name == 'priceminus':
        variant_images = variant_images.order_by('-variant__product__product_price')
    else:
        variant_images = variant_images.order_by('variant__product')
    
    if name=='aplus' or name=='aminus':
        variant_images=variant_images.distinct('variant__product__product_name')
    if name=='priceplus' or 'priceminus':
        variant_images=variant_images.distinct('variant__product__product_price')
        
    ratings=Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    category_filter=category.objects.filter(is_available=True)
    size_filter=Size.objects.filter(is_available=True)
    color_filter=Product.objects.filter(is_available=True)
        
    try:
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.filter(user=request.user).count()
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