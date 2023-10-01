# Create your views here.

from django.shortcuts import render,redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout as dj_logout
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate

# verification email
from .models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError


# signin 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if request.user.is_authenticated:
        return redirect('home') 
    

    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']

        # Validation
        if uname.strip() == '' or pwd.strip() == '':
            messages.error(request, "Fields can't be blank")
            return redirect('signin')

        user = authenticate(username=uname, password=pwd)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home') 
        
        else:
            messages.error(request, "Your username or password is incorrect")
            return redirect('signin')  # Redirect to sign-in page with error message

    return render(request, 'user/registrations/signin.html')

def validateEmail(email):
    from django.core.validators import validate_email
    try :
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
    
    elif value.strip()=='':
        return 'Name field cannot be empty'
    elif User.objects.filter(username=value).exists():
        return 'Username already exists'
    else:
        return False
    

# Signup
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    """ OTP VERIFICATION """

    if request.method=='POST':
        get_otp=request.POST.get('otp')
        if get_otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(get_otp)==UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                # messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'registration/signup.html',{'otp':True,'usr':usr})
            
        # User registration validation
        else:
            firstname = request.POST['firstname']   
            lastname = request.POST['lastname']  
            name = request.POST['name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            # null values checking
            
            
            print(email,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
            
            check = [name,email,password1,password2]
            for values in check:
                if values == '':
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.info(request,'some fields are empty')
                    return render(request,'registration/signup.html',context)
                else:
                    pass
            
            result = validate_name(name)
            if result is not False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,result)
                return render(request,'user/registrations/signup.html',context)
            else:
                pass

            result = validateEmail(email)
            if result is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request,'Enter valid email')
                return render(request,'registration/signup.html',context)
            else:
                pass
            
            Pass = ValidatePassword(password1)
            if Pass is False:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.info(request, "Enter a Strong Password using special characters ($&+,:;=?@|'<>.^*()%!-)")
                return render(request,'user/registrations/signup.html',context)
            else:
                pass
            if password1 == password2:
          
                try:
                    User.objects.get(email=email)
                except:
                    usr = User.objects.create_user(first_name=firstname, last_name=lastname, username=name,email=email,password=password1)
                    usr.is_active=False
                    usr.save()
                    user_otp=random.randint(100000,999999)
                    UserOTP.objects.create(user=usr,otp=user_otp)
                    print(user_otp,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                    mess=f'Hello\t{usr.username},\nYour OTP to verify your account for Flex is {user_otp}\nThanks!'
                    send_mail(
                            "welcome to FLEX Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [usr.email],
                            fail_silently=False
                        )
                    return render(request,'user/registrations/signup.html',{'otp':True,'usr':usr})
                else:
                    context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                    messages.error(request,'Email already exist')
                    return render(request,'user/registrations/signup.html',context)
            else:
                context ={
                        'pre_firstname' :firstname,
                        'pre_lastname' :lastname,
                        'pre_name':name,
                        'pre_email':email,
                        'pre_password1':password1,
                        'pre_password2':password2,
                    }
                messages.error(request,'password mismatch')
                return render(request,'registration/signup.html',context)
    else:
        return render(request,'user/registrations/signup.html')               


   
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='signin')
def logout(request):
    dj_logout(request)
    return redirect('home') 
    
    
    
    
def forgotpassword(request):
    if request.method=='POST':
        get_otp=request.POST.get('otp')
        
        if get_otp:
            get_email=request.POST.get('email')
            user=request.objects.get(email=get_email)
            if not re.search(re.compile(r'^\d{6}$'),get_otp):
                messages.error(request,'Entered OTP only contain nemeric')
                return render(request,'user/registration/signin.html',{'otp':True,'user':user})
            
            sessions_otp=request.session.get('otp')
            if int(get_otp) == sessions_otp:
                password1= request.POST.get('password1')
                password2=request.POST.get('password2')
                context={
                    'pre_otp':get_otp,
                }
                
                if password1.strip()=='' or password2.strip()=='':
                    messages.error(request,'field cannot be empty')
                    return render(request,'user/registration/forgotpassword.html',{'otp':True,'user':user,'pre_otp':get_otp})
                
                elif password1 != password2 :
                    messages.error(request,'password doesnot match')
                    return render(request,'user/registration/forgotpassword.html',{'otp':True,'user':user,'pre_otp':get_otp})
                
                Pass = ValidatePassword(password1)
                if Pass is False:
                    messages.error(request,'Please enter a strong password')
                    return render(request,'user/registration/forgetpassword.html',{'otp':True,'user':user,'pre_otp':get_otp})
                
                user.set_password(password1)
                user.save()
                del request.session['otp']
                messages.success(request,'password changed successfully')
                return redirect('signin')
            else:
                messages.warning(request,'You entered a wrong OTP',{'opt':True,'user':user,'pre_otp':get_otp})
                return render(request,'user/registration/forgotpassword.html',{'otp':True,'user':user,'pre_otp':get_otp})
        else:
            get_otp=request.POST.get('otp1')
            email=request.POST.get('user1') 
            if get_otp:
                user=User.objects.get(email=email)
                messages.error(request,'field cannot be empty')
                return render(request,'user/registration/forgotpassword.html')
                    
            else:
                email=request.POST.get['email']
                
                if email.strip()=='':
                    messages.error(request,'field cannot be empty')
                    return render(request,'user/registration/forgotpassword.html')
                
                email_check=validateEmail(email)
                if email_check is False:
                    messages.error(request,'email is not validate')
                    return render(request,'user/registration/forgotpassword.html')

                if User.objects.filter(email=email):
                    user=User.objects.get(email=email)
                    user_otp=random(100000-999999)
                    request.session['otp']=user_otp
                    messages=f'Hello\t{user.first_name},\n OTP verification for your flex account is{user_otp}\n Thanks'
                    send_mail('welcome to FLEX verify email',
                              messages,
                              settings.EMAIL_HOST_USER,
                              [user.email],
                              fail_silently=False
                    )
                    return render(request,'user/registration/forgotpassword.html',{'otp':True,'user':user,'pre_otp':get_otp})
                else:
                    messages.error(request,'email doesnot exist')
                    return render(request,'user/registration/forgotpassword.html')
    return render(request,'user/registration/forgotpassword.html')
