from django.shortcuts import render,redirect,get_object_or_404
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
from registration.models import ReferralCode
from registration.models import CustomUser

# Create your views here.

# userprofile on userside
@login_required(login_url='signin')
@never_cache
def userprofile(request):
    if request.user ==  None:
        return redirect('signin')
    else:
        user=User.objects.filter(email=request.user.email) 
        address=Address.objects.filter(user=request.user,is_available=True)
        cart_count=Cart.objects.filter(user=request.user).count()
        wishlist_count=Wishlist.objects.filter(user=request.user).count()
        last_order=Order.objects.filter(user=request.user).last()
        order =Order.objects.filter(user=request.user)
        refferal_code=ReferralCode.objects.get(user=request.user)
        
        try:
            wallet=Wallet.objects.get(user=request.user)
        except:
            wallet=0
            
        context ={
            'user1':user,
            'address':address,
            'wallet':wallet,
            'cart_count':cart_count,
            'wishlist_count':wishlist_count,
            'order':order,
            'last_order':last_order,  
            'refferal_code':refferal_code      
        }
        
        return render(request,'user/userprofile/userprofile.html',context)

# to add address on userside
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
        
# edit address on userside
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
    
#to show addres on userside 
def viewaddress(request,view_id):
    
    try:
        viewaddress=Address.objects.get(id=view_id)
    except:
        return redirect('userprofile')
            
    return render(request,'user/userprofile/viewaddress.html',{'viewaddress':viewaddress})   
    
# to edit profile on userside
def editprofile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if first_name.strip() == '' or last_name.strip() == '':
            messages.error(request, 'First or Lastname is empty')
        if email.strip() == '':
            messages.error(request, 'Email cannot be empty')
        email_check = validateemail(email)  # Assuming validateemail is a function to check email validity
        if email_check is False:
            messages.error(request, 'Email not valid!')

        if not email_check or first_name.strip() == '' or last_name.strip() == '':
            return render(request, 'userprofile/editprofile.html', {'user': request.user})

        try:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request, 'User profile updated successfully')
            return redirect('userprofile')

        except:
            messages.error(request, 'User does not exist')

    return render(request, 'user/userprofile/editprofile.html', {'user': request.user})

# to delete address on userside
def deleteaddress(request,delete_id):
    address=Address.objects.get(id=delete_id)
    address.is_available = False
    address.save()
    messages.success(request,'address deleted successfully')
    return redirect('userprofile')

# to change password on userside
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
    
# to  vlidate check email is correct userside
def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError: 
        return False

# to validate password on userside
def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except  ValidationError:
        return  False

# orders that user ordered shows on userside
def orderviewuser(request,view_id):
    try:
        orderview=Order.objects.get(id=view_id)
        address=Address.objects.get(id=orderview.address.id)
        products=OrderItem.objects.filter(order=view_id)
        variant_ids=[product.variant.id for product in products]
        image=VariantImage.objects.filter(variant__id__in=variant_ids).distinct()
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
        

# def validate_referral(request):
    # print('hiiiiiiiiiiiiisssssssssssssssssssssss')
    # if request.method == 'POST':
    #     referral_code = request.POST.get('referral_code')
    #     try:
    #         code_obj = ReferralCode.objects.get(code=referral_code, used=False)
    #     except ReferralCode.DoesNotExist:
    #         code_obj = None

    #     if code_obj:
    #         # Valid code; mark it as used and redirect to a success page
    #         code_obj.used = True
    #         code_obj.save()
    #         return redirect('success_page')  # Replace with your success page URL

    #     # Invalid code; show an error message or render the form again
    #     # with an error message
    #     return render(request, 'referral_form.html', {'error_message': 'Invalid referral code'})

    # return redirect( 'userprofile')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='signin')
def validate_referral(request):
    user = request.user

    # Get the ReferralCode instance associated with the user
    referral_obj = get_object_or_404(ReferralCode, user=user)
    
    if referral_obj.used:
        messages.warning(request, 'You have already used a referral code.')
        return redirect('userprofile')

    if request.method == 'POST':
        
        user_input_code = request.POST.get('referral_codes')  # Update this to 'referral_codes'
        

        try:
            # Try to get the ReferralCode object based on the provided code
            referral_code = ReferralCode.objects.get(code=user_input_code)
        except ReferralCode.DoesNotExist:
            # Referral code does not exist
            messages.warning(request, 'Invalid referral code.')
        else:
            # Check if the referral code is not related to the current user
            if referral_code.user != user:
                # Referral code is valid and not related to the current user

                # Add money to the wallet of the user related to the referral code (50 units)
                add_money_to_wallet(referral_code.user, 50)

                # Add money to the wallet of the current user (referrer) (100 units)
                add_money_to_wallet(user, 100)

                # Mark the referral code as used
                referral_code.used = True
                referral_code.save()

                # Mark the user as having used a referral code
                referral_obj.used = True
                referral_obj.save()

                # You can perform additional actions if needed, like giving rewards, etc.

            else:
                # Referral code is related to the current user
                messages.warning(request, 'Referral code is already associated with your account.')

    return redirect('userprofile')



def add_money_to_wallet(user, amount):
    try:
        wallet = Wallet.objects.get(user=user)
    except Wallet.DoesNotExist:
        # Create a new wallet if it doesn't exist for the user
        wallet = Wallet.objects.create(user=user, wallet=amount)
    else:
        # Update the existing wallet balance
        wallet.wallet += amount
        wallet.save()
