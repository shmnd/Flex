# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout
from brand.models import Brand
from checkout.models import Order,OrderItem,Itemstatus,Orderstatus
from django.db.models import Q
from django.core.exceptions import ValidationError
# from checkout.modes import Order

import csv
from datetime import date, datetime
from itertools import groupby
from fpdf import FPDF
from django.db.models import Prefetch   
from checkout.models import OrderItem

from checkout.models import OrderItem,Order
# from order.models import Order
from django.db.models import Sum

import matplotlib.pyplot as plt
import pandas as pd

# verification email
from registration.models import UserOTP
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError

# to singin for admin
def adminsignin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        print(email,'emaillllllllllllllllllll')
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


# validations to email  for admin
def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

# to validate password  for admin
def ValidatePassword(password):
    from django.contrib.auth.password_validation import validate_password
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False


# to validate name  for admin
def validate_name(value):
    if not re.match(r'^[a-zA-Z\s]*$', value):
        return 'Name should only contain alphabets and spaces'
    
    elif value.strip() == '':
        return 'Name field cannot be empty or contain only spaces' 
    elif User.objects.filter(username=value).exists():
        return 'Usename already exist'
    else:
        return False
    
#adminsignup for admin 
def adminsignup(request):
    # OTP VERIFICATION
    if request.method == 'POST':
        get_otp = request.POST.get("otp")
        if get_otp:
            get_email = request.POST.get("email")
            usr = User.objects.get(email=get_email)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                print(get_otp,usr,'otpppppppppppppppppppppppppp')
                
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
    
    
# user management (block or unblock) adminside
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


