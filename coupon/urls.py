from django.urls import path
from .import views


urlpatterns = [
    path('coupon/',views.coupon,name='coupon'),
    path('addcoupon/',views.addcoupon,name='addcoupon'),
    path('editcoupon/',views.editcoupon,name='editcoupon'),
    path('searchcoupon/',views.searchcoupon,name='searchcoupon'),
    path('deletecoupon/',views.deletecoupon,name='deletecoupon'),
    
]
