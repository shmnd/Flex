from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product,Size,Color,price_range
from .models import Product
from category.models import category
from brand.models import Brand
from django.db.models import Q
from variant.models import Variant
# from variant.models import Varaint

# Create your views here.
@login_required(login_url='adminsignin')
def product(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    

    products=Product.objects.filter(is_available=True).order_by('id')

    product_list={
        'products':products,
        'categories':category.objects.filter(is_available=True).order_by('id'),
        'brand':Brand.objects.order_by('id'),
    }
    return render(request,'admin/adminproduct.html',product_list)

@login_required(login_url='adminsignin')
def createproduct(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        name=request.POST.get('product_name')
        price=request.POST.get('product_price')
        category_id=request.POST.get('category_name')
        brand_id=request.POST.get('brand_name')
        product_description=request.POST.get('product_description')
        print(name,price,category_id,brand_id,product_description,'kanapiiiiiiiiiiiiiiii')

        # validation
        if Product.objects.filter(product_name=name).exists():
            check=Product.objects.get(product_name=name)
            if check.is_available==False:
                check.product_name+=check.product_name
                check.slug+=check.slug
                check.save()
            else:
                messages.error(request,'product name already exists')
                return redirect('product')
            
        if name.strip()=='' or price.strip()=='':
            messages.error(request,'Name or price is empty')
            return redirect('product')
        
        category_obj=category.objects.get(id=category_id)
        brand_obj=Brand.objects.get(id=brand_id)


        # save
        product=Product(
            product_name=name,
            category=category_obj,
            brand=brand_obj,
            product_price=price,
            slug=name,
            product_description=product_description,
        )
        product.save()
        messages.success(request,'Product added successfully')
        return redirect('product')
    return render(request,'admin/adminproduct.html')

@login_required(login_url='adminsignin')
def deleteproduct(request,product_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    delete_product=Product.objects.get(id=product_id)
    variants=Variant.objects.filter(product=delete_product)
    for variant in variants:
        variant.is_available=False
        delete_product.save()
        messages.success(request,'product deleted successfully')
        return redirect('product')

@login_required(login_url='adminsignin')
def editproduct(request,product_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method=='POST':
        name=request.POST.get('product_name')
        price=request.POST.get('product_price')
        category_id=request.POST.get('category')
        brand_id=request.POST.get('brand')
        product_description=request.POST.get('product_description')

        if name.strip()=='' or price.strip()=='':
            messages.error(request,'Name or price fields is empty')
            return redirect('product')
        
        category_obj=category.objects.get(id=category_id)
        brand_obj=Brand.objects.get(id=brand_id)


        if Product.objects.filter(product_name=name).exists():
            check=Product.objects.get(id=product_id)

            if name == check.product_name:
                pass
            else:
                messages.error(request,'Product name already exists')
                return redirect('product')
            
        editproduct=Product.objects.get(id=product_id)
        editproduct.product_name=name
        editproduct.product_price=price
        editproduct.category=category_obj
        editproduct.brand=brand_obj
        editproduct.product_description=product_description
        editproduct.save()
        messages.success(request,'edited successfully')
        return redirect('product')

@login_required(login_url='adminsignin')
def productview(request,product_id):
    if not request.user.is_superuser:  
        return redirect('adminsignin')
    
    variant=Variant.objects.filter(product=product_id,is_availble=True)
    Size_range=Size.objects.filter(is_available=True).order_by('id')
    color_name=Color.objects.filter(is_available=True).order_by('id')
    product=Product.objects.filter(is_available=True).order_by('id')
    variant_list={
        'variant':variant,
        'size_range':Size_range,
        'color_name':color_name,
        'product':product,
    }
    return render(request,'view/productview.html',{'variant_list':variant_list})
    

@login_required(login_url='adminsignin')
def searchproduct(request):
    search=request.POST.get('search')
    if search is None or search.strip()=='':
        messages.error(request,'Field cannot be empty')
        return redirect('product')
    
    product=Product.objects.filter(Q(product_name__icontains=search) | Q(product_price__icontains=search) | Q(category_categories__icontains=search) |Q(brand_name__icontains=search),is_available=True)
    product_list={
        'product':product,
        'categories':category.objects.filter(is_available=True).order_by('id'),
        'name':Brand.objects.filter(is_available=True).order_by('id'),
    }
    if product:
        pass
        return render(request,'product/product.html',product_list)
    else:
        product:False
        messages.error(request,'search not found')
        return redirect('pr')
