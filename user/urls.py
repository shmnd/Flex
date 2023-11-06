from django.urls import path
from . import views

urlpatterns=[
    path('userprofile',views.userprofile,name='userprofile'),
    path('addaddress/<int:add_id>',views.addaddress,name='addaddress'),
    path('editaddress/<int:edit_id>',views.editaddress,name='editaddress'),
    path('viewaddress/<int:view_id>',views.viewaddress,name='viewaddress'),
    path('deleteaddress/<int:delete_id>',views.deleteaddress,name='deleteaddress'),
    
    path('editprofile',views.editprofile,name='editprofile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('orderviewuser/<int:view_id>',views.orderviewuser,name='orderviewuser'),   
    
    path('validate_referral/',views.validate_referral,name='validate_referral'),   
    
]