# Search User on adminside
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
                return render(request, 'admin/usermanagement.html', context)
            else:
                message = "User not found."
                return render(request, 'admin/usermanagement.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'admin/usermanagement.html', {'message': message})
    else:
        return render(request, 'error/index.html')
    
    
#admin logout 
def adminlogout(request):
    logout(request)
    return redirect('adminsignin')



# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta

def dashboard(request, interval='monthly'):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    
    # Set default date range to one month
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)

    # Adjust date range based on the selected interval
    if interval == 'yearly':
        start_date = end_date - timedelta(days=365)
    elif interval == 'weekly':
        start_date = end_date - timedelta(days=7)

    # Sales data query
    sales_data = OrderItem.objects.filter(order__created_at__date__range=[start_date, end_date]).values('order__created_at__date').annotate(total_sales=Sum('price')).order_by('-order__created_at__date')
    
    # Prepare data for the chart
    categories = [item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
    sales_values = [item['total_sales'] for item in sales_data]
   
    # Return data query
    return_data = OrderItem.objects.filter(orderitem_status__item_status__in=["Return", "Cancelled"]).filter(order__created_at__date__range=[start_date, end_date]).values('order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
    return_values = [item['total_returns'] for item in return_data]

    orders = Order.objects.order_by('-created_at')[:10]


    try:
        status_delivery = Order.objects.filter(order_status__id=4).count()
        status_cancel = Order.objects.filter(order_status__id=5).count()
        status_return = Order.objects.filter(order_status__id=6).count()
        Total = status_delivery + status_cancel + status_return
        status_delivery = (status_delivery / Total) * 100
        status_cancel = (status_cancel / Total) * 100
        status_return = (status_return / Total) * 100
    except:
        status_delivery = 0
        status_cancel = 0
        status_return = 0

    try:
        totalearnings = 0
        total_earn = Order.objects.filter(order_status__id=4)
        for i in total_earn:
            i.total_price
            totalearnings += i.total_price
    except:
        totalearnings = 0

    
    try:
        totalsale=0
        total_sales = Order.objects.all()
        for i in total_sales:
            i.total_price
            totalsale+=i.total_price
    except:
        totalsale=0

    
    # Other statistics calculations (totalsale, totalearnings, status_delivery, status_cancel, status_return)

    context = {
        'totalsale': totalsale,
        'totalearnings': totalearnings,
        'status_delivery': status_delivery,
        'status_cancel': status_cancel,
        'status_return': status_return,
        'orders': orders,
        'categories': categories,
        'sales_values': sales_values,
        'return_values': return_values,
    }

    return render(request, 'admin/dashboard.html', context)


# /////////////////////////////////
# def dashboard(request):
#     if not request.user.is_superuser:
#         return redirect('adminsignin')
    
#     sales_data = OrderItem.objects.values('order__created_at__date').annotate(total_sales=Sum('price')).order_by('-order__created_at__date')
#     # Prepare data for the chart
#     categories = [item['order__created_at__date'].strftime('%d/%m') for item in sales_data]
#     sales_values = [item['total_sales'] for item in sales_data]
   
#     return_data = OrderItem.objects.filter(orderitem_status__item_status__in=["Return", "Cancelled"]).values('order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
#     return_values = [item['total_returns'] for item in return_data]
#     orders =Order.objects.order_by('-created_at')[:10]
#     try:
#         totalsale=0
#         total_sales =Order.objects.all()
#         for i in total_sales:
#             i.total_price
#             totalsale+=i.total_price
#     except:
#          totalsale=0 
#     try:
#         totalearnings=0
#         total_earn =Order.objects.filter(order_status__id=4)
#         for i in total_earn:
#             i.total_price
#             totalearnings+=i.total_price
#     except:
#          totalearnings=0       
        
#     try:
#         status_delivery =Order.objects.filter(order_status__id=4).count()
#         status_cancel =Order.objects.filter(order_status__id=5).count()
#         status_return =Order.objects.filter(order_status__id=6).count()
#         Total = status_delivery + status_cancel + status_return 
#         status_delivery = (status_delivery / Total) * 100
#         status_cancel = (status_cancel / Total) * 100
#         status_return = (status_return / Total) * 100
#     except:
#         status_delivery=0
#         status_cancel=0
#         status_return=0
            
#     context = {
#         'totalsale':totalsale,
#         'totalearnings':totalearnings,
#         'status_delivery':status_delivery,
#         'status_cancel':status_cancel,
#         'status_return':status_return,
#         'orders':orders,
#         'categories': categories,
#         'sales_values': sales_values,
#         'return_values': return_values,
#     }
    
#     return render(request,'admin/dashboard.html',context)


# sale report for admin 
@login_required(login_url='adminsignin')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')

    if request.method=='GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
    
        if start_date and end_date:
            # Filter orders based on the selected date range
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            if start_date > end_date:
                messages.error(request, "Start date must be before end date.")
                return redirect('sales_report')
            if end_date > date.today():
                messages.error(request, "End date cannot be in the future.")
                return redirect('sales_report')

            orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            # If no date range is selected, fetch recent 10 orders
            recent_orders = Order.objects.order_by('-created_at')[:10]
            orders = Order.objects.all()
  
    # Calculate total sales and total orders
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    # Calculate sales by status
    sales_by_status = {
        'Pending': orders.filter(order_status= 1).count(),
        'Processing': orders.filter(order_status=2).count(),
        'Shipped': orders.filter(order_status=3).count(),
        'Delivered': orders.filter(order_status=4).count(),
        'Cancelled': orders.filter(order_status=5).count(),
        'Return': orders.filter(order_status=6).count(),
    }
    # Prepare data for rendering the template
    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'admin/salesreport.html', {'sales_report': sales_report})

# generate csv on admin side for sale report 
@login_required(login_url='adminsignin')
def export_csv(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_mode', 'tracking_no', 'Orderd at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()
    for order in orders:
        order_items = OrderItem.objects.filter(order=order).select_related('variant')  # Use select_related to optimize DB queries
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user.first_name if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",  # Only include date in the first row
                    order_item.variant.product.product_name,  # Replace 'product_name' with the actual attribute in your Product model
                    order_item.price,
                    order_item.quantity,
                ])

    return response

# generate pdf on admin side for sale report
@login_required(login_url='adminsignin')
def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.pdf'
    w_pt = 8.5 * 40  # 8.5 inches width
    h_pt = 11 * 20   # 11 inches height   

    pdf = FPDF(format=(w_pt, h_pt))
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)  # Enable auto page break with 15mm margin

    # Set font styles
    pdf.set_font('Arial', 'B', 12)  # Reduce font size for better readability

    # Header Information
    pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
    pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')
    # Table Data
    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No', 'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]
    orders = Order.objects.all().prefetch_related(
        Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('variant'))
    )
    for order in orders:
        order_items = order.orderitem_set.all()
        for index, order_item in enumerate(order_items):
            data.append([
                order.user.first_name if index == 0 else "",
                order.total_price if index == 0 else "",
                order.payment_mode if index == 0 else "",
                order.tracking_no if index == 0 else "",
                str(order.created_at.date()) if index == 0 else "",
                order_item.variant.product.product_name,
                order_item.price,
                order_item.quantity,
            ])
    # Create Table
    col_width = 40  
    row_height = 10
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln()
    response.write(pdf.output(dest='S').encode('latin1'))  
    return response