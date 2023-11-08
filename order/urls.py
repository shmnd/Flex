from django.urls import path
from . import views

urlpatterns=[  
    path('orderlist/',views.orderlist,name='orderlist'),
    path('orderview/<int:view_id>',views.orderview,name='orderview'),
    path('changestatus/',views.changestatus,name='changestatus'),
    path('ordersearch/',views.ordersearch,name='ordersearch'),
    path('orderpaymentsort/',views.orderpaymentsort,name='orderpaymentsort'),
    path('orderstatusshow/',views.orderstatusshow,name='orderstatusshow'),
    path('returnorder/<int:return_id>',views.returnorder,name='returnorder'),
    path('ordercancel/<int:cancel_id>',views.ordercancel,name='ordercancel'),
    path('generatepdf/',views.generatepdf,name='generatepdf'),
]