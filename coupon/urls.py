from django.urls import path
from .import views


urlpatterns = [
    path('coupon/',views.coupon,name='coupon'),
    path('addcoupon/',views.addcoupon,name='addcoupon'),
    path('editcoupon/<int:coupon_id>',views.editcoupon,name='editcoupon'),
    path('searchcoupon/',views.searchcoupon,name='searchcoupon'),
    path('deletecoupon/<int:coupon_id>',views.deletecoupon,name='deletecoupon'),
    
]
