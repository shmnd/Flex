from django.shortcuts import render,redirect
from .models import Offer
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='adminsignin')
def offer(request):
    context ={
        'offer':Offer.objects.filter(is_available=True).order_by('id')
    }
    return render(request,'admin/adminoffer.html',context)

@login_required(login_url='adminsignin')
def addoffer(request):
    if request.method=='POST':
        offername=request.POST.get('offername')
        discount=request.POST.get('discount')
        start_date_str=request.POST.get('start_date')
        end_date_str=request.POST.get('end_date')
        
        print(start_date_str,end_date_str,'zzzzzzzzzzzzzzzzzzzzzzzzzzz')
        
        if offername is None or offername.strip()=='':
            messages.error(request,' offername cannot be empty ')
            return redirect('offer')
        
        if discount.strip()=='':
            messages.error(request,'cannot blank discount')
            return redirect('offer')
        try:
            start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()
        except ValueError:
            messages.error(request,'Invalid date format .Use YYYY-MM-DD')
            return redirect('offer')
        
        if start_date >= end_date:
            messages.error(request,'start date must be before end date')
            return redirect('offer')
        
        if start_date < timezone.now().date():
            messages.error(request,'start date cannot be in past days')
            return redirect('offer')
    
        offer=Offer.objects.create(
            offer_name=offername,
            discount_amount=discount,
            start_date=start_date,
            end_date=end_date
        )
        offer.save()
        messages.success(request,'product successfully saved successfully')
        return redirect('offer')
    
    
@login_required(login_url='adminsignin')
def editoffer(request,offer_id):
    if request.method=='POST':
        offername=request.POST.get('offername')
        discount=request.POST.get('discount')
        start_date_str=request.POST.get('start_date')
        end_date_str=request.POST.get('end_date')
        
        if offername is None and offername.strip()=='':
            messages.error(request,' offername cannot be empty ')
            return redirect('offer')
        
        if Offer.objects.filter(offer_name=offername,is_available=True).exclude(id=offer_id).exists():
            messages.error(request,'Offer name already exists')
        try:
            start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()
        except ValueError:
            messages.error(request,'Invalid date format .Use YYYY-MM-DD')
            return redirect('offer')
        
        if start_date >= end_date:
            messages.error(request,'start date must be before end date')
            return redirect('offer')
        
        if start_date < timezone.now().date():
            messages.error(request,'start date cannot be in past days')
            return redirect('offer')
        
        editoff=Offer.objects.get(id=offer_id)
        editoff.offer_name=offername
        editoff.discount_amount=discount
        editoff.start_date=start_date
        editoff.end_date=end_date
        editoff.save()
    offers:Offer.objects.get(id=offer_id)
    context={
        'offer':offers,
    }
    return render(request,'admin/admincoupon.html',context)

@login_required(login_url='adminsignin')        
def deleteoffer(request,delete_id):
    try:
        offer=Offer.objects.get(id=delete_id)
        offer.is_available=False
        offer.save()
        messages.success(request,'offer deleted sucessfully')
    except:
        messages.error(request,'offer does not exist')
    return redirect('offer')
    
@login_required(login_url='adminsignin')
def searchoffer(request,):
    search=request.POST.get('search')
    if search is None or search.strip()=='':
        messages.error(request,'search feild is empty')
        return redirect('offer')
    
    offer=Offer.objects.filter(Q(offer_name__icontains=search) | Q(discount_amount__icontains=search) | Q(start_date__icontains=search) | Q(end_date__icontains=search),is_available=True)
    context={
        'offer':offer
    }
    
    if offer:
        pass
        return render(request,'admin/admincoupon.html',context)
    else:
        offer:False
        messages.error(request,'search not found')
        return redirect('offer')

