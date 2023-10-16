from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product,Size,Color,price_range
from .models import Product,ProductReview
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

    sorts = request.GET.get('sortby', 'atoz')

    if sorts == 'atoz':
        products = Product.objects.filter(is_available=True).order_by('product_name')
    elif sorts == 'ztoa':
        products = Product.objects.filter(is_available=True).order_by('-product_name')
    elif sorts == 'ltoh':
        products = Product.objects.filter(is_available=True).order_by('product_price')
    elif sorts == 'htol':
        products = Product.objects.filter(is_available=True).order_by('-product_price')
    else:
        products = Product.objects.filter(is_available=True).order_by('id')

    product_list = {
        'product': products,
        'categories': category.objects.filter(is_available=True).order_by('id'),
        'brand': Brand.objects.order_by('id'),
    }

    return render(request, 'admin/adminproduct.html', product_list)



# //////////////////////////////////////////////////////////////

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
        # sort=request.POST.get('sortby')

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
            product_price=price,
            category=category_obj,
            brand=brand_obj,
            slug=name,
            product_description=product_description,
            
        )

        product.save()
        messages.success(request,'Product added successfully')
        return redirect('product')
    
    return render(request,'admin/adminproduct.html')

@login_required(login_url='adminsignin')
def deleteproduct(request, product_id):  
    if not request.user.is_superuser:
        return redirect('adminsignin')
    delete_product = Product.objects.get(id=product_id) 
    variants = Variant.objects.filter(product=delete_product)
    for variant in variants:
        variant.is_available = False
        variant.quantity = 0
        variant.save()
    delete_product.is_available =False
    delete_product.save()
    messages.success(request,'product deleted successfully!')
    return redirect('product')

@login_required(login_url='adminsignin')
def editproduct(request,product_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method=='POST':
        name=request.POST.get('product_name')
        price=request.POST.get('product_price')
        category_id=request.POST.get('category')

        # print(category_id,'pppppppppppppppppppp')

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
def searchproduct(request):
    search = request.POST.get('search')
    if search is None or search.strip() == '':
        messages.error(request, 'Field cannot be empty')
        return redirect('product')

    product=Product.objects.filter(
        Q(product_name__icontains=search) |
        Q(product_price__icontains=search) |
        Q(category__categories__icontains=search) |
        Q(brand__names__icontains=search),
        is_available=True
    )
    product_list = {
        'product': product,
        'categories': category.objects.filter(is_available=True).order_by('id'),
        'brand': Brand.objects.filter(is_available=True).order_by('id'),
    }
    if product:
        return render(request, 'admin/adminproduct.html', product_list)
    else:
        product_list['product'] = False
        messages.error(request, 'Search not found')
        return redirect('product')
    


# /////////////////////////////////            PRODUCT VIEW                     // //////////////////////////////


@login_required(login_url='adminsignin')
def productview(request,product_id):

    if not request.user.is_superuser:  
        return redirect('adminsignin')
    
    variant=Variant.objects.filter(product=product_id,is_available=True)
    Size_range=Size.objects.filter(is_available=True).order_by('id')
    color_name=Color.objects.filter(is_available=True).order_by('id')
    product=Product.objects.filter(is_available=True).order_by('id')
    variant_list={
        'variant':variant,
        'size_range':Size_range,
        'color_name':color_name,
        'product':product,
    }
    for i in variant:
        print(i.id,i.product,'gggggggggggggggggggggggg')
    return render(request,'admin/adminproductview.html',{'variant_list':variant_list})


def addreview(request):

    if request.method == 'POST':
        
        if request.user.is_authenticated:
            rating = int(request.POST.get('rating'))
            review_text = request.POST.get('review')
            name = request.POST.get('name')
            email = request.POST.get('email')
            product_id = request.POST.get('product_id')
            img_id =request.POST.get('img_id')
            view_id =request.POST.get('view_id')

            print(rating,review_text,name,email,product_id,'111111111111')

            # Get the product instance based on the product_id
            product = Product.objects.get(id=product_id)
            print(product, rating,review_text,'lotttttttttttttttttttta22222222222222222')

            if rating == 0:
                messages.error(request,'Please Select Stars!')
                return redirect('orderviewuser',view_id)

            if request.user.email == email:
            # Create and save the product review associated with the product
                review = ProductReview.objects.create(
                product=product,
                rating=rating,
                review_text=review_text,
                name=name,
                email=email,
            )
                print(review,'33333333333333333333333333')
                messages.success(request,'Your Review added successfully!')
                return redirect('orderviewuser',view_id)         
            
            else:
                messages.error(request,'Invalid email! Please log in with the correct email!')
                return redirect('orderviewuser',view_id)
 
        else:
            messages.error(request,'Login to continue!')
            return redirect('orderviewuser',view_id)
 
        messages.error(request,'Invalid request method!')
    
    return redirect('orderviewuser',view_id)
    
