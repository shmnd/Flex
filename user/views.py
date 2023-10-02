from django.shortcuts import render,redirect
from django.utils import timezone
import re
from django.forms import ValidationError
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from cart.models import Cart
from checkout.models import Itemstatus,OrderItem,Order,Orderstatus
from dashboard.views import validateEmail
from order.models import Order,Order_cancelled,Orderreturn
from product.models import Product,Size,Color
from variant.models import Variant,VariantImage
from user.models import User
from wishlist.models import Wishlist
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from .models import Address,Wallet
from registration.models import CustomUser


# from checkout.models import Itemstatus, Order,OrderItem


# Create your views here.
@login_required(login_url='signin')
def userprofile(request):
    if request.user.is_authenticated:
        user=CustomUser.objects.filter(email=request.user.email) 
        address=Address.objects.filter(user=request.user,is_available=True)
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        last_order=Order.objects.filter(user=request.user).last()
        order =Order.objects.filter(user=request.user) 
        
        try:
            wallet=wallet.objects.get(user=request.user)
        except:
            wallet=0
            
        context={
            'user':user,
            'address':address,
            'wallet':wallet,
            'cart_count':cart_count,
            'wishlist_count':wishlist_count,
            'order':order,
            'last_order':last_order,        
        }
        return render(request,'user/userprofile/userprofile.html',context)
    else:
        messages.error(request,'user did not logged in')
        return redirect('home')
    
    


def addaddress(request,add_id):
    if request.method=='POST':
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        
        context={
            'pre_first_name': first_name,
            'pre_last_name':last_name,
            'pre_country':country,
            'pre_address':address,
            'pre_city':city,
            'pre_pincode':pincode,
            'pre_phone':phone,
            'pre_email':email,
            'pre_state':state,
            'pre_order_note':order_note,
            'check':add_id,
            'wishlist_count':wishlist_count, 
            'cart_count':cart_count,
        }
        
        if request.user is None:
            return
        
        if first_name.strip() =='':
            messages.error(request,'names cannot be empty')
            context['pre_first_name']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if last_name.strip()=='':
            messages.error('names cannot be empty')
            context['pre_last_name']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if country.strip()=='':
            messages.error(request,'country cannot be empty')
            context['pre_country']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if city.strip()=='':
            messages.error(request,'field city is empty')
            context['pre_city']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if address.strip()=='':
            messages.error(request,'address field is emptpy')
            context['pre_address']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            context['pre_pincode']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        if not re.search(re.compile(r'^\d{6}$'),pincode ): 
            messages.error(request,'should only t contain nuemeric')
            context['pre_pincode']=''
            return render(request,'user/userprofile/addaddress.html',context)

        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone):
            messages.error(request,'Enter valid phone number')
            context['pre_phone']=''
            return render(request,'user/userprofile/addaddress.html',context)
        
        phonenumber_checking=len(phone)
        if not phonenumber_checking==10:
            messages.error(request,'phone number should cotain 10 digits')
            context['pre_phone']=''
            return render(request,'user/userprofile/addaddress.html',context)
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            context['pre_email']=''
            return render(request,'user/userprofile/addaddress.html',context)
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            context['pre_email']=''
            return render(request,'user/userprofile/addaddress.html',context)
                    
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            context['pre_state']=''
            return render(request,'user/userprofile/addaddress.html',context)

        # ad =Address.objects.check()

        ads=Address()
        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.state=state
        ads.order_note=order_note
        ads.is_available=True
        ads.save()
        messages.success(request,' Address Added successfully!')
        if add_id==1:
            check=1
            return redirect('userprofile')
        else: 
            check=2 
            return redirect('checkout')
    
    cart_count=Cart.objects.filter(user=request.user).count()
    
    wishlist_count=Wishlist.objects.filter(user=request.user).count()
    if add_id ==1:
        check=1
    else:
        check=2
    return render(request,'user/userprofile/addaddress.html',{'check':check,'wishlist_count':wishlist_count,'cart_count':cart_count})
        
