from django.contrib import admin
from .models import Order,OrderItem,Orderstatus,Itemstatus


# Register your models here.
admin.site.register(Orderstatus)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Itemstatus)


