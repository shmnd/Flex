from django.urls import path
from . import views

urlpatterns=[
    
    path('cart',views.cart,name='cart'),
    path('removecart/<int:cart_id>',views.removecart,name='removecart'),
    path('addcart',views.addcart,name='addcart'),
    path('updatecart/',views.updatecart,name='updatecart'),
      
]