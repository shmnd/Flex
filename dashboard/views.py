# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout



# verification email
from registration.models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError


def adminsignin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email,'hiiiiiiiiiiiiiiiiiiiiiiii')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        # Validation
        if email.strip() == '' or password.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('adminsignin')

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect('dashboard')
            else:
                messages.error(request, "You are not a superuser")
                return redirect('adminsignin')

        messages.error(request, "Invalid email or password")
        return redirect('adminsignin')

    return render(request, 'admin/adminsignin.html')


# validations
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False
    
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False
    
    
    
    
def adminsignup(request):
    # OTP VERIFICATION
    if request.method == 'POST':
        get_otp = request.POST.get("otp")
        # print(get_otp,'bbbbbbbbbbbbbbbbbbbbbbbbb')
        if get_otp:
            get_email = request.POST.get("email")
            usr = User.objects.get(email=get_email)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                # print(get_otp,usr,'cccccccccccccccccccccccccccccccccc')
                
                usr.is_active = True
                usr.is_superuser = True
                usr.save()  # Save the changes to the user object
                auth.login(request, usr)
                messages.success(request, f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('dashboard')
            else:
                messages.warning(request, 'You Entered a wrong OTP')
                return render(request, 'admin/adminsignup.html', {'otp': True, 'usr': usr})

        # User registration validation
        else:
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Null values checking
            check = [email, password1, password2]
            for value in check:
                if value == '':
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.info(request, 'Some fields are empty')
                    return render(request, 'admin/adminsignup.html', context)

            result = validateEmail(email)
            if not result:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a valid email')
                return render(request, 'admin/adminsignup.html', context)

            Pass = ValidatePassword(password1)
            if not Pass:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.info(request, 'Enter a strong password')
                return render(request, 'admin/adminsignup.html', context)

            if password1 == password2:
                try:
                    User.objects.get(email=email)
                except User.DoesNotExist:
                    usr = User.objects.create_user(username=email, email=email, password=password1)
                    usr.is_active = False
                    usr.is_superuser = True
                    usr.save()
                    
                    user_otp = random.randint(100000, 999999)
                    UserOTP.objects.create(user=usr, otp=user_otp)
                    print(user_otp,'sssssssssssssssssssssssss')
                    mess = f'Hello {usr.username},\nYour OTP to verify your account for Flex is {user_otp}\nThanks!'
                    send_mail(
                        "Welcome to FLEX : Verify your Email",
                        mess,
                        settings.EMAIL_HOST_USER,
                        [usr.email],
                        fail_silently=False
                    )
                    return render(request, 'admin/adminsignup.html', {'otp': True, 'usr': usr})
                else:
                    context = {
                        'pre_email': email,
                        'pre_password1': password1,
                        'pre_password2': password2,
                    }
                    messages.error(request, 'Email already exists')
                    return render(request, 'admin/adminsignup.html', context)
            else:
                context = {
                    'pre_email': email,
                    'pre_password1': password1,
                    'pre_password2': password2,
                }
                messages.error(request, 'Password mismatch')
                return render(request, 'admin/adminsignup.html', context)
    else:
        return render(request, 'admin/adminsignup.html')
    
    
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    return render(request,'admin/dashboard.html')
    
    
    
# user management
def user(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    user_data = User.objects.all().order_by('id')
    return render(request,'admin/usermanagement.html',{'users': user_data})


# Block User
def blockuser(request,user_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('user')

# brand

def brands(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    brand_data = brand.objects.all().order_by('id')
    return render(request, 'brand/brand.html',{'brand' : brand_data})

# Crete brand
def createbrands(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        cname = request.POST.get('brand_name', '')
        eimage = request.FILES.get('brand_image', None)
        address = request.POST['brand_address']
        cdescription = request.POST['brand_discription']

        # Validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')

        if not eimage:
            messages.error(request, "Image not uploaded")
            return redirect('brands')

        bran = brand(
            brand_name=cname,
            brand_image=eimage,
            brand_address=address,
            brand_discription=cdescription,
        )
        bran.save()
        return redirect('brands')

    return render(request, 'brand/createbrands.html')


# Edit Brand
def editbrands(request, editbrands_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if request.method == 'POST':
        cname = request.POST['brand_name']
        address = request.POST['brand_address']
        cdescription = request.POST['brand_discription']
# validation
        if cname.strip() == '':
            messages.error(request, "Name Field empty")
            return redirect('brands')

        try:
            cat = brand.objects.get(id=editbrands_id)
            eimage = request.FILES['brand_image']
            cat.brand_image = eimage
            cat.save()
        except:
            pass 

        cat = brand.objects.get(id=editbrands_id)
        cat.brand_name = cname
        cat.brand_address = address
        cat.brand_discription = cdescription
        cat.save()
        return redirect('brands')
    cate = brand.objects.filter(slug=editbrands_id)       
    return render(request, 'brand/editbrands.html', {'catego': cate})

# Delete brand
def deletebrands(request,deletebrands_id):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    bran = brand.objects.get(id=deletebrands_id)
    bran.delete()
    return redirect('brands')


# Search User
def searchuser(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users = User.objects.filter(username__icontains=keyword).order_by('id')
            if users.exists():
                context = {
                    'users': users,
                }
                return render(request, 'admin/dashboard.html', context)
            else:
                message = "User not found."
                return render(request, 'admin/dashboard.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'admin/dashboard.html', {'message': message})
    else:
        return render(request, 'error/index.html')
    
# Aearch Brand
def search_brand(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            Brand = brand.objects.filter(brand_name__icontains=keyword).order_by('id')
            if Brand.exists():
                context = {
                    'brand': Brand,
                }
                return render(request, 'brand/brand.html', context)
            else:
                message = "Brand not found."
                return render(request, 'brand/brand.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'brand/brand.html', {'message': message})
    else:
        return render(request, 'error/index.html')
    
    
def adminlogout(request):
    logout(request)
    return redirect('adminsignin')
    