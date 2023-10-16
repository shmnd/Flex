from django.urls import path
from .import views
# from views import *

urlpatterns = [
    path('product',views.product,name='product'),
    path('createproduct.',views.createproduct,name='createproduct'),
    path('editproduct/<int:product_id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:product_id>',views.deleteproduct,name='deleteproduct'),
    path('productview/<int:product_id>', views.productview, name='productview'),    
    path('searchproduct/',views.searchproduct,name='searchproduct'),
    path('addreview/', views.addreview, name='addreview'),     
    
]
