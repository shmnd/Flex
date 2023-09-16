from django.urls import path
from .import views

urlpatterns = [
    path('',views.products,name='products'),
    path('createproduct.',views.createproduct,name='createproduct'),
    path('editproduct/<int:editproduct_id>',views.editproduct,name='editproduct'),
    path('deleteproduct/<int:deleteproduct_id>',views.deleteproduct,name='deleteproduct'),
    path('searchproduct',views.searchproduct,name='searchproduct')
]
