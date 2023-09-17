from django.urls import path
from .import views
# from views import *

urlpatterns = [
    path('product',views.product,name='product'),
    path('createproduct.',views.createproduct,name='createproduct'),
    path('editproduct/<int:editproduct_id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:deleteproduct_id>',views.deleteproduct,name='deleteproduct'),
    path('product_view/<int:product_id>', views.product_view, name='product_view'),    
    path('searchproduct',views.searchproduct,name='searchproduct')
]
