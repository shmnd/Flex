from django.urls import path, include
from .import views

urlpatterns = [
    path('adminsignin/',views.adminsignin, name='adminsignin'),
    path('adminsignup/',views.adminsignup, name='adminsignup'),
    path('',views.dashboard, name='dashboard'),
    path('user/',views.user, name='user'),
    path('searchuser/',views.searchuser, name='searchuser'),
    path('brands/', views.brands, name='brands'),
    path('search_brand/', views.search_brand, name='search_brand'),
    path('createbrands/', views.createbrands, name='createbrands'),
    path('editbrands/<slug:editbrands_id>', views.editbrands, name='editbrands'),
    path('deletebrands/<slug:deletebrands_id>', views.deletebrands, name='deletebrands'),
    path('blockuser/<int:user_id>', views.blockuser, name="blockuser"),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
]