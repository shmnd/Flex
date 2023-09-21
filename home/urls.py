from django.urls import path 
from .import views

urlpatterns = [
    path('',views.home, name='home'),
    path('productshow/<int:prod_id>/<int:img_id>',views.productshow,name='productshow'),
    path('usercategoryshow/<int:category_id>',views.usercategoryshow,name='usercategoryshow'),
    # path('contact/',views.contact, name='contact'),
    # path('admin_contact/',views.admin_contact, name='admin_contact'),
    # path('search_contact/',views.search_contact, name='search_contact'),
    path('blog/',views.blog, name='blog'),
]
