from django.shortcuts import render,redirect
from coupon.models import Coupon
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
import re
from django.db.models import Q

# Create your views here.
# to view coupon in admin page
def coupon(request):
    context = {
        'coupon':Coupon.objects.filter(is_available=True).order_by('id')
    }

    return render(request,'admin/admincoupon.html',context)

# for adding coupon 
@login_required(login_url='adminsignin')
def addcoupon(request):
    if request.method=='POST':
        coupon_name=request.POST.get('coupon_name')
        coupon_code=request.POST.get('coupon_code')
        min_price=request.POST.get('minimum_price')
        coupon_discount_amount=request.POST.get('coupon_discount_amount')
        start_date_str=request.POST.get('start_date')
        end_date_str=request.POST.get('end_date')
    
        if coupon_name is None or coupon_name.strip() == '':
            messages.error(request,'coupon field can not be empty ')
            return redirect('coupon')
        
        if not re.search(r'\b[A-z0-9a-z]{2,}\b',coupon_code):
            messages.error(request,'coupon must include letters and numbers')
            return redirect('coupon')
        
        min_price=int(min_price)
        if not min_price >=0:
            messages.error(request,'minimum price must a positive number')
            return redirect('coupon')
        
        if coupon_discount_amount.strip()=="":
            messages.error(request,'discount cannot be blank')
            return redirect('coupon')
        
        coupon_discount_amount=int(coupon_discount_amount)
        if not coupon_discount_amount >=0:
            messages.error(request,'discount price must be positive')
            return redirect('coupon')
        
        try:
            start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()
        except ValueError:
            messages.error(request,'invalid date format. Use YYYY-MM-DD')
            return redirect('coupon')
        
        if start_date >=end_date:
            messages.error(request, 'strat date must before end date')
            return redirect('coupon')
        
        if start_date < timezone.now().date():
            messages.error(request, 'Start date cannot be in the past')
            return redirect('coupon')
        
        coupon=Coupon.objects.create(
            coupon_name=coupon_name,
            coupon_code=coupon_code,
            min_price=min_price,
            coupon_discount_amount=coupon_discount_amount,
            start_date=start_date,
            end_date=end_date,
        )
        coupon.save()
        
        messages.success(request,'Coupon added successfully ')
        return redirect('coupon')
    
# for editing coupon 
@login_required(login_url='adminsignin')
def editcoupon(request,coupon_id):
    if request.method=='POST':
        coupon_name=request.POST.get('coupon_name')
        coupon_code=request.POST.get('coupon_code')
        min_price=request.POST.get('minimum_price')
        coupon_discount_amount=request.POST.get('coupon_discount_amount')
        start_date_str=request.POST.get('start_date')
        end_date_str=request.POST.get('end_date')
        
        if coupon_name is None or coupon_name.strip() == '':
            messages.error(request,'coupon field can not be empty ')
            return redirect('coupon')
        
        if not re.search(r'\b[A-z0-9a-z]{2,}\b',coupon_code):
            messages.error(request,'coupon must include letters and numbers')
            return redirect('coupon')
        
        if min_price.strip()=="":
            messages.error(request,'minimum price cannot be blank')
            return redirect('coupon')
        min_price=int(min_price)
        if not min_price >0:
            messages.error(request,'minimum price must be positive')
            return redirect('coupon')
               
        if coupon_discount_amount.strip()=="":
            messages.error(request,'discount cannot be blank')
            return redirect('coupon')
        coupon_discount_amount=int(coupon_discount_amount)
        if not coupon_discount_amount >=0:
            messages.error(request,'discount price must be positive')
            return redirect('coupon')
        try:
            start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()
        except ValueError:
            messages.error(request,'invalid date format. Use YYYY-MM-DD')
            return redirect('coupon')
        
        if start_date >= end_date:
            messages.error(request, 'strat date must before end date')
            return redirect('coupon')
        
        if start_date < timezone.now().date():
            messages.error(request, 'Start date cannot be in the past')
            return redirect('coupon')
            
        if Coupon.objects.filter(coupon_name=coupon_name,is_available=True).exclude(id=coupon_id).exists():
            messages.error(request,'name already exists')
            return redirect('coupon')
        
        coupon_edit=Coupon.objects.get(id=coupon_id)
        coupon_edit.coupon_name=coupon_name
        coupon_edit.coupon_code=coupon_code
        coupon_edit.min_price=min_price
        coupon_edit.coupon_discount_amount=coupon_discount_amount
        coupon_edit.start_date=start_date
        coupon_edit.end_date=end_date
        coupon_edit.save()
        messages.success(request,'Coupon edited sucessfully')    
        return redirect('coupon')
    coupon :Coupon.objects.get(id=coupon_id)
    context = {
        'coupon': coupon,
    }
    return render(request,'admin/admincoupon.html',context)
        
# to search coupon 
@login_required(login_url='adminsignin')
def searchcoupon(request):
    search=request.POST.get('search')
    if search is None or search.strip()=="":
        messages.error(request,'field is empty')
        return redirect('coupondelete')
    coupon=(
        Coupon.objects.filter(Q(coupon_name__icontains=search) | Q(coupon_code__icontains=search)|
                              Q(min_price__icontains=search) |Q(coupon_discount_amount__icontains=search) |
                              Q(start_date__icontains=search) |Q(end_date__icontains=search),is_available=True)
    )

# to delete coupon
@login_required(login_url='adminsignin')
def deletecoupon(request,coupon_id):
    try:
        coupon_delete=Coupon.objects.get(id=coupon_id)
        coupon_delete.is_available=False
        coupon_delete.save()
        messages.success(request,'coupon deleted')
        return redirect('coupon')
    except:
        messages.error(request,'The specified coupon does not  exist')
    return redirect('coupon')
    