from django.urls import path 
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('productshow/<int:prod_id>/<int:img_id>',views.productshow,name='productshow'),
    path('usercategoryshow/<int:category_id>',views.usercategoryshow,name='usercategoryshow'),
    # blog is only html page there is no view or url (did'nt crearte app for blog)
    path('shop/shop/blog.html', views.blog, name='blog'),
 
]
