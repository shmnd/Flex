from django.urls import path, include
from .import views

urlpatterns = [
    path('adminsignin/',views.adminsignin, name='adminsignin'),
    path('adminsignup/',views.adminsignup, name='adminsignup'),
    path('',views.dashboard, name='dashboard'),
    path('user/',views.user, name='user'),
    path('searchuser/',views.searchuser, name='searchuser'),
    path('blockuser/<int:user_id>', views.blockuser, name="blockuser"),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    
    path('sales_report/',views.sales_report,name='sales_report'),
    
    path('export_csv/',views.export_csv,name='export_csv'),
    path('generate_pdf/',views.generate_pdf,name='generate_pdf'),
    path('export_excel/',views.export_excel,name='export_excel'),
    


]