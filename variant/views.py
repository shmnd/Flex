from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.core.exceptions import ObjectDoesNotExist
from .forms import ImageForm
from django.http import JsonResponse
from django.db.models import Q
from .models import Product,Size,Color,price_range,Variant,VariantImage
import webcolors


# Create your views here.


def productvariant(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    variant= Variant.objects.filter(is_available=True).order_by('id')
    size_range=Size.objects.filter(is_available=True).order_by('id')
    color_name=Color.objects.filter(is_avialable=True).order_by('id')
    product=Product.objects.filter(is_available=True).order_by('id')

    variant_list={
        'variant': variant,
        'size_range': size_range,
        'color_name':color_name,
        'product':product,
    }
    return render(request,'variant/variant.html',{'variant_list':variant_list})


def addproductvariant(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        variant_name=request.POST.get('variant_name')
        variant_size=request.POST.get('variant_size')
        variant_color=request.POST.get('variant_color')
        variant_quantity=request.POST.get('variant_quantity')

    # validation
        if variant_quantity.strip()=='':
            messages.error(request,'Quantity field cannot be empty')
            return redirect('productvariant')
        
        try:
            product_obj=Product.objects.get(id=variant_name)
            size_obj=Product.objects.get(id=variant_size)
            color_obj=Color.objects.get(id=variant_color)

            # check variant is already exists

            if Variant.objects.filter(product=product_obj,size=size_obj,color=color_obj).exists():
                messages.error(request,'variant with the same product,size, and color already exists')
                return redirect('productvariant')
            

            # save new variant
            add_variant=Variant(
                product=product_obj,
                color=color_obj,
                size=size_obj,
                quantity=variant_quantity,
            )
            add_variant.save()

            messages.success(request,'Variant added successfully')
            return redirect('productvariant')

        except ObjectDoesNotExist:
            messages.error(request,'Invalid product ,size,or color selected')
            return redirect('productvariant')
        
    return render(request,'variant/variant.html')


def editproductvariant(request,variant_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        variant_name=request.POST.get('variant_name')
        variant_size=request.POST.get('variant_size')
        variant_color=request.POST.get('variant_color')
        variant_quantity=request.POST.get('variant_quantity')

        if variant_quantity.strip()=='':
            messages.error(request,'Quantity field is empty')
            return redirect('productvariant')
        

        product_obj=Product.objects.get(id=variant_name)
        size_obj=Size.objects.get(id=variant_size)
        color_obj=Color.objects.get(id=variant_color)


        # check if variant alredy exists
        if Variant.objects.filter(product=product_obj,size=size_obj,color=color_obj).exists():
            check=Variant.objects.get(id=variant_id)
            if product_obj==check.product and size_obj==check.size and color_obj==check.color:
                pass
            else:
                messages.error(request,'Variant with the same product,size and color already exists')
                return redirect ('productvariant')
            
        edit_variant=Variant.objects.get(id=variant_id)
        edit_variant.color=color_obj
        edit_variant.size=size_obj
        edit_variant.product=product_obj
        edit_variant.quantity=variant_quantity
        edit_variant.save()
        messages.success(request,'producted edited successfully')
        return redirect('productvariant')
    
def productvariantdelete(request,variant_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    delete_productvariant= Variant.objects.get(id=variant_id)
    delete_productvariant.is_available=False
    delete_productvariant.quantity=0
    delete_productvariant.save()
    messages.success(request,'product variant deleted sucessfully')
    return redirect('productvariant')


def productsize(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    product_size=Size.objects.filter(is_avialable=True).order_by('id')
    return render(request,'sizemanagement/sizemanagement.html')

def addsize(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        size=request.POST.get('size')
        if size.strip()=='':
            messages.error(request,'Field cannot be empty')
            return redirect('productsize')
        
        if Size.objects.filter(size_range=size).exists():
            messages.error(request,'Size already exists')
            return redirect('productsize')
        

        size_object=Size(size_range=size)
        size_object.save()
        messages.success(request,'Size added succesfully')
        return redirect('productsize')
    
    return render(request,'sizemanagement/sizemanagement.html')

def sizedelete(request,size_range_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    delete_size=Size.objects.get(id=size_range_id)
    delete_size.is_available=False
    delete_size.save()
    messages.success(request,'size deleted succesfully')
    return redirect('productsize')


def productcolor(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    products_color=Color.objects.filter(is_available=True).order_by('id')
    return render(request,'colormanagement/colormanagement.html',{'product_color':products_color})

def addcolor(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        colorname=request.POST.get('color1')
        color=request.POST.get('color')
        color1=color

        color=get_color_name(color)
        if  color=='Unknown':
            color=color1

        if colorname.strip()=='':
            messages.error(request,'Field cannot be empty')
            return redirect('productcolor')
        
        if Color.objects.filter(color_name=colorname).exists():
            color_add=Color.objects.get(color_name=colorname)
            if color_add.is_avilable==False:
                pass
            else:
                messages.error(request,'color already exists')
                return redirect('productcolor')
        
        color_object=Color(color_name=colorname,color_code=color)
        color_object.save()

        messages.success(request,'color added sucessfully')
        return redirect('productcolor')

    return render(request,'colormanagement/colormanagement.html')

def colordelete(request,color_name_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    delete_color=Color.objects.get(id=color_name_id)
    delete_color.is_avilable=False
    delete_color.save()
    messages.success(request,'color deleted succesfully')
    return redirect('productcolor')

def get_color_name(color_code):
    try:
        color_name = webcolors.rgb_to_name(webcolors.hex_to_rgb(color_code))
        return color_name
    except ValueError:
        return "Unknown"




    

