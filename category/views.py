from django.shortcuts import render,redirect,get_object_or_404
from .models import category
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from product .models import Product
from django.http import HttpResponse

# Create your views here.

@login_required(login_url='adminsignin')
def categories(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    category_data=category.objects.all().order_by('id')
    return render(request,'admin/admincategory.html',{'category':category_data})

def createcategory(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        name=request.POST.get('categories')
        description=request.POST.get('categories_description')
        
        # validation
        if name.strip()=='':
            messages.error(request,'name cannot be blank ')
            return redirect('categories')
        
        if category.objects.filter(slug=name).exists():
            messages.error(request,'this category is already exists ')
            return redirect('categories')
    # save
        categr=category(categories=name,categories_description=description,slug=name)
        categr.save()
        return redirect('categories')
    
    
    # edit category
    
def editcategory(request,editcategory_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    if request.method=='POST':
        
        name=request.POST.get('categories')
        discription=request.POST.get('categories_description')
        
            
# validation
        try:
            categr=category.objects.get(id=editcategory_id)
        except category.DoesNotExist:
            messages.error(request,'Category not found')
            return redirect('categories')
        if name.strip()=='':
            messages.error(request,'name cannot be empty')
            return redirect('categories')
        
        categr=category.objects.get(id=editcategory_id)
        categr.categories=name
        categr.categories_description=discription
        categr.save()
        return redirect('categories')
        
        
        
# delete category 

def deletecategory(request, deletecategory_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')

    # Get the category to be deleted
    categr = get_object_or_404(category, id=deletecategory_id)

    if request.method == 'POST':
        # Get the selected category to move products to
        deleting_cate_id = request.POST.get('dropcate')

        if deleting_cate_id == 'None':
            # If 'None' is selected, delete the category and its products
            categr.delete()
        else:
            try:
                # Check if the destination category exists
                cate_move = get_object_or_404(category, id=deleting_cate_id)
                # Get all products in the deleting category
                prod_move = Product.objects.filter(category_id=deletecategory_id)
                
                # Move each product to the selected category
                for p in prod_move:
                    p.category = cate_move
                    p.save()
            except category.DoesNotExist:
                # Handle the case where the destination category doesn't exist
                messages.error(request, 'Destination category does not exist')
        
    # Always delete the deleting category after moving or deleting its products
    categr.delete()

    return redirect('categories')
 

# search category

def searchcategory(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    
    if 'keyword' in request.GET:
    
        keyword=request.GET.get ('keyword')
        
        if keyword:
            cate=category.objects.filter(categories__icontains=keyword).order_by('id')
            if cate.exists():
                context={
                    'category':cate
                }
                return render(request,'admin/admincategory.html',context)
            else:
                messages='category  not  found'
                return render(request,'admin/admincategory.html',{'messages':messages})
        else:
            messages='Enter valid category'
            return render(request,'admin/admincategory.html',{'messagaes':messages})
    else:
        return render(request,'404.html')
            



                 
        