def editaddress(request,edit_id):
    if request.method=='POST':
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        pincode=request.POST.get('pincode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        state=request.POST.get('state')
        order_note=request.POST.get('order_note')
        try:
            editaddress=Address.objects.get(id=edit_id)
        except:
            return redirect('userprofile')
            
        if request.user is None:
            return

        if first_name.strip() == '' : 
            messages.error(request,'names cannot be empty!!!')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if last_name.strip() == '':
            messages.error(request,'names cannot be empty!!!')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if country.strip()=='':
            messages.error(request,'Country cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if city.strip()=='':
            messages.error(request,'city cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if address.strip()=='':
            messages.error(request,'address cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if pincode.strip()=='':
            messages.error(request,'pincode cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if not re.search(re.compile(r'^\d{6}$'),pincode ):  
            messages.error(request,'should only 6 contain numeric!')   
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'),phone ): 
            messages.error(request,'Enter valid phonenumber!')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if phone.strip()=='':
            messages.error(request,'phone cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        phonenumber_checking=len(phone)
        if not  phonenumber_checking==10:
            messages.error(request,'phonenumber should be must contain 10digits!')  
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        if email.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        email_check=validateemail(email)
        if email_check is False:
            messages.error(request,'email not valid!')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})     
        if state.strip()=='':
            messages.error(request,'state cannot be empty')
            return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress})
        try:
            ads=Address.objects.get(id=edit_id)
        except Address.DoesNotExist:
            messages.error(request,'Address not found')
            return redirect('userprofile')

        ads.user=request.user
        ads.first_name=first_name
        ads.last_name=last_name
        ads.country=country
        ads.address=address
        ads.city=city
        ads.state=state
        ads.pincode=pincode
        ads.phone=phone
        ads.email=email
        ads.order_note=order_note
        ads.is_available=True
        ads.save()
        messages.success(request,'address edited successfully')
        return redirect('userprofile')
    try:
        editaddress=Address.objects.get(id=edit_id)
    except:
        return redirect('userprofile')
    cart_count=Cart.objects.filter(user=request.user).count()
    wishlist_count=Wishlist.objects.filter(user=request.user).count()
    return render(request,'user/userprofile/editaddress.html',{'editaddress':editaddress,'wishlist_count':wishlist_count,'cart_count':cart_count})
    
    
def viewaddress(request,view_id):
    
    try:
        viewaddress=Address.objects.get(id=view_id)
    except:
        return redirect('userprofile')
            
    
    return render(request,'user/userprofile/viewaddress.html',{'viewaddress':viewaddress})   
    

def editprofile(request):
    if request.method=='POST':
        
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        emaill=request.POST.get('email')
        
        try:            
            user = CustomUser.objects.get(emails=request.user)
        except:
            return redirect('userprofile')

        print('llllllllllllllllllllllllllllllllll')
            
        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First or Lastname is empty')
            return render(request,'user/userprofile/editprofile.html',{'user':user})
        
        if emaill.strip()=='':
            messages.error(request,'email cannot be empty')
            return render(request,'user/userprofile/editprofile.html',{'user':user})
        email_check=validateemail(emaill)
        
        if email_check is False:
            messages.error(request,'email not valid!')
            return render(request,'user/userprofile/editprofile.html',{'user':user})
        
        try:
            user=User.objects.get(emaill=request.user)
            print(user)
            user.first_name=first_name
            user.last_name=last_name
            user.email=emaill
            user.save()
            messages.success(request,'userprofile updated successfull')
            return redirect('userprofile')
        except:
            messages.error(request,'User does not exist')
    # print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
    try:
        user = CustomUser.objects.get(emails=request.user.email)

    except:
         return redirect('userprofile')
    return render(request,'user/userprofile/editprofile.html',{'user':user})



def deleteaddress(request,delete_id):
    address=Address.objects.get(id=delete_id)
    address.is_available = False
    address.save()
    messages.success(request,'address deleted successfully')
    return redirect('userprofile')


def changepassword(request):
    if request.method=='POST':
        old_password=request.POST.get('old_password')
        new_password=request.POST.get('new_password')
        confirm_newpassword=request.POST.get('confirm_newpassword')
    # validations
        if new_password.strip()=='' and confirm_newpassword.strip()=='':
            messages.error(request,'column cannot be empty')
            return render(request,'user/userprofile/password.html')
        if new_password != confirm_newpassword:
            messages.error(request,'Password did not match')
            return render(request,'user/userprofile/password.html')
        
        password_check=validatepassword(new_password)
        if password_check is False:
            messages.error(request,'enter a strong password')
            return render(request,'user/userprofile/password.html')
        user= User.objects.get(username=request.user)
        if check_password(old_password,user.password):
            user.set_password(new_password)
            user.save()
            
            update_session_auth_hash(request,user)
            messages.success(request,'password updated successfully')
            return redirect('userprofile')
        else:
            messages.error(request,'invalid old password')
            return render(request,'user/userprofile/password.html')
    return render(request,'user/userprofile/password.html')
    

def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError: 
        return False
    
def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except  ValidationError:
        return  False
    


def orderviewuser(request,view_id):
    try:
        orderview=Order.objects.get(id=view_id)
        address=Address.objects.get(id=orderview.address.id)
        products=OrderItem.objects.filter(order=view_id)
        variant_ids=[product.variant.id for product in products]
        image=VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__color')
        item_status_o=Itemstatus.objects.all()
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        date=orderview.update_at + timedelta(days=3)
        
        
        if date >=timezone.now():
            date=True
        else:
            date=False
            
        context={
            'date':date,
            'address':address,
            'products':products,
            'image':image,
            'item_status_o':item_status_o,
            'wishlist_count':wishlist_count,
            'cart_count':cart_count,
            'orderview':orderview,
        }
        return render(request,'user/userprofile/orderviewuser.html',context)
    
    
    except Order.DoesNotExist:
         print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('userprofile')    
        

