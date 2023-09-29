from django.urls import path,include
from . import views

urlpatterns=[  
    path('Shop/',views.Shop,name='Shop'),
    path('shopfilter/',views.shop_filter,name='shop_filter'),
    path('shopsort/',views.shop_sort,name='shop_sort'),
]