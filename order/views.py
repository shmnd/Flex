from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from checkout.models import Order,OrderItem,Orderstatus,Itemstatus
from order.models import Orderreturn,Order_cancelled
from product.models import Product
from user.models import Address, Wallet
from variant.models import Variant,VariantImage
from cart.models import Cart
from django.db.models import Q
from django.contrib import messages

# Create your views here.


def orderlist(request):
    order=Order.objects.all().order_by('id')
    
    context={
        'order':order,
    }
    
    return render(request,'admin/order.html')


def orderview(requset):
    
    try:
        orderview=Order.objects.all(id=view_id)
        address=Address.objects.get(id=orderview.address.id)
        products=OrderItem.objects.filter(order=view_id)
        variant_ids=[product.variant.id for product in products]
        image=VariantImage.objects.filter(variant__id__in=variant_ids).distinct('variant__color')
        item_status_o=Itemstatus.objects.all()
        context={
            'orderview':orderview,
            'address':address,
            'products':products,
            'image':image,
            'item_status_o':item_status_o,
            
        }
        return render(request,'view/orderview.html',context)
    except Order.DoesNotExist:
        print('order does not exist')
    except Address.DoesNotExist:
        print('addres does not exist')
    return redirect('orderlist')
    
    
def changestatus(request):
    
    if not request.user.is_superuser:
        return redirect('adminsignin')
    
    orderitem_id=request.POST.get('orderitem_id')
    order_status=request.POST.get('status')
    order_variant=request.POST.get('variant_id')
    
    order_items=OrderItem.objects.get(variant=order_variant,id=orderitem_id)
    item_status_instance=Itemstatus.objects.get(id=order_status)
    veiw_id=orderitems.order.id
    
    try:
    # ṭotal item status
        all_order_item=OrderItem.objects.filter(order=view_id)
          
          
        total_count=all_order_item()
        
        Pending=all_order_item.filter(orderitem_status__id=1).count()
        Processing = all_order_item.filter(orderitem_status__id=2).count()
        Shipped = all_order_item.filter(orderitem_status__id=3).count()
        Delivered = all_order_item.filter(orderitem_status__id=4).count()
        Cancelled = all_order_item.filter(orderitem_status__id=5).count()
        Return = all_order_item.filter(orderitem_status__id=6).count()
        
        if total_count ==Pending:
            total_value==1
        elif total_count==Processing:
            total_value=2
        elif total_count==Shipped:
            total_value=3
        elif total_count== Delivered:
            total_value=4
        elif total_count==Cancelled:
            total_value=5
        elif total_count==Return:
            total_value=6
        else:
            total_value=1
            
    except:
        return redirect('orderview',view_id)
    
    change_all_item_status=Order.objects.get(id=view_id)
    item_status_instance_all=Orderstatus.objects.get(id=total_value)
    change_all_item_status.order_status=item_status_instance_all
    change_all_item_status.save()
    
    messages.success(request,'status updated')
    return redirect('order_view',view_id)



def returnorder(request,return_id):
    try:
        orderitem_id=OrderItem.objects.get(id=return_id)
        view_id=orderitem_id.order.id
    except:
        return redirect('userprofile')
    if request.method=='POST':
        options=request.POST.get('options')
        reason=request.POST.get('reason')
        
    # validation
    
        if options.strip()=='':
            messages.error(request,'enter your options')
            return redirect('orderviewstatus',view_id)
        if reason.strip()=='':
            messages.error(request,'enter your reason')
            return redirect('orderviewuser',view_id)
        reason_checking=len(reason)
        if not reason_checking<20:
            messages.error(request,'write minimum 20 lines')
            return  redirect('overviewstatus',view_id)
        
    qty=orderitem_id.quantity
    variant_id=orderitem_id.variant.id
    order_id=Order.objects.get(id=orderitem_id.order.id)
    
    variant=Variant.objects.filter(id=variant_id).first()
    variant_quantity=variant.quantity +qty
    variant.save()
    
    order_item_id=Itemstatus.objects.get(id=6)
    orderitem_id.orderitem_status=order_item_id
    total_P =orderitem_id.price
    print(total_P)
    orderitem_id.save()
    try:
        # total item status
        all_order_item=OrderItem.objects.filter(order=view_id)
        
        # import pdb
        # pdb.set_trace()
        total_count= all_order_item.count()
        
        Pending=all_order_item.filter(orderitem_status__id=1).count()
        Processing = all_order_item.filter(orderitem_status__id=2).count()
        Shipped = all_order_item.filter(orderitem_status__id=3).count()
        Delivered = all_order_item.filter(orderitem_status__id=4).count()
        Cancelled = all_order_item.filter(orderitem_status__id=5).count()
        Return = all_order_item.filter(orderitem_status__id=6).count()
        
        if total_count == Pending:
            total_value = 1
        elif total_count == Processing:
            total_value = 2  
        elif total_count == Shipped:
            total_value = 3
        elif total_count == Delivered:
            total_value = 4
        elif total_count == Cancelled:
            total_value = 5
        elif total_count == Return:
            total_value = 6
        else:
            total_value = 4   
    
    except:
        return redirect('orderview',view_id) 
    
    change_all_item_status = Order.objects.get(id=view_id)
    item_status_instance_all=Orderstatus.objects.get(id=total_value)
    change_all_item_status.order_status=item_status_instance_all
    change_all_item_status.save()
    
    returnorder=Orederreturn.objects.create(user=request.user,order=order_id,options=options,reason=reason)
    order= Order.objects.filter(id=view_id).first()
    if variant.product.offer:
        total_price=variant.product.product_price*qty
        offer_price=variant.product.offer.discount_amount*qty
        total_price= total_price-offer_price
    else:
        total_price=variant.product.product_price*qty
    if order.return_total_price:
        pass
    else:
        order.return_total_price=int(order.total_price)
    order.return_total_price=order.return_total_price-total_price
    if order.return_total_price<0:
        order.return_total_price=None
    order.save()
    try:
        wallet=Wallet.objects.get(user=request.user)
        wallet.wallet += total_price
        wallet.save()
    except Wallet.DoesNotExist:
        wallet=Wallet.objects.create(user=request.user,wallet=total_price)
        
        orderitem_id.save()
        messages.success(request,'your order return sucessfuly')
        return redirect('orderviewuser',view_id)
    
    
