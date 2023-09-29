from django.urls import path,include
from . import views

urlpatterns=[  
    path('shop/',views.shop,name='shop'),
    path('shopfilter/',views.shopfilter,name='shopfilter'),
    path('shopsort/',views.shopsort,name='shopsort'),
]