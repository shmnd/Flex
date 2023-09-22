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
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user).order_by('id')
        variants=cart.values_list('variant',flat=True)
        cart=Cart.objects.filter(user=request.user).count()
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
            'wishlist_count':wishlist_count,
            'cart_count':cart_count,
            
            
            
        }
def removecart(request):
    pass
def addcart(request):
    pass
def updatecart(request):
    pass

 