def ordercancel(request,cancel_id):
    try:
        orderitem_id=OrderItem.objects.get(id=cancel_id)
        orderitem=orderitem_id
        view_id=orderitem_id.order.id
    except:
        return redirect('userprofile')
    if request.method=='POST':
        options=request.POST.get('options')
        reason= request.POST.get('reason')
    #  validation
    
        if options.strip():
            messages.error(request,'enter your options')
            return redirect('orderviewuser',view_id)
        if reason.strip():
            messages.error(request,'reason must be added')
            return redirect('orderviewuser',view_id)
        
        
        order=Order.objects.filter(id=view_id).first()
        qty=orderitem.quantity
        variant_id=orderitem.variant.id
        variant=Variant.objects.filter(id=variant_id).first()
        cancelled=Order_Cancelled.objects.createf(user=request.user,order=order)
        
        if order.payment_mode=='razopay' or order.payment_mode=='wallet':
            order=Order.objects.get(id=view_id)
            
            
            if variant.product.offer:
                total_price= variant.product.product_price*qty
                offer_price=variant.product.offer.discount_amount*qty
                # total_price=total_price-offer_price
            else:
                total_price=variant.product.product_price*qty
            if order.return_total_price:
                pass
            else:
                order.return_total_price=int(order.total_price)
            order.return_total_price=order.return_total_price-total_price
            
            if order.coupon:
                if order.return_total_price<order.coupon.min_price:
                    total_price=total_price-order.coupon.coupon_discount_amount
                    order.coupon=None
                else:
                    pass
                if order.return_total_price<0:
                    order.return_total_price=None
                order.save()
                try:
                    wallet=Wallet.objects.get(user=request.user)
                    wallet.wallet += total_price
                    wallet.save()
                except Wallet.DoesNotExist:
                    wallet=Wallet.objects.create(user=request.user,wallet=total_price)
            # udate the product quantity
            variant.quantity=variant.quantity+qty
            variant.save()
            order_item_id=Itemstatus.objects.get(id=5)
            all_order_item=OrderItem.object.filter(order=view_id)
            orderitem.orderitem_status=order_item_id
            orderitem.save()
            try:
                # total item_status
                all_order_item=OrderItem.objects.filter(order=view_id)
                # import pdb
                # pdb.set_trace()
                total_count = all_order_item.count()
                
                Pending=all_order_item.filter(orderitem_status__id=1).count()
                Processing=all_order_item.filter(orderitem_status__id=2).count()
                Shipped=all_order_item.filter(orderitem_status__id=3).count()
                Delivered=all_order_item.filter(orderitem_status__id=4).count()
                Cancelled=all_order_item.filter(orderitem_status__id=5).count()
                Return=all_order_item.filter(orderitem_status__id=6).count()
                
                if total_count == Pending:
                    total_value = 1
                elif total_count == Processing:
                    total_value = 2  
                elif total_count == Shipped:
                    total_value = 3
                elif total_count == Delivered:
                    total_value = 4
                elif total_count == Cancelled:
                    total_value = 5
                elif total_count == Return:
                    total_value = 6
                else:
                    total_value = 1    
            
            except:
                return redirect('order_view',view_id)
            
            change_all_items_status=Order.objects.get(id=view_id)
            item_status_instance_all=Orderstatus.objects.get(id=total_value)
            change_all_items_status.order_status=item_status_instance_all
            change_all_items_status.save()
            messages.success(request,'your order cancelled success')
            return redirect('orderviewuser',view_id)
        return redirect('userprofile')
            
            
def ordersearch(requset):
    search=requset.POST.get('search')
    if search is None or search.strip() == '':
        messages.error(request,'Filed cannot empty!')
        return redirect('order_list')
    order=Order.objects.filter(Q(user__first_name__icontains=search)| Q(created_at__icontains=search) |Q(total_price__icontains=search))
    context={'order':order,}
    if order:
        pass
    else:
        order:False
        messages.error(request,'search not found')
        return redirect('orderlist')
    return render(request,'admin/order.html',context)
                
                
                
def orderstatusshow(request):
    name=request.POST.get('name')
    if name=='Pending':
        order=Order.objects.filter(order_status=1)
        context={'order':order}
        return render(request,'admin/order.html',context)
    if name == 'Processing':
        order = Order.objects.filter(order_status=2)
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    if name == 'Shipped':
        order = Order.objects.filter(order_status=3)
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    if name == 'Delivered':
        order = Order.objects.filter(order_status=4)
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    if name == 'Cancelled':
        order = Order.objects.filter(order_status=5)
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    if name == 'Return':
        order = Order.objects.filter(order_status=6)
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    if name == 'All':
        order =Order.objects.all().order_by('id')
        context={'order':order,}   
        return render(request,'admin/order.html',context)
    else:
        return redirect('orderlist')
    
def orderpaymentsort(request):
    name=request.POST.get('name')
    if name=='cod':
        order=Order.objects.filter(payment_mode='cod')
        context={'order':order}
        return render(request,'admin/order.html',context)
    if name=='razorpay':
        order=Order.object.filter(payment_mode='razorapay')
        context={'order':order}
        return render(request,'admin/order.html',context)
    else:
        return redirect('orderlist')
                